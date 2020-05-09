import re
import pandas as pd
from inspect import getmembers, isfunction, isclass

global global_df

###################
# Init copy of df #
###################
global_df = pd.read_csv('input/cells.tsv', delimiter='\t', encoding='utf-8')
global_df = global_df[global_df["Source"].isnull() == False]
global_df = global_df[global_df["Source"] != ""]
global_df.dropna()
global_df = global_df[global_df["Source"].isnull() == False]
global_df = global_df[global_df["Cell ID"].isnull() == False]
global_df.drop_duplicates(inplace=True)


####################
# Helper functions #
####################
def getPreCellSource(c, n):
    try:

        id = c.cell.stable_id
        exec_indx = id.rfind("_#_")
        exec_count = id[exec_indx + 3:]
        new_exec = int(exec_count) - n
        if new_exec > 0:
            new_id = c.cell.stable_id[0:-1] + str(new_exec)
            source = global_df[global_df["Cell ID"] == new_id]["Source"].iloc[0]
        return source
    except:
        return ""

def getLibRegex(lib_name):
    functions_list = [o[0] for o in getmembers(lib_name) if isfunction(o[1]) or isclass(o[1])]
    regex = '(?<!import)(=|\(|\.)('
    for item in functions_list:
        if item[0] == "" and item[-1] == "":
            continue
        regex += " ?" + item + "|"
    regex = regex[0:-1]
    regex += ")"
    return regex


#############
# Load Data #
#############
def LF_Read(c):
    READ_RGX = r'read_csv\(|read_table\(|Reader\('
    cells = c.cell
    matches = re.search(READ_RGX, cells.text)
    return 'Load Data' if matches else None


################
# Prep & Clean #
################

# Hopefully this LF will get small weight and it will affect in scenarios that no other LF fits.
def LF_Def(c):
    DEF_RGX = r'def \S+\(.*\):'
    cells = c.cell
    matches = re.search(DEF_RGX, cells.text)
    return 'Prep & Clean' if matches else None

def LF_Concat(c):
    CONCAT_RGX = r'\.concat|\.copy|\.replace|\.insert|\.sample|\.shuffle|shuffle\(|\.append|\.astype'
    cells = c.cell
    matches = re.search(CONCAT_RGX, cells.text)
    return 'Prep & Clean' if matches else None

def LF_Split(c):
    SPLIT_RGX = r'train_test_split\('
    cells = c.cell
    matches = re.search(SPLIT_RGX, cells.text)
    return 'Prep & Clean' if matches else None


def LF_Drop(c):
    Drop_RGX = r'\.drop|\.dropna'
    cells = c.cell
    matches = re.search(Drop_RGX, cells.text)
    return 'Prep & Clean' if matches else None

def LF_Fill(c):
    Fill_RGX = r'\.fill|\.random'
    cells = c.cell
    matches = re.search(Fill_RGX, cells.text)
    return 'Prep & Clean' if matches else None


def LF_Nulls(c):
    Null_RGX = r'isnull|fillna|notna|notnull'
    cells = c.cell
    matches = re.search(Null_RGX, cells.text)
    return 'Prep & Clean' if matches else None

def LF_Loc(c):
    LOC_RGX = r'\.loc\[|\.iloc\[|\.at\[|\.iat\[|\.rename|\.where'
    cells = c.cell
    matches = re.search(LOC_RGX, cells.text)
    return 'Prep & Clean' if matches else None

def LF_Transformions(c):
    token_list = ['Binarizer', 'FunctionTransformer', 'KBinsDiscretizer', 'KernelCenterer',
                  'LabelBinarizer', 'LabelEncoder', 'MultiLabelBinarizer', 'MaxAbsScaler',
                  'MinMaxScaler', 'Normalizer', 'OneHotEncoder', 'OrdinalEncoder',
                  'PolynomialFeatures', 'PowerTransformer', 'QuantileTransformer',
                  'RobustScaler', 'StandardScaler', 'binarize', 'TfidfVectorizer']
    TRANSFORM_RGX = '(?<!import)(=|\(|\.)('
    for item in token_list:
        if item[0] == "" and item[-1] == "":
            continue
        TRANSFORM_RGX += " ?" + item + "|"
    TRANSFORM_RGX = TRANSFORM_RGX[0:-1]
    TRANSFORM_RGX += ")"
    cells = c.cell
    matches = re.search(TRANSFORM_RGX, cells.text)
    return 'Prep & Clean' if matches else None

def LF_TransformOps(c):
    TRANSFORMOPS_RGX = r'\.scale|power_transform|\.transform|\.fit_transform|\.fit_sample'
    cells = c.cell
    matches = re.search(TRANSFORMOPS_RGX, cells.text)
    return 'Prep & Clean' if matches else None


def LF_TxtEncode(c):
    TXT_ENCD_RGX = r'\.Word2Vec|word2vec|(?<!nltk\.)corpus'
    cells = c.cell
    matches = re.search(TXT_ENCD_RGX, cells.text)
    return 'Prep & Clean' if matches else None

