from GraphConverter import GraphConverter
from util import constants

# test file
pdf = "eu-001.pdf"
file = constants.PDF_PATH + pdf

# convert PDF
converter = GraphConverter(file)
result = converter.convert()
print(result["graphs"][0].out_edges(keys=True, data=True))
