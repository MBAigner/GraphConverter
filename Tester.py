from GraphConverter import GraphConverter
from util import constants
from util import StorageUtil

# test file
pdf = "eu-001.pdf"
file = constants.PDF_PATH + pdf

# convert PDF
converter = GraphConverter(file)
result = converter.convert_graph()
print(result)