from GraphConverter.GraphConverter import GraphConverter
from GraphConverter.util import constants

# test file
pdf = "eu-001.pdf"
file = constants.PDF_PATH + pdf

# convert PDF
converter = GraphConverter(file,
                           merge_boxes=False, regress_parameters=True,
                           use_font=True, use_width=True, use_rect=True, use_horizontal_overlap=True,
                           use_vertical_overlap=True,
                           page_ratio_x=2, page_ratio_y=5, font_eps_h=1, font_eps_v=1)
result = converter.convert()
print(result["graphs"][0].out_edges(keys=True, data=True))
