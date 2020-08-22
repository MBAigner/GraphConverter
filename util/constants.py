# store/load
LOAD_OCR = True
STORE_CSV = False
LOAD_CSV = not STORE_CSV
STORE_GRAPH = False
LOAD_GRAPH = not STORE_GRAPH
STORE_CLUSTERS = False
LOAD_CLUSTERS = not STORE_CLUSTERS
STORE_CLASSIFICATION_RESULTS = True

# text box transformation
MERGE_RECTANGLE_TEXT_BOXES = False
USE_RECTANGLE_BOX_COORDINATES = False

# paths
OCR_PATH = "../converted_data/ocr/"
CSV_PATH = "../converted_data/csv/"
GRAPH_PATH = "../converted_data/graph/"
CLUSTER_PATH = "../converted_data/clustered/"
MODEL_PATH = "../models/"

# data sets
TABLEBANK = "tablebank"
ICDAR = "icdar"

# document meta calculations
OPTIMIZE = True

# classification set preparation
USE_COMPLETE_TABLES_FOR_TRAINING_DATA = False
IN_BOX_TOLERANCE = 5

# base classifier thresholds
BASELINE_THRESHOLD = 1
BASELINE_TOLERANCE = 0.75
RECTANGLE_TOLERANCE = 0.4
LOOP_TOLERANCE = .4
SPARSITY_RELATIVE_DIFF_THRESHOLD = .1

# merge settings
HORIZONTAL_MERGE_THRESHOLD = 20
VERTICAL_MERGE_THRESHOLD = 20
WEAK_MERGE = True
HORIZONTAL_WEAK_MERGE_THRESHOLD = HORIZONTAL_MERGE_THRESHOLD
VERTICAL_WEAK_MERGE_THRESHOLD = VERTICAL_MERGE_THRESHOLD

# visibility graph settings
USE_FONT = True
USE_WIDTH = True
USE_RECT = True
# overlap settings
USE_HORIZONTAL_OVERLAP = False
USE_VERTICAL_OVERLAP = False
HORIZONTAL_OVERLAP_THRESHOLD = 0.3
VERTICAL_OVERLAP_THRESHOLD = 0.7

# clustering settings
USE_LEV_DISTANCE = False
USE_GOWER_DISTANCE = not USE_LEV_DISTANCE
USE_TEXT = True
USE_FONT_DIST = True
USE_TOKENS = True
USE_LOOPS = True

# weigthing
TOKEN_WEIGHT = 1
LOOP_WEIGHT = 1
FONT_WEIGHT = 3
LEV_DIST_WEIGHT = 1
HORIZONTAL_SCALING = 0  # 0.001
DIAGONAL_SCALING = 0  # 0.001

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

# pdf miner layout analysis parameters
USE_CUSTOM_PDF_PARAMETERS = True
DEFAULT_DETECT_VERTICAL = True
DEFAULT_LINE_OVERLAP = 0.5
DEFAULT_LINE_MARGIN = 0.15
DEFAULT_WORD_MARGIN = 0.1
DEFAULT_CHAR_MARGIN = 0.5
DEFAULT_BOXES_FLOW = 0.5

# parameter regression
TRAINING_SET = TABLEBANK
N_TRAINING_SAMPLES = 1000
REGRESS_GRAPH_PARAMETERS = False

# pre-classification
CLASSIFY_TEXT = True
CLASSIFY_LIST = True
CLASSIFY_PLOT = False
FLOAT_EPS = .001

# classifier
MULTIMODAL_CLASSIFIER = "multimodal"
MULTIMODAL_CLASSIFIER_MODEL = "decision_tree_tablebank"
LOOP_CLASSIFIER = "loop"
BASELINE_CLASSIFIER = "baseline"
SPARSITY_CLASSIFIER = "sparsity"
VISUAL_CLASSIFIER = "visual"
ENSEMBLE_CLASSIFIER = "ensemble"
ENSEMBLE_CANONICALS = [LOOP_CLASSIFIER, SPARSITY_CLASSIFIER, MULTIMODAL_CLASSIFIER]
CLASSIFIER = LOOP_CLASSIFIER

# labeling
LABEL_INPUT_PATH = "../main/input/"
PDF_LABEL_INPUT_PATH = "../../data/custom/pdfs/"
LABEL_OUTPUT_PATH = "../main/output/YOLO_darknet/"
LABELED_DATA_FILE_PATH = PDF_LABEL_INPUT_PATH
LABELED_DATA_FILE_EXT = "pdf"
