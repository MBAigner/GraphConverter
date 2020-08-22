
def in_same_element_type(node1, node2):
    """

    :param node1:
    :param node2:
    :return:
    """
    return node1["in_element"] == node2["in_element"]


def is_same_rectangle(node1, node2, use_ids=False):
    """

    :param node1:
    :param node2:
    :param use_ids:
    :return:
    """
    return (node1["in_element"] == "rectangle" and
            node1["in_element_ids"] == node2["in_element_ids"] and
            use_ids) or node1["box"] == node2["box"]


def is_sharing_vertical_border(node1, node2):
    """

    :param node1:
    :param node2:
    :return:
    """
    return ((node1["in_element_ids"] == [] and node2["in_element_ids"] == []) or (
            node1["in_element_ids"] != [] and node2["in_element_ids"] != [] and (
            (node1["in_element_ids"][1] == node2["in_element_ids"][0]) or
            (node1["in_element_ids"][0] == node2["in_element_ids"][1]))))


def is_sharing_horizontal_border(node1, node2):
    """

    :param node1:
    :param node2:
    :return:
    """
    return ((node1["in_element_ids"] == [] and node2["in_element_ids"] == []) or (
            node1["in_element_ids"] != [] and node2["in_element_ids"] != [] and (
            (node1["in_element_ids"][2] == node2["in_element_ids"][3]) or
            (node1["in_element_ids"][3] == node2["in_element_ids"][2]))))
