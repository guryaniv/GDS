# In order to use this code you must have Kaggle credentials set up.
# Follow instruction at: https://github.com/Kaggle/kaggle-api#api-credentials
import time
import os
import kaggle

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
# Check on specific dataset \ competition if its kernels amount is valid (more than 5 notebooks for this dataset).
#`you can change the amount of notebooks manually in the return line
# Inputs:
#   [BOOL] is_comp  - indicates whether the name suggests dataset \ competition
#   [STR]  name     - represents the name of the dataset \ competition.
#   [INT] num - min amount of notebooks per dataset
# Return:
#   [BOOL] - whether dataset \ competition has valid amount of kernels.
def kernels_amount_valid(is_comp, name, num=10):
    total = 0
    if is_comp:
        kernels_c = kaggle.api.kernels_list(competition=name, page_size=100, language='python')
        total = len(kernels_c)
    else:
        kernels_d = kaggle.api.kernels_list(dataset=name, page_size=100, language='python')
        total = len(kernels_d)
    return True if total > num else False


# Description:
#   Writes into datasets list file competitions suffix for later use.
#   Can get optional string for specific competition search.
# Inputs:
#   [STR] search_in - Kaggle api optional value for specific search value. (Same as Kaggle API input)
#   [INT] num - min amount of notebooks per dataset
# Return:
#   Does not return any value.
def get_competitions(search_in=None, num=10):
    # There could be more than 1 page of datasets for a specific search, we search first 30 pages.
    for idx in range(1, 30):
        try:
            comp_arr = kaggle.api.competitions_list(page=idx, search=search_in)
            if len(comp_arr) == 0:
                break
        except:
            print("Exception (Probably too many API requests. sleeping for 30 seconds)")
            # Sleeps in order to "clear" requests.
            time.sleep(30)
            idx -= 1
        print("Found " + str(len(comp_arr)) + " competitions")
        for i, comp in enumerate(comp_arr):
            comp = str(comp)
            # Checks whether the dataset was already viewed (in both valid link and non valid files)
            if is_in_file(comp, consts.DATA_LINKS_NAME) or is_in_file(comp, consts.NOT_VALID_DATA_LINKS_NAME):
                continue
            try:
                # Checks kernels amount value and inserts to links file (or non-valid links file)
                is_valid = kernels_amount_valid(True, comp, num=num)
                if is_valid:
                    print("V - " + str(i) + ": " + comp)
                    write_to_file('/c/' + comp, consts.DATA_LINKS_NAME)
                else:
                    print("X - " + str(i) + ": Not enough notebooks")
                    write_to_file('/c/' + comp, consts.NOT_VALID_DATA_LINKS_NAME)
            except:
                print("Exception (Probably too many API requests. sleeping for 30 seconds)")
                # Sleeps in order to "clear" requests.
                time.sleep(30)
                is_valid = kernels_amount_valid(True, comp, num=num)
                if is_valid:
                    print("V - " + str(i) + ": " + comp)
                    write_to_file('/c/' + comp, consts.DATA_LINKS_NAME)
                else:
                    print("X - " + str(i) + ": Not enough notebooks")
                    write_to_file('/c/' + comp, consts.NOT_VALID_DATA_LINKS_NAME)


# Description:
#   Writes into datasets list file datasets suffix for later use.
#   Can get optional string for specific dataset search.
# Inputs:
#   [STR] search_in - Kaggle api optional value for specific search value. (Same as Kaggle API input)
# Return:
#   Does not return any value.
def get_datasets(search_in=None, num=10):
    # There maybe more than 1 page of datasets for specific search, we search first 30 pages.
    for idx in range(1, 30):
        try:
            ds_arr = kaggle.api.datasets_list(page=idx, search=search_in)
            if len(ds_arr) == 0:
                break
        except:
            print("Exception (Probably too many API requests. sleeping for 30 seconds)")
            # Sleeps in order to "clear" requests.
            time.sleep(30)
            idx -= 1
        print("Found " + str(len(ds_arr)) + " datasets")
        for i, ds in enumerate(ds_arr):
            ds = str(ds)
            # Checks whether the dataset was already viewed (in both valid link and non valid files)
            if is_in_file(ds, consts.DATA_LINKS_NAME) or is_in_file(ds, consts.NOT_VALID_DATA_LINKS_NAME):
                continue
            try:
                # Checks kernels amount value and inserts to links file (or non-valid links file)
                is_valid = kernels_amount_valid(False, ds, num=num)
                if is_valid:
                    print("V - " + str(i) + ": " + ds)
                    write_to_file('/c/' + ds, consts.DATA_LINKS_NAME)
                else:
                    print("X - " + str(i) + ": Not enough notebooks")
                    write_to_file('/c/' + ds, consts.NOT_VALID_DATA_LINKS_NAME)
            except:
                print("Exception (Probably too many API requests. sleeping for 30 seconds)")
                # Sleeps in order to "clear" requests.
                time.sleep(30)
                is_valid = kernels_amount_valid(False, ds, num=num)
                if is_valid:
                    print("V - " + str(i) + ": " + ds)
                    write_to_file('/c/' + ds, consts.DATA_LINKS_NAME)
                else:
                    print("X - " + str(i) + ": Not enough notebooks")
                    write_to_file('/c/' + ds, consts.NOT_VALID_DATA_LINKS_NAME)


# Description:
#   Writes into datasets list file dataset name.
# Inputs:
#   [STR] name - name of dataset \ competition.
# Return:
#   Does not return any value.
def write_to_file(name, file):
    try:
        with open(file, "a+") as f:
            f.write(name)
            f.write("/\n")
    except:
        os.mkdir(consts.ASSETS_FOLDER)
        with open(file, "a+") as f:
            f.write(name)
            f.write("/\n")


# Description:
#   Writes into datasets list file dataset name.
# Inputs:
#   [STR] name - name of dataset \ competition.
# Return:
#   Does not return any value.
def is_in_file(name, file):
    try:
        if name in open(file).read():
            return True
        return False
    except:
        return False


# Description:
#   Wrapper function for get_datasets and get_competitions.
# Inputs:
#   [STR] search - Kaggle api optional value for specific search value. (Same as Kaggle API input)
#   [BOOL] comp - Whether to use get_competitions or not.
#   [BOOL] ds - Whether to use get_datasets or not.
#   [INT] num - min amount of notebooks per dataset
# Return:
#   Does not return any value.
def get_kaggle_metadata(search=None, comp=True, ds=True, num=10):
    if comp:
        get_competitions(search, num)
    if ds:
        get_datasets(search, num)


