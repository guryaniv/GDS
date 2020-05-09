import os
import patoolib

############################################# NOTE ###################################################
# This file purpose is to maintain important paths and file name that may be used in several files.  #
# configure tha paths and file names how you'd like, but please notice that in the run process there #
# may be some hard coded paths (if we missed them), so be aware.                                     #
# the file is currently configured to run with new example paths                                     #
# (to not overrun or use existing data).                                                             #
# the original paths that were used are commented                                                    #
# (use them if you wish to run the existing trained models)                                          #
######################################################################################################

# ***** configurations for the downloading process ***** #

# datasets download configurations:

# Kaggle credentials
KAGGLE_USER = "tamirhuber@gmail.com"
KAGGLE_PW = "T@mir1513213"

CWD = os.path.abspath(os.pardir)    # our current working directory

# our assets folder that will contain necessary files for the downloading process
# ASSETS_FOLDER = os.path.join(CWD, "data_gathering", "assests")                           # original path
ASSETS_FOLDER = os.path.join(CWD, "data_gathering", "Example_assets")                      # ***CHANGE HERE*** #

# list of relevant datasets that will be downloaded using "download.py"
DATA_LINKS_NAME = os.path.join(ASSETS_FOLDER, 'data_links.txt')
# list of non-relevant datasets, so we won't search for them again
NOT_VALID_DATA_LINKS_NAME = os.path.join(ASSETS_FOLDER, 'not_data_links.txt')
# webdriver path
CHROME_WEBDRIVER_PATH = os.path.join('driver', 'chromedriver.exe')



# Path for the directory in which all of the datasets, their metadata and notebooks will be saved
# (one folder inside the DATASETS folder for each dataset)
# DATASETS = os.path.join(CWD, "datasets")                                            # original path
DATASETS = os.path.join(CWD, "Example_datasets")                                      # ***CHANGE HERE*** #

# File names for the files that will be created for each dataset we download:
ERROR_LOG = "error_log.txt"         # error log for running notebooks
EXECUTED_FILE = "executed.txt"      # keeps executed notebooks list
TEMP_NB_EXECUTED = "temp_nb.txt"    # temp file for executing notebooks
descFileName = 'desc.txt'           # dataset description
evalFileName = 'eval.txt'           # evaluation method for competitions datasets
tagsFileName = 'tags.txt'           # the dataset's tags
overFileName = 'over.txt'           # additional metadata

LOG_PATH = os.path.join(DATASETS, ERROR_LOG)
TEMP_NB = os.path.join(DATASETS, TEMP_NB_EXECUTED)

# datasets download configurations (download.py):
LINKS_TSV = os.path.join(ASSETS_FOLDER, "links_ds.tsv")                     # notebooks links
UNKNOWN_ERRORS = os.path.join(ASSETS_FOLDER, "unknown_errors.txt")          # notebooks download error log
NOT_VALID_KERNELS = os.path.join(ASSETS_FOLDER, "not_valid_kernels.txt")    # list of invalid notebooks
EXECUTED_DS = os.path.join(ASSETS_FOLDER, EXECUTED_FILE)                    # list of executed notebooks

# ***** configurations for our tsv files ***** #

# the data folder that will contain the tsvs that we work with
# DATA_FOLDER = os.path.join(CWD, "Data")                                                # original path
DATA_FOLDER = os.path.join(CWD, "Example_Data")                                          # ***CHANGE HERE*** #

# Main TSV files path
DS_TSV = os.path.join(DATA_FOLDER, "datasets.tsv")
CELLS_TSV = os.path.join(DATA_FOLDER, "cells.tsv")
# TAGGED_CELLS_TSV = os.path.join(DATA_FOLDER, "tagged_cells.tsv")
# we tagged the original cells.tsv file inplace, you can save in another file and change the paths
TAGGED_CELLS_TSV = CELLS_TSV
NB_TSV = os.path.join(DATA_FOLDER, "notebook.tsv")

# ***** configurations for the classifier ***** #
CLASSIFICATION_FOLDER = os.path.join(CWD, "classification")
# our hand tagged labels location
GOLD_LABELS = os.path.join(CLASSIFICATION_FOLDER, "input", "gold_labels.tsv")           # original path
# the folder in which the trained classifier is saved
# CLASSIFIER = CLASSIFICATION_FOLDER                                                    # original path
CLASSIFIER = os.path.join(CLASSIFICATION_FOLDER, "example_classifier")                  # ***CHANGE HERE*** #


