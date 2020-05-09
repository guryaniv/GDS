import ast
import re
import codecs


# Description:
#   Get the text code of a cell and returns it masked format and ast format (tuple)
#   It is also updates and maintains the trans_dict
# Inputs:
#   [STR]  cell_text  - string that represents the cell code.
#   [DICT] trans_dict - translation dictionary of variable and modules names. Should be created with init_trans_dict()
# Return:
#   ([STR], [STR]) - tupple which contains the AST format as its first value and the masked format as its second one.
def mask_source(cell_text, trans_dict):
    # Checks if the cell is a list of lines, if so joins them
    if isinstance(cell_text, list):
        cell_text = "".join(cell_text)
    try:
        if cell_text is None:
            return "", ""
        # Checks the cell unicode
        if "\n" not in cell_text:
            if "\n" in codecs.decode(cell_text, 'unicode_escape'):
                cell_text = codecs.decode(cell_text, 'unicode_escape')

        # Checks for special first lines in the cell and remoces them
        cell_text = cell_text.replace("%matplotlib inline", "")
        cell_text = cell_text.replace("%%time", "")
        tree = ast.parse(cell_text)
        ast_txt = str(ast.dump(tree))
    except Exception as e:
        if cell_text is None:
            print("TypeError in cell - 'None'")
            if e is TypeError:
                print("TypeError in cell - \n")
            else:
                print("Error in cell - \n" + cell_text)
        print("Error is - " + str(e))
        return "", ""
    node_append_counter = 0
    new_cell = ""
    # Traversing the AST of the cell, checking the instance of each node
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            continue

        if isinstance(node, ast.Assign) or isinstance(node, ast.Expr):
            module = ""
            var = ""
            parsed = ""

            try:
                # If instance is Assign, it converts the variable to numbered one via the trans_dict.
                if isinstance(node, ast.Assign):
                    var_orig = node.targets[0].id
                    if var_orig in trans_dict.keys():
                        var = trans_dict[var_orig]
                    else:
                        var_cnt = trans_dict["___var_counter"]
                        var = "var" + str(var_cnt)
                        trans_dict["___var_counter"] = (var_cnt + 1)
                        trans_dict.update({var_orig: var})

                    module_as = node.value.func.value.id
                    module = trans_dict[module_as]
                    if var is not "":
                        parsed = var + "="
                else:
                    # This instance is Expr
                    var_orig = node.value.func.value.id
                    if var_orig in trans_dict:
                        var = trans_dict[var_orig]
                    else:
                        var = var_orig
                    parsed = var + "."
                func = node.value.func.attr
                # We are numbering multiple 'add' or 'append' in the same cell, to force each one equal weights.
                if func == "add":
                    try:
                        layer = node.value.args[0].func.id
                        func += "_" + layer.lower()
                    except:
                        layer = ""
                if func == "append":
                    func += "_" + str(node_append_counter)
                    node_append_counter += 1
                if module is not "":
                    parsed += module + "."
                parsed += func + " "
                new_cell += parsed
            except:
                try:
                    func = node.value.value.attr
                    new_cell += func + " "
                except:
                    continue
        # Import instances are converted to 'import_<module_name>' with no alias names.
        # It will re-converted to its original form via trans_dict
        if isinstance(node, ast.Import):
            for alias in node.names:
                new_cell += "import_" + alias.name + " "

    return ast_txt, new_cell


# Description:
#   Get the text code of a cell and parses each import line form it
#   Inserts it to trans_dict for later use in mask_source.
# Inputs:
#   [STR]  source     - string that represents the cell code.
#   [DICT] trans_dict - translation dictionary of variable and modules names. Should be created with init_trans_dict()
# Return:
#   None - this function does not return any value.
def parse_imports_to_trans_dict(source, trans_dict):
    source = source.replace("\"", "")
    source = source.replace("'", "")

    # Workaround since sometimes breaklines are \\\\n and sometimes \\n
    source = source.replace("\\\\n", "\\n")
    source = source.replace("\\\\r", "\\r")

    lines = re.split("\\n|\\r", source)
    for line in lines:
        if "import" in line:
            if "as" in line:
                words = line.split(" ")
                if words[0] is "":
                    words = words[1:]
                orig = words[1].replace("\"", "")
                orig = orig.replace("\'", "")
                target = words[3].replace("\"", "")
                target = target.replace("\'", "")

                trans_dict.update({target: orig})


