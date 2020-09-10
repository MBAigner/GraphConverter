import numpy as np
from GraphConverter.util import StorageUtil, constants


class DocumentMetaCharacteristics(object):

    x_var = 0
    y_var = 0
    font_size_var = 0
    bold_pct = 0
    italic_pct = 0
    font_name_entropy = 0
    font_size_entropy = 0
    mean_x_diff_page = []

    def __init__(self, locations, media_boxes, optimize=True):
        self.page_ratio_x = constants.DEFAULT_PAGE_RATIO_X
        self.page_ratio_y = constants.DEFAULT_PAGE_RATIO_Y
        self.x_eps = constants.DEFAULT_X_EPS
        self.y_eps = constants.DEFAULT_Y_EPS
        self.x_phys = constants.DEFAULT_X_PHYS
        self.font_eps_h = constants.DEFAULT_FONT_EPS_HORIZONTAL
        self.font_eps_v = constants.DEFAULT_FONT_EPS_VERTICAL
        self.width_pct_eps = constants.DEFAULT_WIDTH_PCT
        self.width_page_eps = constants.DEFAULT_PAGE_WIDTH_EPS
        self.avg_widths = []
        self.x_var_page = []
        self.y_var_page = []
        self.x_diff_page = []
        self.mean_x_diff_page = []
        self.mean_y_diff_page = []
        self.y_diff_page = []
        self.locations = locations
        self.media_boxes = media_boxes
        self.optimize_params = optimize
        self.num_pages = int(np.max(self.locations["page"])) + 1
        self.threshold_x = np.full(self.num_pages, 250)
        self.threshold_y = np.full(self.num_pages, 150)
        self.media_box_width = np.full(self.num_pages, 600)
        self.threshold_page_width = np.full(self.num_pages, 600)
        self.font_name_entropy = 0
        self.font_size_entropy = 0

    def optimize(self):
        """

        :return:
        """
        # x and y coordinate difference deviations
        for page in self.locations["page"].unique():
            page_loc = self.locations[self.locations["page"] == page]
            xs = sorted(page_loc["x_0"].unique())
            xs_diff = [j-i for i, j in zip(xs[:-1], xs[1:])]
            ys = sorted(page_loc["y_0"].unique())
            ys_diff = [j-i for i, j in zip(ys[:-1], ys[1:])]
            # x0 and y0 differences + means + standard deviations
            self.x_diff_page.append(xs_diff)
            self.mean_x_diff_page.append(np.mean(xs_diff) if len(xs_diff) > 0 else 0)
            self.x_var_page.append(np.std(xs_diff) if len(xs_diff) > 1 else 0)
            self.y_diff_page.append(ys_diff)
            self.mean_y_diff_page.append(np.mean(ys_diff) if len(ys_diff) > 0 else 0)
            self.y_var_page.append(np.std(ys_diff) if len(ys_diff) > 1 else 0)
            # average widths
            self.avg_widths.append((page_loc["x_1"] - page_loc["x_0"]).mean())
        # coordinate difference standard deviation means
        self.x_var = np.mean(self.x_var_page)
        self.y_var = np.mean(self.y_var_page)
        # font size deviations
        self.font_size_var = np.std(self.locations["font_size"])
        font_size_pct = self.locations["font_size"].value_counts() / len(self.locations)
        if len(font_size_pct) == 1:
            self.font_size_entropy = 0
        else:
            for pct in font_size_pct:
                self.font_size_entropy -= pct * np.log(pct) / np.log(len(font_size_pct))
        # bold + italic percentages
        self.bold_pct = np.mean(self.locations["bold"])
        self.italic_pct = np.mean(self.locations["italic"])
        # font entropy
        font_name_pct = self.locations["font_name"].value_counts() / len(self.locations)
        if len(font_name_pct) == 1:
            self.font_name_entropy = 0
        else:
            for pct in font_name_pct:
                self.font_name_entropy -= pct * np.log(pct) / np.log(len(font_name_pct))

    def regress_parameters(self):
        """

        :return:
        """
        X = [[self.font_size_entropy, self.font_name_entropy, self.bold_pct,
              self.italic_pct, self.x_var, self.y_var, np.mean(self.avg_widths)]]
        self.x_eps = constants.DEFAULT_X_EPS
        self.y_eps = constants.DEFAULT_Y_EPS
        self.x_phys = constants.DEFAULT_X_PHYS
        self.font_eps_h = constants.DEFAULT_FONT_EPS_HORIZONTAL
        self.font_eps_v = constants.DEFAULT_FONT_EPS_VERTICAL
        self.width_pct_eps = constants.DEFAULT_WIDTH_PCT
        self.width_page_eps = 1
        self.page_ratio_x = StorageUtil.load_object(constants.MODEL_PATH, "page_ratio_x").predict(X)
        self.page_ratio_y = StorageUtil.load_object(constants.MODEL_PATH, "page_ratio_y").predict(X)
        self.x_eps = StorageUtil.load_object(constants.MODEL_PATH, "x_eps").predict(X)
        self.x_phys = self.x_eps
        self.y_eps = StorageUtil.load_object(constants.MODEL_PATH, "page_ratio_y").predict(X)
        self.font_eps_h = StorageUtil.load_object(constants.MODEL_PATH, "font_eps").predict(X)
        self.font_eps_v = self.font_eps_h
        self.width_pct_eps = StorageUtil.load_object(constants.MODEL_PATH, "width_pct_eps").predict(X)
        self.width_page_eps = StorageUtil.load_object(constants.MODEL_PATH, "threshold_page_width").predict(X)

    def generate_attributes(self):
        """

        :return:
        """
        self.optimize()  # calculate meta characteristics
        if self.optimize_params:
            self.regress_parameters()
        # default thresholds based on page size
        for page in range(self.num_pages):
            self.media_box_width[page] = self.media_boxes[page]['x1'] - \
                                         self.media_boxes[page]['x0']
            self.threshold_page_width[page] = self.width_page_eps * self.media_box_width[page]
            self.threshold_x[page] = abs(self.media_boxes[0]['x1'] -
                                         self.media_boxes[0]['x0']) / self.page_ratio_x
            self.threshold_y[page] = abs(self.media_boxes[0]['y1'] -
                                         self.media_boxes[0]['y0']) / self.page_ratio_y
