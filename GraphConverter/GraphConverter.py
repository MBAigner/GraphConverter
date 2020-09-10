from PDFContentConverter import PDFContentConverter
import networkx as nx
import numpy as np
from GraphConverter.util import RectangleUtil, constants
from GraphConverter.document.DocumentMetaCharacteristics import DocumentMetaCharacteristics
from GraphConverter.merging.PDFTextBoxMerging import PDFTextBoxMerging


class GraphConverter(object):

    def __init__(self, pdf, merge_boxes=False, regress_parameters=False,
                 use_font=True, use_width=True, use_rect=True, use_horizontal_overlap=False,
                 use_vertical_overlap=False,
                 page_ratio_x=2, page_ratio_y=2, x_eps=2, y_eps=2, font_eps_h=1, font_eps_v=1,
                 width_pct_eps=.4, width_page_eps=.5):
        self.pdf = pdf
        self.set_attributes(merge_boxes, regress_parameters,
                            use_font, use_width, use_rect, use_horizontal_overlap, use_vertical_overlap,
                            page_ratio_x, page_ratio_y, x_eps, y_eps, font_eps_h, font_eps_v,
                            width_pct_eps, width_page_eps)
        conv = PDFContentConverter(self.pdf).convert()
        self.loc_df = conv["content"]
        self.media_boxes = conv["media_boxes"]
        self.n = conv["page_count"]
        self.loc_df = PDFTextBoxMerging(data=self.loc_df,
                                        media_boxes=self.media_boxes).transform()
        if self.loc_df is not None:
            self.meta = DocumentMetaCharacteristics(self.loc_df, self.media_boxes,
                                                    optimize=regress_parameters)
            self.meta.generate_attributes()

    def set_attributes(self, merge_boxes, regress_parameters,
                       use_font, use_width, use_rect, use_horizontal_overlap, use_vertical_overlap,
                       page_ratio_x, page_ratio_y, x_eps, y_eps, font_eps_h, font_eps_v,
                       width_pct_eps, width_page_eps):
        """

        :param merge_boxes:
        :param regress_parameters:
        :param use_font:
        :param use_width:
        :param use_rect:
        :param use_horizontal_overlap:
        :param use_vertical_overlap:
        :param page_ratio_x:
        :param page_ratio_y:
        :param x_eps:
        :param y_eps:
        :param font_eps_h:
        :param font_eps_v:
        :param width_pct_eps:
        :param width_page_eps:
        :return:
        """
        constants.USE_FONT = use_font
        constants.USE_WIDTH = use_width
        constants.USE_RECT = use_rect
        constants.USE_HORIZONTAL_OVERLAP = use_horizontal_overlap
        constants.USE_VERTICAL_OVERLAP = use_vertical_overlap
        constants.MERGE_RECTANGLE_TEXT_BOXES = merge_boxes
        constants.USE_RECTANGLE_BOX_COORDINATES = merge_boxes
        constants.OPTIMIZE = regress_parameters
        constants.DEFAULT_PAGE_RATIO_X = page_ratio_x
        constants.DEFAULT_PAGE_RATIO_Y = page_ratio_y
        constants.DEFAULT_X_EPS = x_eps
        constants.DEFAULT_Y_EPS = y_eps
        constants.DEFAULT_X_PHYS = x_eps
        constants.DEFAULT_FONT_EPS_HORIZONTAL = font_eps_h
        constants.DEFAULT_FONT_EPS_VERTICAL = font_eps_v
        constants.DEFAULT_WIDTH_PCT = width_pct_eps
        constants.DEFAULT_PAGE_WIDTH_EPS = width_page_eps

    def convert(self):
        """

        :return:
        """
        if self.loc_df is None:
            return [], None

        self.loc_df.set_index("id", inplace=True)
        self.loc_df["cluster_label"] = 0

        graph_list = []
        for page in range(self.meta.num_pages):
            G = nx.MultiDiGraph()
            loc_df_page = self.loc_df[self.loc_df["page"] == page]
            G.add_nodes_from(list(loc_df_page.index))
            nodes = loc_df_page.to_dict("index")
            nx.set_node_attributes(G, nodes)
            G = self.add_edges(G, page)
            G = nx.disjoint_union(nx.MultiDiGraph(), G)
            G = self.label_loops(G)
            graph_list.append(G)
        return {"graphs": graph_list,
                "document_meta": self.meta}

    def add_edges(self, G, page=0):
        """

        :param G:
        :param page:
        :return:
        """
        nodes = dict(G.nodes(data=True))
        node_ids = list(nodes.keys())
        for i in range(len(node_ids) - 1):
            id1 = node_ids[i]
            node1 = nodes[id1]

            for j in range(i + 1, len(node_ids)):
                id2 = node_ids[j]
                node2 = nodes[id2]

                delta_x_min = min(abs(node2["x_0"] - node1["x_0"]),
                                  abs(node2["x_1"] - node1["x_1"]),
                                  abs(node2["pos_x"] - node1["pos_x"]))
                delta_y_min = min(abs(node2["y_0"] - node1["y_0"]),
                                  abs(node2["y_1"] - node1["y_1"]),
                                  abs(node2["pos_y"] - node1["pos_y"]))
                length_x_min = min(abs(node2["x_1"] - node1["x_0"]),
                                   abs(node2["x_0"] - node1["x_1"]))
                length_y_min = min(abs(node2["y_1"] - node1["y_0"]),
                                   abs(node2["y_0"] - node1["y_1"]))
                delta_f = abs(node2["font_size"] - node1["font_size"])

                # horizontal edges
                if self.fulfills_horizontal_edge_conditions(node1, node2, page,
                                                            delta_f, length_x_min, delta_y_min):
                    if node1["pos_x"] < node2["pos_x"]:
                        G = self.get_horizontal_edge(G, id1, id2, length_x_min)
                    else:
                        G = self.get_horizontal_edge(G, id2, id1, length_x_min)

                # vertical edges
                if self.fulfills_vertical_edge_conditions(node1, node2, page,
                                                          delta_x_min, length_y_min, delta_f):
                    if node2["y_1"] > node1["y_1"]:
                        G = self.get_vertical_edge(G, id1, id2, length_y_min)
                    else:
                        G = self.get_vertical_edge(G, id2, id1, length_y_min)
        return G

    def get_horizontal_edge(self, G, id_start, id_end, length):
        """

        :param G:
        :param id_start:
        :param id_end:
        :param length:
        :return:
        """
        edges_from_node = [e for e in G.out_edges(id_start, keys=True, data=True)
                           if e[3]["direction"] == "h"]
        if len(edges_from_node) == 0:
            G.add_edge(id_start, id_end, length=length,
                       lengthx_phys=length, lengthy_phys=0, direction="h",
                       weight=length, key="h")
        elif len(edges_from_node) == 1:
            if edges_from_node[0][3]["lengthx_phys"] >= length:
                G.remove_edges_from(edges_from_node)
                G.add_edge(id_start, id_end, length=length,
                           lengthx_phys=length, lengthy_phys=0, direction="h",
                           weight=length, key="h")
        return G

    def get_vertical_edge(self, G, id_start, id_end, length):
        """

        :param G:
        :param id_start:
        :param id_end:
        :param length:
        :return:
        """
        edges_from_node_phys = [e for e in G.out_edges(id_start, keys=True, data=True)
                                if e[3]["direction"] == "v"]
        if len(edges_from_node_phys) == 0:
            G.add_edge(id_start, id_end, length=length,
                       lengthx_phys=0, lengthy_phys=length,
                       direction="v", weight=length, key="v")
        elif len(edges_from_node_phys) == 1:
            if edges_from_node_phys[0][3]["lengthy_phys"] >= length:
                G.remove_edges_from(edges_from_node_phys)
                G.add_edge(id_start, id_end, length=length,
                           lengthx_phys=0, lengthy_phys=length,
                           direction="v", weight=length, key="v")
        return G

    def label_loops(self, graph):
        """

        :param graph:
        :return:
        """
        loop_labels = dict()
        all_nodes = dict(graph.nodes(data=True))
        subgraph_H = nx.DiGraph()
        subgraph_V = nx.DiGraph()
        subgraph_H.add_nodes_from(graph)
        subgraph_V.add_nodes_from(graph)
        subgraph_H.add_edges_from([(e[0], e[1]) for e in graph.edges(keys=True, data=True) if e[2] == "h"])
        subgraph_V.add_edges_from([(e[0], e[1]) for e in graph.edges(keys=True, data=True) if e[2] == "v"])
        distances = dict(nx.all_pairs_shortest_path_length(subgraph_V, cutoff=3))
        nodes_list = list(subgraph_V.nodes)
        num_nodes = len(subgraph_V)
        A_V = np.zeros((num_nodes, num_nodes))
        for i in range(num_nodes):
            id1 = nodes_list[i]
            if id1 in distances:
                for j in range(num_nodes):
                    id2 = nodes_list[j]
                    if id2 in distances[id1] and id1 != id2:
                        A_V[i, j] = 1
        distances = dict(nx.all_pairs_shortest_path_length(subgraph_H, cutoff=3))
        nodes_list = list(subgraph_H.nodes)
        num_nodes = len(subgraph_H)
        A_H = np.zeros((num_nodes, num_nodes))
        for i in range(num_nodes):
            id1 = nodes_list[i]
            if id1 in distances:
                for j in range(num_nodes):
                    id2 = nodes_list[j]
                    if id2 in distances[id1] and id1 != id2:
                        A_H[i, j] = 1

        loops = np.argwhere((A_H.dot(A_V) + A_V.dot(A_H) == 2) |
                            (A_H.transpose().dot(A_V) + A_V.dot(A_H.transpose()) == 2))
        loop_vertices = list(set(loops.flatten()))
        for x in loops:
            edges_from_node = [e for e in graph.out_edges(x[0], keys=True, data=True)
                               if e[3]["direction"] == "l"]
            lengthx = min(abs(all_nodes[x[0]]["x_0"]-all_nodes[x[1]]["x_1"]), abs(all_nodes[x[0]]["x_1"]-all_nodes[x[1]]["x_0"]))
            lengthy = min(abs(all_nodes[x[0]]["y_0"] - all_nodes[x[1]]["y_1"]), abs(all_nodes[x[0]]["y_1"] - all_nodes[x[1]]["y_0"]))
            length = np.sqrt(lengthx**2 + lengthy**2)
            if len(edges_from_node) == 0:
                graph.add_edge(x[0], x[1], length=length,
                               lengthx_phys=lengthx, lengthy_phys=lengthy, direction="l",
                               weight=1 / length, key="l")
            elif len(edges_from_node) > 0:
                if edges_from_node[0][3]["length"] >= length:
                    graph.remove_edges_from(edges_from_node)
                    graph.add_edge(x[0], x[1], length=length,
                                   lengthx_phys=lengthx, lengthy_phys=lengthy, direction="l",
                                   weight=1 / length, key="l")
        loop_labels.update(dict.fromkeys(loop_vertices, 1))
        nx.set_node_attributes(graph, loop_labels, 'is_loop')
        return graph

    def fulfills_horizontal_edge_conditions(self, node1, node2, page,
                                            delta_f, length_x_min, delta_y_min):
        """

        :param node1:
        :param node2:
        :param page:
        :param delta_f:
        :param length_x_min:
        :param delta_y_min:
        :return:
        """
        return (delta_y_min < self.meta.y_eps or
                (constants.USE_VERTICAL_OVERLAP and
                 GraphConverter.is_vertically_overlapping(node1, node2))) and (
                (length_x_min < self.meta.threshold_x[page] and
                 (not constants.USE_FONT or
                  delta_f < self.meta.font_eps_h
                  )) or
                (constants.USE_RECT and
                 RectangleUtil.is_same_rectangle(node1, node2)))

    def fulfills_vertical_edge_conditions(self, node1, node2, page,
                                          delta_x_min, length_y_min, delta_f):
        """

        :param node1:
        :param node2:
        :param page:
        :param delta_x_min:
        :param length_y_min:
        :param delta_f:
        :return:
        """
        width_1 = node1["x_1"] - node1["x_0"]
        width_2 = node2["x_1"] - node2["x_0"]
        width_rel = abs(width_1 - width_2) / max(width_1, width_2, 1)
        return (delta_x_min < self.meta.x_eps or
                (constants.USE_HORIZONTAL_OVERLAP and
                 GraphConverter.is_horizontally_overlapping(node1, node2))) and\
                (length_y_min < self.meta.threshold_y[page] and
                 (not constants.USE_WIDTH or
                  ((width_rel < self.meta.width_pct_eps or
                    max(width_1, width_2) < self.meta.threshold_page_width[page])))
                 and (delta_f < self.meta.font_eps_v or not constants.USE_FONT)
                 or (constants.USE_RECT and
                     RectangleUtil.is_same_rectangle(node1, node2)))

    @staticmethod
    def is_horizontally_overlapping(node1, node2):
        """

        :param node1:
        :param node2:
        :return:
        """
        union = max(node2["x_1"]-node1["x_0"], node1["x_1"]-node2["x_0"])
        intersection = min(node1["x_1"], node2["x_1"]) - max(node1["x_0"], node2["x_0"])
        return intersection / union >= constants.HORIZONTAL_OVERLAP_THRESHOLD

    @staticmethod
    def is_vertically_overlapping(node1, node2):
        """

        :param node1:
        :param node2:
        :return:
        """
        min_height = min(node1["y_0"] - node1["y_1"], node2["y_0"] - node2["y_1"])
        overlap = min(node1["y_0"], node2["y_0"]) - max(node1["y_1"], node2["y_1"])
        return overlap / min_height >= constants.VERTICAL_OVERLAP_THRESHOLD

    def get_media_boxes(self):
        """

        :return:
        """
        return self.media_boxes

    def get_page_count(self):
        """

        :return:
        """
        return self.n
