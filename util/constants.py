# text box transformation
MERGE_RECTANGLE_TEXT_BOXES = False
USE_RECTANGLE_BOX_COORDINATES = False

# paths
OCR_PATH = "../converted_data/ocr/"
CSV_PATH = "../converted_data/csv/"
GRAPH_PATH = "../converted_data/graph/"
CLUSTER_PATH = "../converted_data/clustered/"
MODEL_PATH = "../models/"

# document meta calculations
OPTIMIZE = True

# visibility graph settings
USE_FONT = True
USE_WIDTH = True
USE_RECT = True
USE_HORIZONTAL_OVERLAP = False
USE_VERTICAL_OVERLAP = False
HORIZONTAL_OVERLAP_THRESHOLD = 0.3
VERTICAL_OVERLAP_THRESHOLD = 0.7

# visibility graph parameters
DEFAULT_PAGE_RATIO_X = 1.9
DEFAULT_PAGE_RATIO_Y = 20
DEFAULT_X_EPS = 2
DEFAULT_Y_EPS = 2
DEFAULT_X_PHYS = DEFAULT_X_EPS
DEFAULT_FONT_EPS_VERTICAL = 1
DEFAULT_FONT_EPS_HORIZONTAL = DEFAULT_FONT_EPS_VERTICAL
DEFAULT_WIDTH_PCT = .4
DEFAULT_PAGE_WIDTH_EPS = .5
