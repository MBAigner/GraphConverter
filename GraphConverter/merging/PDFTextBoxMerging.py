import pandas as pd
from GraphConverter.util import constants


class PDFTextBoxMerging(object):

    def __init__(self, data, media_boxes):
        self.data = data
        self.media_boxes = media_boxes

    def transform(self):
        """

        :return:
        """
        if constants.USE_RECTANGLE_BOX_COORDINATES:
            self.data = self.transform_text_to_box_coordinates()
        if constants.MERGE_RECTANGLE_TEXT_BOXES:
            self.data = self.merge_elements()
        return self.data

    def transform_text_to_box_coordinates(self):
        """

        :return:
        """
        return self.data.apply(lambda x: self.text_to_box_coordinates(x), axis=1)

    def text_to_box_coordinates(self, row):
        """

        :param row:
        :return:
        """
        if row["in_element_ids"].count(-1) == 0:
            row["x_0"] = row["in_element_ids"][0]
            row["y_1"] = row["in_element_ids"][1]
            row["y_0"] = row["in_element_ids"][3]
            row["x_1"] = row["in_element_ids"][2]
            row["pos_x"] = (row["x_0"] + row["x_1"]) / 2
            row["pos_y"] = (row["y_0"] + row["y_1"]) / 2
        return row

    def merge_elements(self):
        """

        :return:
        """
        self.data["in_element_ids2"] = self.data["in_element_ids"].apply(str)
        self.data = self.data.sort_values(by=['page', 'in_element_ids2', 'box'])
        data_new = pd.DataFrame(data=None, columns=self.data.columns,
                                index=self.data.index)
        prev_rect = ""
        row_complete = None
        add = False
        for i, row in self.data.iterrows():
            if row["in_element"] != "rectangle" or row["in_element_ids"].count(-1) != 0:
                data_new = data_new.append(row, ignore_index=True)
            else:
                rect = row["in_element_ids2"]
                if rect == prev_rect:
                    row_complete["text"] = row_complete["text"] + "\n" + row["text"]
                    if not constants.USE_RECTANGLE_BOX_COORDINATES:
                        row_complete["x_0"] = min(row["x_0"], row_complete["x_0"])
                        row_complete["y_1"] = min(row["y_1"], row_complete["y_1"])
                        row_complete["y_0"] = max(row["y_0"], row_complete["y_0"])
                        row_complete["x_1"] = max(row["x_1"], row_complete["x_1"])
                    add = True
                else:
                    if row_complete is None:
                        row_complete = row
                    if add and not constants.USE_RECTANGLE_BOX_COORDINATES:
                        page_height = self.media_boxes[int(row_complete["page"])]["y1page"]
                        row_complete["pos_x"] = (row_complete["x_0"] + row_complete["x_1"]) / 2
                        row_complete["pos_y"] = (row_complete["y_0"] + row_complete["y_1"]) / 2
                        row_complete["abs_pos"] = (row_complete["pos_x"],
                                                   page_height - row_complete["pos_y"] -
                                                   page_height * row_complete["page"])
                        add = False
                    data_new = data_new.append(row_complete)
                    row_complete = row
                prev_rect = rect
        data_new.dropna(inplace=True)
        self.data = data_new.drop(["in_element_ids2"], axis=1)
        return self.data
