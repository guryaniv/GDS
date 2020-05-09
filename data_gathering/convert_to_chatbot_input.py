import pandas as pd
import pickle

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



# Description:
#   Gets a CSV, removes any duplicates and saves it as a new file.
#   Note - it should be used on CSV of format ["Line", "Next"], as we used eventually in the project.
# Inputs:
#   [STR]  in_file - path that points to the input CSV file.
#   [DICT] output  - path that points to the output CSV file.
# Return:
#   This function does not return any value
def keep_unique_pairs(in_file, output):
    df = pd.read_csv(in_file, sep="\t", header=None, names=["Line", "Next"])
    total = len(df)
    df.drop_duplicates(['Line', 'Next'], inplace=True)
    filtered = len(df)
    print("Filtered duplicates, pairs remaining:", filtered*100/total, "%")
    df.to_csv(output, sep='\t')


# Description:
#   In the formation of lines and not cells (line-next),
#   there are many duplicates sources that followed by large variety of different 'nexts'.
#   This function keeps only the 'n_keep' nexts and removes any non-frequent ones to converge the results.
# Inputs:
#   [DATAFRAME] df - dataframe object with the pairs of source-next.
#   [STR] src_name - the column name of the source of the pairs.
#   [STR] next_name - the column name of the next (2nd element) of the pairs.
#   [INT] n_keep - the amount of next to keep, for example if equal 3 it will keep only the 3 most frequent nexts.
#   [BOOL] logs - if True it will print extensive logs, default value is False.\
# Return:
#   [DATAFRAME] - dataframe object after filtering any non-frequent pairs.
def keep_freq_couples(df, src_name, next_name, n_keep, logs=False):
    dup = df[df.duplicated([src_name], keep=False)]
    dup = dup.sort_values(src_name, ascending=False)
    dup = dup.reset_index(drop=True)
    # Count the different sources.
    cnt = dup.groupby([src_name]).size().reset_index(name='count')
    cnt = cnt.sort_values('count', ascending=False)
    cnt = cnt.reset_index(drop=True)
    out = pd.DataFrame(columns=[src_name, next_name])
    total = len(cnt)
    print("Found diffrent sources of:", total)
    for j, row in enumerate(cnt.iterrows()):
        if not logs:
            if total // 100 > 0:
                if (j % (total // 100)) == 0:
                    print(str(j * 100 // total) + "%")

        txt = row[1][0]
        nexts = df[df[src_name] == txt]
        # Counts the nexts
        cnt2 = nexts.groupby([next_name]).size().reset_index(name='count')
        cnt2 = cnt2.sort_values('count', ascending=False)
        cnt2 = cnt2.reset_index(drop=True)

        to_keep = []
        for i, row2 in enumerate(cnt2.iterrows()):
            if i == n_keep:
                break
            to_keep.append(row2[1][0])
        temp = df[(df[src_name] == txt) & (df[next_name].isin(to_keep))]
        out = out.append(temp)
        if logs:
            print("Iteration", i, "out of", total)
            print("For source:", txt, "Found a total nexts of:", len(nexts))
            print("Different next amount is:", len(cnt2), "will keep -", len(temp))
            print("---------------------\n")

    print("Done. Kept:", (len(out) / len(df) * 100), "%")
    return out


# Description:
#   Converts from CSV of cells to CSV of lines, splitting each cell to its lines.
#   The format is 3-lines followed by the next one. For first lines it maybe 1/2 lines followed by the next one.
#   There are 2 modes - Save or Load, in load mode it uses saved file to speed up time.
#   It needs to merge all cells of the same notebook in order to convert to line format
#   it saves each merged notebook for loading.
# Inputs:
#   [BOOL] load - if True it will try to load pre-saved,
#   otherwise it will run all function and save the files for later. Default value is True.
#   [INT] earlystop - if you want to stop creating the pairs after a specific number of notebooks
#                     set earlystop accordingly
#   [BOOL] ptg - if true will show progress percentage (not needed for small amount)
# Return:
#   This function does not return any values.
def cells_to_masked_lines(load=True, earlystop=None, ptg=True):
    if load:
        # Try to load pre-saved files
        with open(consts.NB_LINES_TXT, "rb") as f_lines:  # Unpickling
            nbs = pickle.load(f_lines)
        with open(consts.NB_LABELS_TXT, "rb") as f_labels:  # Unpickling
            labels = pickle.load(f_labels)
        print("Loaded notebook and labels lists")
        print("Notebooks size is", len(nbs))
        print("Labels list size is", len(labels))
        if len(nbs) != len(labels):
            print("Error in loading lists from files. Changing to 'Save Mode'")
            load = False
    if not load:
        # Not load mode, will run all code segments and will save files.
        df = pd.read_csv(consts.TAGGED_CELLS_TSV, delimiter='\t')
        df.head()
        mask = df.drop(['Notebook name', 'Cell ID', 'User Name', 'Output', 'Source', 'AST'], axis=1)
        nbs = []
        labels = []
        mask = mask[mask["Masked"] != "NB_END"]
        total = len(mask)
        nb_lines = []  # For each notebook each item in the list is a line-code
        nb_labels = []  # Each item is the line label, indexing is important to tie each line with its label.
        for index, row in enumerate(df.iterrows()):
            if ptg:
                if index % (total//100) == 0:
                    print(str(1+(100*index//total)) + "%")
            if (index + 1) == len(mask):
                nbs.append(nb_lines)
                labels.append(nb_labels)
                nb_lines = []
                nb_labels = []
                continue
            if mask.at[index+1, "Execution count"] == 1:
                nbs.append(nb_lines)
                labels.append(nb_labels)
                nb_lines = []
                nb_labels = []
            else:
                n_mask = mask.at[index+1, "Masked"]
                n_lbl = mask.at[index+1, "Label"]
                if not pd.isna(n_mask):
                    n_lines = n_mask.split(" ")
                    n_lines = list(filter(lambda a: a != "", n_lines))
                    n_len = len(n_lines)
                    n_labels = [n_lbl] * n_len
                    nb_lines.extend(n_lines)
                    nb_labels.extend(n_labels)

        print("Saving notebook and labels lists...")
        print("Notebooks size is", len(nbs))
        print("Labels list size is", len(labels))

        with open(consts.NB_LINES_TXT, "wb") as f_lines:  # Pickling
            pickle.dump(nbs, f_lines)
        with open(consts.NB_LABELS_TXT, "wb") as f_labels:  # Pickling
            pickle.dump(labels, f_labels)

    print("Total", len(nbs), "notebooks")
    
    # Clearing existing files
    with open(consts.LOAD_TSV, "w+") as load_f:
        load_f.write("")
    with open(consts.PREP_TSV, "w+") as prep_f:
        prep_f.write("")
    with open(consts.EXPLORE_TSV, "w+") as exp_f:
        exp_f.write("")
    with open(consts.IMPORT_TSV, "w+") as imp_f:
        imp_f.write("")
    with open(consts.TRAIN_TSV, "w+") as tra_f:
        tra_f.write("")
    with open(consts.EVAL_TSV, "w+") as eval_f:
        eval_f.write("")

    # Each label has its own buffer, lines will be concatenated to existing buffer until overflow.
    # When buffer is overflowing it will be printed to file and start over.
    buffers = ["", "", "", "", "", ""]
    label_index = ["Load", "Prep", "Train", "Eval", "Explore", "Import"]
    files_index = [consts.LOAD_TSV, consts.PREP_TSV, consts.TRAIN_TSV, consts.EVAL_TSV, consts.EXPLORE_TSV, consts.IMPORT_TSV]

    for nb_idx, note in enumerate(nbs):
        if earlystop != None:
            if earlystop == nb_idx:
                print("Earlystopping...")
                return
        print("Starts with notebook number - ", nb_idx+1)
        if len(note) == 0:
            continue
        lines = list(filter(lambda a: a != "", note))
        lines_label = labels[nb_idx]
        for line_num, line in enumerate(lines):
            curr_label = lines_label[line_num]
            buffer_ind = label_index.index(curr_label)
            curr_buffer = buffers[buffer_ind]
            if line_num + 1 == len(lines):
                break
            if line_num == 0:
                write = lines[0] + '\t' + lines[1]
            elif line_num == 1:
                write = lines[0] + " " + lines[1] + '\t' + lines[2]
            else:
                write = lines[line_num-2] + " " + lines[line_num-1] + " " + lines[line_num] + '\t' + lines[line_num+1]
            curr_buffer += write + '\n'
            if len(curr_buffer) > 50000:
                print("Writing length of buffer " + curr_label + " is too big - ", len(curr_buffer))
                print("Writing into file and resets the buffer")
                with open(files_index[buffer_ind], "a+") as file:
                    file.write(curr_buffer)
                curr_buffer = ""
            buffers[buffer_ind] = curr_buffer

    # Going over buffers and print any remains the txt files.
    for buf_ind, buf in enumerate(buffers):
        if buf == "":
            continue
        with open(files_index[buf_ind], "a+") as file:
            print("Clearing any remains inside buffer -" + str(label_index[buf_ind]) + ". Remaining length is" + str(len(buf)))
            file.write(buf)


# Description:
#   Creates a CSV file of masked pairs of cells from the main cells CSV file.
#   It may use labeled cell CSV or none labeled, it also enables to save all the unique pairs.
# Inputs:
#   [STR] label - if None it uses non tagged CSV file of cells. Otherwise it uses the pairs of that specific label only.
#   [STR] file  - the path of the output file, default is consts.MASKED_TSV
#   [BOOL] unique  - if True it also create file that keeps all the unique paris.
#   [BOOL] ptg - if true will show progress percentage (not needed for small amount)
# Return:
#   This function does not return any values.
def cells_to_masked_pairs(label=False, file=consts.MASKED_TSV, unique=True, ptg=True):
    if label is None:
        df = pd.read_csv(consts.CELLS_TSV, delimiter='\t')
    else:
        df = pd.read_csv(consts.TAGGED_CELLS_TSV, delimiter='\t')
    print("Starts with", len(df))
    df = df[True != pd.isna(df["Cell ID"])]
    df = df.reset_index()
    print("After initial cleaning", len(df))

    mask = df.drop(['Notebook name', 'Cell ID', 'User Name', 'Output', 'Source', 'AST'], axis=1)
    mask["Next masked"] = ""

    total = len(mask)

    for index, row in enumerate(df.iterrows()):
        if ptg == True:
            if index % (total//100) == 0:
                print(str(1+(100*index//total)) + "%")
        if (index + 1) == len(mask):
            mask.at[index, "Next masked"] = "NB_END"
            continue
        if mask.at[index+1, "Execution count"] == 1:
            mask.at[index, "Next masked"] = "NB_END"
        else:
            n = mask.at[index+1, "Masked"]
            mask.at[index, "Next masked"] = n

    print("Cells number before cleaning:", len(mask))
    mask = mask[True != pd.isna(mask["Masked"])]
    mask = mask[True != pd.isna(mask["Next masked"])]
    mask = mask[mask["Next masked"] != "NB_END"]

    # Filter specific label
    if label is not None:
        print("Before filtering by label - total cells was", len(mask))
        mask = mask[mask["Label"] == label]

    print("Cells number after cleaning:", len(mask))
    mask.drop(mask.columns.difference(['Masked', 'Next masked']), 1, inplace=True)

    if unique:
        uni = mask.drop_duplicates(subset=["Masked", "Next masked"])
        print(len(uni)/len(mask), "% - Are left in unique pairs dataset")
        uni.to_csv(file[:-4] + "_unique.tsv", sep='\t', index=False)


# Description:
#   Creates a CSV file of AST pairs of cells from the main cells CSV file.
#   Note, it has less option since it was used and deprecated. We moved on with mask form.
# Inputs:
#   This function does not use any inputs.
# Return:
#   This function does not return any values.
def cells_to_ast_pairs():
    df = pd.read_csv(consts.CELLS_TSV, delimiter='\t')
    df.head()
    ast = df.drop(['Notebook name', 'Cell ID', 'User Name', 'Output', 'Label', 'Source', 'Masked'], axis=1)

    ast["Next AST"] = ""
    for index, row in enumerate(df.iterrows()):
        if (index + 1) == len(ast):
            ast.at[index, "Next AST"] = "NB_END"
            continue
        if ast.at[index+1, "Execution count"] == 1:
            ast.at[index, "Next AST"] = "NB_END"
        else:
            n = ast.at[index+1, "AST"]
            ast.at[index, "Next AST"] = n

    print("Cells number before cleaning:", len(ast))
    ast = ast[True != pd.isna(ast["AST"])]
    ast = ast[True != pd.isna(ast["Next AST"])]
    ast = ast[ast["Next AST"] != "NB_END"]
    print("Cells number after cleaning:", len(ast))

    ast = ast.drop(['Execution count'], axis=1)
    ast = keep_freq_couples(ast, "AST", "Next AST", 3)
    ast.to_csv(consts.AST_TSV, sep='\t', index=False)


# Description:
#   Creates a CSV file of source pairs of cells from the main cells CSV file.
#   Note, it has less option since it was used and deprecated. We moved on with mask form.
# Inputs:
#   This function does not use any inputs.
# Return:
#   This function does not return any values.
def cells_to_source_pairs():
    df = pd.read_csv(consts.CELLS_TSV, delimiter='\t')
    df.head()
    source = df.drop(['Notebook name', 'Cell ID', 'User Name', 'Output', 'Label', 'AST', 'Masked'], axis=1)

    source["Next Source"] = ""
    for index, row in enumerate(df.iterrows()):
        if (index + 1) == len(source):
            source.at[index, "Next Source"] = "NB_END"
            continue
        if source.at[index+1, "Execution count"] == 1:
            source.at[index, "Next Source"] = "NB_END"
        else:
            n = source.at[index+1, "Source"]
            source.at[index, "Next Source"] = n

    print("Cells number before cleaning:", len(source))
    source = source[True != pd.isna(source["Source"])]
    source = source[True != pd.isna(source["Next Source"])]
    source = source[source["Next Source"] != "NB_END"]
    print("Cells number after cleaning:", len(source))

    source = source.drop(['Execution count'], axis=1)
    source = keep_freq_couples(source, "Source", "Next Source", 3)
    source.to_csv(consts.SOURCE_TSV, sep='\t', index=False)
