import os
import csv

# importing modules from the same directory is different between systems and python versions
try:
    import data_gathering.consts as consts
    print("consts imported")
except:
    try:
        import consts as consts
        print("consts imported")
    except:
        try:
            from .consts import consts as consts
            print("consts imported")
        except:
            try:
                from data_gathering import consts as consts
                print("consts imported")
            except:
                print("couldn't import consts")

# DATA_SETS_FILE_PATH = os.path.join(consts.DATA_FOLDER, 'DataSets.csv')


# Description:
#   Get all the values in order to create a row in the dataset TSV file for each dataset.
# Inputs:
#   [STR] ds_path - the path of specific dataset.
# Return:
#   [LIST] - list of the values of each column in the dataset row
def get_ds_table_elem(ds_path):
    os.chdir(ds_path)
    res = []
    res.append(os.path.basename(ds_path))

    for i, filename in enumerate([consts.descFileName, consts.evalFileName, consts.tagsFileName, consts.overFileName]):
        res.append(get_file_data(ds_path, filename))
    return res


# Description:
#   Get data from a TXT file which will be put into a specific column.
# Inputs:
#   [STR] curr_dir_path - the path of specific dataset.
#   [STR] filename      - the name of which file the function will read.
# Return:
#   [STR] - the text inside filename after removing special chars.
def get_file_data(curr_dir_path, filename):
    filePath = os.path.join('', filename)
    if os.path.exists(filePath):
        with open(os.path.join(curr_dir_path, filename), 'r', encoding="utf-8") as f:
            data = f.read()
            data = data.replace("\n", "")
            data = data.replace("\r", "")
            data = data.replace("\t", "")
        return data


# Description:
#   Iterates all datasets and reads each one metadatas in order to build a TSV table of all the datasets.
# Inputs:
#   This function does not get an inputs.
# Return:
#   This function does not return any values.
#   Note - the function creates a TSv file under the name of <consts.DS_TSV>
def generate_ds_tsv():
    ds_path = consts.DATASETS
    tsv_table = []
    for dataSet in os.listdir(ds_path):
        if os.path.isfile(os.path.join(ds_path, dataSet)):
            continue
        tsv_table.append(get_ds_table_elem(os.path.join(ds_path, dataSet)))

    try:
        with open(consts.DS_TSV, 'w', encoding="utf-8", newline='') as csvFile:
            tsv_writer = csv.writer(csvFile, quotechar='"', quoting=csv.QUOTE_MINIMAL, delimiter='\t')
            tsv_writer.writerow(['Names', 'Desc', 'Eval', 'Tag', 'Over'])
            [tsv_writer.writerow(row) for row in tsv_table if any(row)]
    except:
        os.mkdir(consts.DATA_FOLDER)
        with open(consts.DS_TSV, 'a+', encoding="utf-8", newline='') as csvFile:
            tsv_writer = csv.writer(csvFile, quotechar='"', quoting=csv.QUOTE_MINIMAL, delimiter='\t')
            tsv_writer.writerow(['Names', 'Desc', 'Eval', 'Tag', 'Over'])
            [tsv_writer.writerow(row) for row in tsv_table if any(row)]
    print("Done, Saved at", consts.DS_TSV)
