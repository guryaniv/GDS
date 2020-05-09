import csv
import json
import os
import ast

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
try:
    from data_gathering.masking import mask_source, parse_imports_to_trans_dict
except:
    try:
        from masking import mask_source, parse_imports_to_trans_dict
    except:
        print("Could not import 'masking'")


# Get the text code of a cell and return striped from quotes and special whitespace chars
# Inputs:
#       [STR] source - the source text of a cell
# Return:
#       [STR] - stripped format of the source, removing quotes and whitespaces
def strip_clean_source(source):
    if source[0] == '\"' and source[-1] == '\"':
        source = source[1:-1]
    if source[0] == '\'' and source[-1] == '\'':
        source = source[1:-1]
    source_clean = source.replace("\\n", " ")
    source_clean = source_clean.replace("\n", " ")
    source_clean = source_clean.replace("\\r", " ")
    source_clean = source_clean.replace("\r", " ")
    source_clean = source_clean.replace("\\t", " ")
    source_clean = source_clean.replace("\t", " ")
    return source_clean


# Extract the dataset name of a dataset path by finding the last slash in the path
# Inputs:
#       [STR] path - the path of a dataset
# Return:
#       [STR] - only the name of the dataset from the path
def get_ds_from_path(path):
    last_slash = path.rfind("\\")
    return path[last_slash+1:]


# Iterates over all datasets directory, for each dataset it iterates over its kernels,
# And for each kernels it iterates over its entire cells.
# For each cell it calculates unique ID (username, notebook name, cell execution count).
# It also generates other fields (execution count, AST, mask, etc...) and insert to TSV.
# In order to create the masked representation of a cell please see more details inside 'masking.py'
# NOTE: this function creates 2 TSV files (NB_TSV, CELLS_TSV)
# Inputs:
#       This function does not require any inputs.
#       [INT] earlystop - if you want to stop creating the tsvs after a specific number of notebooks
#                         set earlystop accordingly
# Return:
#       This function does not return any value.
#       It creates 2 external files for other uses.
def generate_nb_tsv(earlystop=None):
    # Setting a list of all the datasets
    ds_arr = []
    ds_path = consts.DATASETS
    for folder in os.listdir(ds_path):
        if os.path.isdir(os.path.join(ds_path, folder)):
            ds_arr.append(os.path.join(ds_path, folder))
    total_cells = 0
    total_nb = 0
    print("Loading datasets from: ", ds_path)
    # Creating 2 TSV file pointers.
    with open(consts.NB_TSV, mode="w", encoding="utf-8") as csvNBFile:
        with open(consts.CELLS_TSV, mode="w", encoding="utf-8") as csvCellFile:
            # Setting up header row in both TSV
            csvNBWriter = csv.writer(csvNBFile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvNBWriter.writerow(["Score", "Username", "Notebook name", "Dataset"])
            csvCellWriter = csv.writer(csvCellFile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvCellWriter.writerow(["Cell ID", "User Name", "Notebook name", "Source", "Output", "Execution count", "Masked", "AST", "Label"])
            # Iterating each dataset for the list
            for i, folder in enumerate(ds_arr):
                print(i, "--- Start with", folder, "\n")
                k_folder = os.path.join(folder, "kernels")
                if os.path.exists(k_folder):
                    # Iterating each kernel of the dataset
                    for nb_num, file in enumerate(os.listdir(k_folder)):
                        if os.path.isfile(os.path.join(k_folder, file)):
                            try:
                                # Extracting metadata from the file name
                                score = file.split("---")[0]
                                user = file.split("---")[1]
                                name = file.split("---")[2]
                                ds_name = get_ds_from_path(folder)
                                # Write a row inside NB_TSV
                                csvNBWriter.writerow([score, user, name, ds_name])
                                file_path = os.path.join(k_folder, file)
                                # Starting to read the kernel cells
                                print("Starting notebook", nb_num, file)
                                # Reads the cell and convert it into JSON object.
                                with open(file_path, encoding="utf-8") as f:
                                    data = json.load(f)
                                    cells = data["cells"]
                                    print("Found", len(cells), "cells")
                                    exec = 1
                                    # Setting translation dict for masking purposes.
                                    nb_tran_dict = {"___var_counter": 0}
                                    # Iterates the cells of the kernels
                                    for cell in cells:
                                        # Making sure it is code cell.
                                        if cell["cell_type"] == "code":
                                            raw_source = cell["source"]

                                            source = repr(raw_source)
                                            # Sometimes cells become list of lines, in that case we join them.
                                            if source[0] == "[":
                                                source_list = ast.literal_eval(source)
                                                source = repr(" ".join(source_list))

                                            parse_imports_to_trans_dict(source, nb_tran_dict)
                                            source = strip_clean_source(source)
                                            # Getting cell representations (masking, AST)
                                            try:
                                                ast_tree, funcs = mask_source(raw_source, nb_tran_dict)
                                                outputs = cell["outputs"]

                                                # Not used, we simulate it by counting execution count by ourselves.
                                                exec_count = cell["execution_count"]
                                                id = user + "_#_" + name + "_#_" + str(exec)

                                                # Write cell row into CELLS_TSV
                                                csvCellWriter.writerow([id, user, name, source, outputs, exec, funcs, ast_tree, ""])
                                                exec += 1
                                            # In case of an error we skip.
                                            except SyntaxError as e:
                                                continue
                                    print("Finished notebook number", nb_num, " - with total cells of", exec)
                                    # Counters maintenance
                                    total_nb += 1
                                    total_cells += exec
                                    if earlystop != None:
                                        if total_nb == earlystop:
                                            return
                                    print("So far gathered", total_cells, "of cells")

                            # In case of an early error we print for debug purposes.
                            except (IndexError, UnicodeDecodeError, json.JSONDecodeError) as e:
                                print(str(nb_num) + "  Error in notebook: " + file)
                                print("Error is: " + str(e))

    print("\n\nFound " + str(total_cells) + " cells out of " + str(total_nb) + " notebooks, from a total of " + str(i) + " datasets")
    print("Done.")