# Description:
#   Search a dict object by a value and not by key.
# Inputs:
#   [DICT] dic   - dict object which is wished to search a value from it.
#   [STR]  value - string that represents the value you wished to search.
# Return:
#   [STR] - return the first key that points to 'value'. If no key found returns None
def dict_search_key(dic, value):
    for key, val in dic.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if val == value:
            return key
    return None


# Description:
#   Gets a masked format of a cell with its corresponding trans_dict and returns it to its original form.
# Inputs:
#   [STR]  mask       - string that represents the masked format of a cell code.
#   [DICT] trans_dict - translation dictionary of variable and modules names. Should be created with init_trans_dict()
# Return:
#   [STR] - original cell code of the masked format.
def unmask_source(mask, trans_dict):
    # Splits the masked format by " " to get each token
    tokens = mask.split(" ")
    unmask = ""
    # Clears any empty items
    tokens = list(filter(lambda a: a != "", tokens))
    for token in tokens:
        # For each token it may be one of three types: import, assign, expression
        if "import_" in token:  # import line - splits the '_' and gets any aliases
            mod = token.replace("import_", "")
            mod_as = dict_search_key(trans_dict, mod)
            if mod_as is None:
                unmask += "import " + mod + "\n"
            else:
                unmask += "import " + mod + " as " + mod_as + "\n"
            continue

        if "=" in token:  # assign line - gets the original variables and modules names from trans_dict
            var_m = token[:token.find("=")]
            var_u = dict_search_key(trans_dict, var_m)
            if var_u is None:
                var_u = var_m
            exp = token[token.find("=") + 1:]
            if "." not in exp:
                unmask += var_u + " = " + exp + "\n"
                continue
            mod = exp[:exp.find(".")]
            mod_as = dict_search_key(trans_dict, mod)
            if mod_as is None:
                mod_as = mod
            func = exp[exp.find(".") + 1:]
            unmask += var_u + " = " + mod_as + "." + func + "\n"
        elif "." in token:  # expression line - - gets the original variables and modules names from trans_dict
            var_m = token[:token.find(".")]
            var_u = dict_search_key(trans_dict, var_m)
            if var_u is None:
                var_u = var_m
            func = token[token.find(".") + 1:]
            unmask += var_u + "." + func + "\n"
        else:
            # Defualt case if any error occurred, gets the last variable inside trans_dict as the variable name
            last_var_cnt = trans_dict["___var_counter"] - 1
            var_u = dict_search_key(trans_dict, "var" + str(last_var_cnt))
            unmask += var_u + "." + token + "\n"
    unmask = unmask[:-1]
    return unmask


# Description:
#   Creates an empty defaulted trans_dict to be used with any other functions in this module.
# Inputs: No inputs values
# Return:
#   [DICT] - returns clear dict with special key initialized as the variable counter
def init_trans_dict():
    return {"___var_counter": 0}


# Full usage flow:
# If source is given in variable named 'src'
#   1. Initiate translation dictionary
#   2. Parse all import module to alias names
#   3. Convert source into masked representation
#
# If given masked output and you wish to unmask it use to following command.
# (NOTE: second variable is FULL translation dict - mask_source fills it up)
#   1. Unmask to masked source


# src = "import numpy as np\nimport pandas as pd\ndf = pd.read_csv('t.txt')\nsubm = pd.DataFrame()\n" \
#       "subm['Id'] = id_test\nsubm['Predicted'] = np.argmax(preds, axis=1)\nsubm.to_csv('submission.csv', index=False)"
# tran_dict = init_trans_dict()
# parse_imports_to_trans_dict(src, tran_dict)
# mask = mask_source(src, tran_dict)[1]
#
# mask = "import_numpy import_pandas var0=pandas.read_csv var1=pandas.DataFrame var1.to_csv "
# unmask = unmask_source(mask, tran_dict)