# ***** configurations for the chatbot files and models ***** #

CHATBOT_FOLDER = os.path.join(CWD, "Chatbot")
# folder to save trained chatbot models
# CHATBOT_MODELS_FOLDER = os.path.join(CHATBOT_FOLDER, "Models")                         # original path
CHATBOT_MODELS_FOLDER = os.path.join(CHATBOT_FOLDER, "Example_Models")                   # ***CHANGE HERE*** #



# TSV files for chatbot training:
MASKED_TSV = os.path.join(DATA_FOLDER, "masked.tsv")
LINES_TSV = os.path.join(DATA_FOLDER, "lines.tsv")
AST_TSV = os.path.join(DATA_FOLDER, "ast.tsv")
SOURCE_TSV = os.path.join(DATA_FOLDER, "source.tsv")

# TSV files by class category
EXPLORE_TSV = os.path.join(DATA_FOLDER, "Explore.tsv")
PREP_TSV = os.path.join(DATA_FOLDER, "Prep.tsv")
LOAD_TSV = os.path.join(DATA_FOLDER, "Load.tsv")
TRAIN_TSV = os.path.join(DATA_FOLDER, "Train.tsv")
EVAL_TSV = os.path.join(DATA_FOLDER, "Eval.tsv")
IMPORT_TSV = os.path.join(DATA_FOLDER, "Import.tsv")

# TXT files for 'convert_to_chatbot_input.py'
NB_LINES_TXT = os.path.join(ASSETS_FOLDER, "nb_lines.txt")
NB_LABELS_TXT = os.path.join(ASSETS_FOLDER, "nb_labels.txt")

# our Compressed saved trained chatbot models first file
TRAINED_MODELS_PART1 = os.path.join(CHATBOT_MODELS_FOLDER, "rar", "Trained Models.part01.rar")

# ******** chatbot saved trained models locations ******** #
## these models will be used by the recommendation engine ##
EXPLORE_MODEL = os.path.join(CHATBOT_MODELS_FOLDER, "Explore.tar")
PREP_MODEL = os.path.join(CHATBOT_MODELS_FOLDER, "Prep.tar")
LOAD_MODEL = os.path.join(CHATBOT_MODELS_FOLDER, "Load.tar")
TRAIN_MODEL = os.path.join(CHATBOT_MODELS_FOLDER, "Train.tar")
EVAL_MODEL = os.path.join(CHATBOT_MODELS_FOLDER, "Eval.tar")
IMPORT_MODEL = os.path.join(CHATBOT_MODELS_FOLDER, "Import.tar")

# This function writes logs into external TXT file so it van reviewed later for any insights or debugging
# Since several other function may take time and will be run in the background, it is hard to debug in live.
# Inputs:
#       [STR] msg - the error which should be logged.
# Return:
#       This function does not return any value
def log_error(msg):
    with open(LOG_PATH, "a+") as f:
        f.write(msg)
        f.write("\n")


# This function inserts a sub-path into an existing path. For example for add_sub_folder_to_path('a\b\c.txt', 'sub'),
# We will get back 'a\b\sub\c.txt'
# Inputs:
#       [STR] path - the file path
#       [STR] sub  - the sub-folder name which should be inserted into path.
# Return:
#       [STR] - a new file path after inserting sub into path
def add_sub_folder_to_path(path, sub):
    file_name = os.path.basename(path)
    file_path = path.replace(file_name, "")
    new_path = os.path.join(file_path, sub)
    if not os.path.exists(new_path):
        print(new_path, "is not exists. Creating it...")
        os.mkdir(new_path)
    full_path = os.path.join(new_path, file_name)
    return full_path


# This function unzipping the compressed chatbot model.
# Inputs:
#       Function does not get any inputs
# Return:
#       This function does not return any value
def unrar_trained_models():
    folder = CHATBOT_MODELS_FOLDER
    part1 = TRAINED_MODELS_PART1
    if not os.path.exists(folder):
        print(folder, "does not exists... Creating it now.")
        os.mkdir(folder)

    print("Start to extract multiple rar files, using unrar method on first file -", part1)
    patoolib.extract_archive(part1, outdir=folder)