def LF_Token(c):
    TOEKN_RGX = r'Tokenizer|\.texts_to_sequences|\.fit_on_texts'

import sklearn.feature_extraction as f_e
def LF_sklearn_f_e(c):
    RGX = getLibRegex(f_e)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Prep & Clean' if matches else None

import sklearn.feature_selection as f_s
def LF_sklearn_f_s(c):
    RGX = getLibRegex(f_s)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Prep & Clean' if matches else None

import sklearn.impute as impute
def LF_sklearn_impute(c):
    RGX = getLibRegex(impute)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Prep & Clean' if matches else None

import sklearn.preprocessing as sklearn_p_p
def LF_sklearn_p_p(c):
    RGX = getLibRegex(sklearn_p_p)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Prep & Clean' if matches else None


#################
# Train & Param #
#################

def LF_Models(c):
    MODELS_RGX = r'(?<!import)(=|\(|\.)(' \
                 ' ?Model| ?CatBoostClassifier| ?LinearRegression| ?LogisticRegression| ?KFold| ?xgb| ?Sequential| ?RandomForestClassifier)'
    cells = c.cell
    matches = re.search(MODELS_RGX, cells.text)
    return 'Train & Param' if matches else None


def LF_Train(c):
    TRAIN_RGX = r'\.fit\(|\.train|epoch|\.compile'
    cells = c.cell
    matches = re.search(TRAIN_RGX, cells.text)
    return 'Train & Param' if matches else None


def LF_Optimize(c):
    OPTIMIZE_RGX = r'\.optimise'
    cells = c.cell
    matches = re.search(OPTIMIZE_RGX, cells.text)
    return 'Train & Param' if matches else None


def LF_Params(c):
    PARAMS_RGX = r'learning_rate ?= ?|nthread ?= ?|max_bin ?= ?|ntrees ?= ?|model_id ?= ?|(\s|\\n|\')seed ?= ?|iterations ?= ?|' \
                 'batch_size ?= ?|training_dropout ?= ?|training_epochs ?= ?|n_samples ?= ?|display_step ?= ?|' \
                 'optimizer ?= ?|metrics ?= ?|loss ?= ?|softmax|\.dropout|num_rounds ?= ?|max_samples ?= ?|' \
                 'n_neighbors ?= ?|step ?= ?|loss ?= ?\'mean_squared_error\'|\'eval_metric\'|\'max_depth\''
    cells = c.cell
    matches = re.search(PARAMS_RGX, cells.text)
    return 'Train & Param' if matches else None


import sklearn.cluster as cluster


def LF_sklearn_cluster(c):
    RGX = getLibRegex(cluster)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Train & Param' if matches else None


import sklearn.linear_model as sklearn_l_m


def LF_sklearn_l_m(c):
    RGX = getLibRegex(sklearn_l_m)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Train & Param' if matches else None


import sklearn.ensemble as ensemble


def LF_sklearn_ensemble(c):
    RGX = getLibRegex(ensemble)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Train & Param' if matches else None


import sklearn.mixture as mixture


def LF_sklearn_mixture(c):
    RGX = getLibRegex(mixture)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Train & Param' if matches else None


import sklearn.neighbors as neighbors


def LF_sklearn_neighbors(c):
    RGX = getLibRegex(neighbors)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Train & Param' if matches else None


import sklearn.neural_network as sklearn_n_n


def LF_sklearn_n_n(c):
    RGX = getLibRegex(sklearn_n_n)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Train & Param' if matches else None


import sklearn.svm as svm


def LF_sklearn_svm(c):
    RGX = getLibRegex(svm)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Train & Param' if matches else None


import sklearn.tree as sklearn_tree


def LF_sklearn_tree(c):
    RGX = getLibRegex(sklearn_tree)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Train & Param' if matches else None


# import h2o.estimators as estimators
def LF_h2o_estimators(c):
    token_list = ['H2OGradientBoostingEstimator', 'H2ODeepLearningEstimator', 'H2ODeepWaterEstimator', 'H2OGeneralizedLinearEstimator', 'H2ONaiveBayesEstimator',
                  'H2ORandomForestEstimator', 'H2OStackedEnsembleEstimator', 'H2OXGBoostEstimator', 'H2OAggregatorEstimator', 'H2OAutoEncoderEstimator',
                  'H2OGeneralizedLowRankEstimator', 'H2OIsolationForestEstimator', 'H2OKMeansEstimator', 'H2OPrincipalComponentAnalysisEstimator',
                  'H2OAutoML', 'H2OEstimator', 'H2OGridSearch', 'H2OSingularValueDecompositionEstimator', 'H2OWord2vecEstimator']
    H2O_RGX = '(?<!import)(=|\(|\.)('
    for item in token_list:
        if item[0] == "" and item[-1] == "":
            continue
        H2O_RGX += " ?" + item + "|"
    H2O_RGX = H2O_RGX[0:-1]
    H2O_RGX += ")"
    cells = c.cell
    matches = re.search(H2O_RGX, cells.text)
    return 'Train & Param' if matches else None

########
# Eval #
########


PREDICT_RGX = r'\.predict'
SCORE_RGX = r'score\(|f1_score\(|accuracy\(|recall\(|precision\(|confusion|cnf_matrix'
EVAL_RGX = r'\.model_performance|\.eval'
ERROR_RGX = r'mean_absolute_error\(|mean_squared_error\(|rms|mse'
ALL_EVAL_RGX = PREDICT_RGX + "|" + SCORE_RGX + "|" + EVAL_RGX + "|" + ERROR_RGX


def LF_Predict(c):
    cells = c.cell
    matches = re.search(PREDICT_RGX, cells.text)
    return 'Eval' if matches else None


def LF_Score(c):
    cells = c.cell
    matches = re.search(SCORE_RGX, cells.text)
    return 'Eval' if matches else None


def LF_Eval(c):
    cells = c.cell
    matches = re.search(EVAL_RGX, cells.text)
    return 'Eval' if matches else None


def LF_Error(c):
    cells = c.cell
    matches = re.search(ERROR_RGX, cells.text)
    return 'Eval' if matches else None

def LF_Curves(c):
    CURVE_PLT_RGX = r'roc_curve|auc\(|[^\']AUC[^\']|roc_auc_curve'
    cells = c.cell
    matches = re.search(CURVE_PLT_RGX, cells.text)
    return 'Eval' if matches else None

import sklearn.metrics as metrics
def LF_sklearn_metrics(c):
    RGX = getLibRegex(metrics)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Eval' if matches else None


###########
# Explore #
###########
def LF_Sizes(c):
    READ_RGX = r'read_csv|read_table'
    SIZES_RGX = r'\.shape|\.value_counts' #|len\('
    cells = c.cell
    matches = re.search(SIZES_RGX, cells.text)
    is_read = re.search(READ_RGX, cells.text)
    if matches:
        if is_read:
            return 'Load Data'
        else:
            return 'Explore'
    else:
        return None


def LF_Explore(c):
    LOAD_RGX = r'read_csv\(|read_table\(|Reader\('
    EXPLORE_RGX = r'\.head|\.unique|\.heatmap|\.tail|\.info|\.describe|\.median|\.sum\(\)|\.min\(\)'
    cells = c.cell
    is_load = re.search(LOAD_RGX, cells.text)
    if is_load:
        return None # 'Load Data'
    else:
        is_eval = re.search(ALL_EVAL_RGX, cells.text)
        if is_eval:
            return None # 'Eval'
        else:
            matches = re.search(EXPLORE_RGX, cells.text)
            return 'Explore' if matches else None


def LF_Plotting(c):
    PLOT_RGX = r'plo?t\S*\(|\.hist'
    cells = c.cell
    is_plot = re.search(PLOT_RGX, cells.text)
    is_eval = re.search(ALL_EVAL_RGX, cells.text)
    if is_plot:
        if is_eval:
            return None # 'Eval'
        else:
            pre = getPreCellSource(c, 1)
            is_pre_eval = re.search(ALL_EVAL_RGX, pre)
            if is_pre_eval:
                return 'Eval'
            return 'Explore'
    else:
        return None


import sklearn.covariance as covariance


def LF_sklearn_covariance(c):
    RGX = getLibRegex(covariance)
    cells = c.cell
    matches = re.search(RGX, cells.text)
    return 'Explore' if matches else None


##########
# Import #
##########


def LF_Import(c):
    IMPORT_RGX = r'import '  # Added space after import to avoid "importance"
    cells = c.cell
    matches = re.search(IMPORT_RGX, cells.text)
    return 'Import' if matches else None


LFs_Load = [LF_Read]
LFs_Prep = [LF_Def, LF_Concat, LF_Split, LF_Drop, LF_Fill, LF_Nulls, LF_Loc, LF_Transformions, LF_TransformOps, LF_TxtEncode, LF_Token, LF_sklearn_f_e, LF_sklearn_f_s ,LF_sklearn_impute ,LF_sklearn_p_p]
LFs_Train = [LF_Models, LF_Train, LF_Optimize, LF_Params, LF_sklearn_cluster, LF_sklearn_l_m,
             LF_sklearn_ensemble, LF_sklearn_mixture, LF_sklearn_neighbors,
             LF_sklearn_n_n, LF_sklearn_svm, LF_sklearn_tree, LF_h2o_estimators]
LFs_Eval = [LF_Predict, LF_Score, LF_Eval, LF_Error, LF_Curves, LF_sklearn_metrics]
LFs_Explore = [LF_Explore, LF_Sizes, LF_Plotting, LF_sklearn_covariance]
LFs_Import = [LF_Import]



