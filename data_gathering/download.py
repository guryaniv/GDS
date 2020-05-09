# -*- coding: utf-8 -*-

# In order to use this code you must have Kaggle credentials set up.
# Follow instruction at: https://github.com/Kaggle/kaggle-api#api-credentials

from selenium import webdriver
import time
import os
import html2text
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
#   Read link suffix from external text file into list.
# Return:
#   [LIST] - contains Kaggle dataset links.
def read_links():
    with open(consts.DATA_LINKS_NAME, "r") as f:
        lines = f.read().split('\n')
        lines.remove('')
        links = list(map(lambda suffix: "https://www.kaggle.com" + suffix, lines))
        return links


# Description:
#   Gets the name of the dataset\competition from its link. Subtracts it from the URL.
# Inputs:
#   [STR] link - Kaggle dataset link.
# Return:
#   ([STR], [BOOL]) - tupple which contains the dataset name and boolean indicates whether it is a competition.
def get_name(link):
    is_competition = link.find('/c/')
    if -1 == is_competition:
        slash_start = link.find('/', 23)
        slash_end = link.find('/', slash_start+1)
        name = link[slash_start+1: slash_end]
        return name, False
    else:
        slash_start = 25
        slash_end = link.find('/', slash_start + 1)
        name = link[slash_start: slash_end]
        return name, True


# Description:
#   Login into Kaggle account on stops all active notebooks. (Kaggle limits the number of active notebook sessions).
#   To close any recent active notebooks we simulating closing each one.
# Return:
#   Does not return.
def stop_notebooks():
    print("Starting to stop notebooks")
    link = "https://www.kaggle.com/tamirhuber/kernels"
    xpath = "//a[text()='Stop']"
    stop_browser = login(link, "stam_folder")
    list_stop = stop_browser.find_elements_by_xpath(xpath)
    for stop in list_stop:
        stop.click()
        time.sleep(1)
    time.sleep(5)
    stop_browser.close()
    print("Stopped all notebooks, sleeping for 5 seconds")
    time.sleep(5)


# Description:
#   Login into kaggle account on opens a browser. Also sets the download path for that browser.
#   It uses pre-defined Username and password that may be modified in consts file.
# Inputs:
#   [STR] link           - Kaggle dataset link. for example - https://www.kaggle.com/jessevent/all-crypto-currencies/
#   [STR] kernels_folder - Dataset name to set relevant folder as download path. for example - 'all-crypto-currencies'.
#                          The folder download path will be CWD/datasets/<kernels_folder>
# Return:
#   [WebDriver] - class provided by selenium package, the WebDriver is opened on the dataset link.
def login(link, kernels_folder):
    options = webdriver.ChromeOptions()
    download_path = os.path.join(consts.DATASETS, kernels_folder)
    print("Chrome will save to - " + download_path)
    options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False
    })

    browser = webdriver.Chrome(executable_path=consts.CHROME_WEBDRIVER_PATH,
                               chrome_options=options)
    print("Opening " + link)
    # Opens the provided link
    browser.get(link)
    # Locating sign-in button
    sign_in = browser.find_element_by_id("sign-in-button")
    time.sleep(1)
    # Clicking sign-in button
    sign_in.click()
    time.sleep(2)
    # click sign in using with your email (to use username and password)
    using = browser.find_element_by_link_text("Sign in with your email");
    # using = browser.find_element_by_xpath("//a[//text()='Sign in with your email']")
        # "//div[class='LoginRegisterStyles_FullPageContent-sc-1iu1e3x dErhIX']"
        # "//div[class='LoginRegisterStyles_SocialButtons-sc-1ul1coh emCnbm']"
        # "/a[class='LoginRegisterStyles_SignInOrRegisterIconButton-sc-18qv3mq iAOZbU'][position()=2]")
    using.click()
    time.sleep(5)
    # Locating username and password text fields. Also the submit button
    user = browser.find_element_by_id("username-input-text")
    pwd = browser.find_element_by_id("password-input-text")
    submit = browser.find_element_by_id("submit-sign-in-button")
    # Entering username and password
    user.send_keys(consts.KAGGLE_USER)
    pwd.send_keys(consts.KAGGLE_PW)
    time.sleep(2)
    # Clicking submit
    submit.click()
    time.sleep(2)
    print("Browsing again to requested link (After login may site may redirect)")
    # Kaggle may redirect, so we re-open the original link.
    browser.get(link)
    return browser


# Description:
#   Scroll the browser until no more kernels can be found, at the end scrolls all the way up.
#   Used mainly to load more kernels at kernels page.
# Inputs:
#   [WebDriver] browser - class provided by selenium package that is opened on the dataset's kernels page.
# Return:
#   Does not return.
def scroll_browser(browser):
    # Try to locate message indicates there are no more kernels.
    msg = browser.find_elements_by_class_name("smart-list__message")
    m_inner = msg[0].get_attribute("innerHTML")
    scrolls = 0
    try:
        # While no that message is found we scroll to bottom of the page.
        while m_inner.find("No more kernels to show") == -1 and scrolls < 30:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            # Try to locate message indicates there are no more kernels.
            msg = browser.find_elements_by_class_name("smart-list__message")
            m_inner = msg[0].get_attribute("innerHTML")
            scrolls += 1
        # When we finished to scroll down we scroll back up.
        browser.execute_script("window.scrollTo(0, 0);")
        time.sleep(3)
    except:  # Handles script execution error
        print("Error in Scrolling")


# Description:
#   Strips the score value from string which is WebElement object (Div).
# Inputs:
#   [STR] div_text - string which is WebElement object (Div).
# Return:
#   [STR] - The score of that notebook, if an error occurs returns "NULL".
def get_score_from_div(div):
    # Gets the HTML text from div element
    html_text = div.text
    h = html2text.HTML2Text()
    text = h.handle(html_text)
    score = (str(text))
    # Checks that the score is proper float number
    try:
        float(score)
        return score.strip()
    except ValueError:
        return "NULL"


# Description:
#   Get all the kernels links from a dataset page.
#   This is the only way to get the actual link for each link which is a must in order to use the Kaggle API.
#   Those links will be saved in 'LINKS_TSV' files and will be used in pull_kernels().
# Inputs:
#   [STR] kaggle_link - The dataset kaggle page link.
#   [STR] ds_name - Only the dataset name which is the sub-folder to save the kernels.
#   [BOOL] is_comp - True if the dataset is competition.
# Return:
#   [INT] - The amount of kernels found.
def get_kernels_links(kaggle_link, ds_name, is_comp):
    # Opens WebDriver and logs in into kaggle kernels page.
    browser = login(kaggle_link, ds_name)
    # Scrolls to load all kernels.
    scroll_browser(browser)
    score = "NULL"
    try:
        # Getting all kernels links.
        kernel_list = browser.find_elements_by_class_name("block-link__anchor")
        kernels_num = len(kernel_list)
        print("Found total of " + str(kernels_num) + " kernel links")
        # If it is a competition we try to get the score of each kernel.
        if is_comp:
            scores_list = browser.find_elements_by_class_name("kernel-list-item__score")
            scores_num = len(scores_list)
        # Iterating each link to get score again (if first method did not work)
        for i, link in enumerate(kernel_list):
            nb_path = link.get_attribute("href")[len("https://www.kaggle.com/"):]
            if is_comp:
                if i >= scores_num:
                    score = "NULL"
                else:
                    try:
                        score = get_score_from_div(scores_list[i])
                    except:
                        print("Error trying accessing kernel score, setting NULL")
                        score = "NULL"
            else:
                score = "-"
            # Setting up link as <dataset_name>\t<kernel_link>\t<score>
            line = ds_name + "\t" + nb_path + "\t" + score + "\n"
            # Writes each link in external file.
            with open(consts.LINKS_TSV, "a+") as f:
                f.write(line)
    except:
        print("Error listing kernels")
    browser.close()
    return kernels_num


# Description:
#   Accept the competition rules automatically. Sometimes the user have to agree to the competition rules.
# Inputs:
#   [OBJ] data_browser - Selenium browser object with relevant page.
# Return:
#   Does not return a value
def comp_accept_rules(data_browser):
    # Locating rules tab
    rules_btn = data_browser.find_element_by_id('pageheader-nav-item--rules')
    rules_btn.click()
    time.sleep(1)
    # Locating the accept-rules button
    accept_btn = data_browser.find_elements_by_class_name('competition-rules__accept')
    if len(accept_btn) > 0:
        accept_btn[0].click()
        time.sleep(3)
    # Going back to overview tab
    overview_btn = data_browser.find_element_by_id('pageheader-nav-item--overview')
    overview_btn.click()
    time.sleep(3)


# Description:
#   Get description data of a competition from its Kaggle page.
# Inputs:
#   [OBJ] data_browser - Selenium browser object with relevant page.
# Return:
#   [STR] - The string of the description section of the dataset.
def comp_get_desc(data_browser):
    # Going to 'Description' tab.
    desc_btn = data_browser.find_element_by_id('pageheader-nav-item--description')
    time.sleep(5)
    desc_btn.click()
    time.sleep(1)
    # Locating the text element and convert the HTML to text.
    text_elem = data_browser.find_elements_by_class_name('markdown-converter__text--rendered')
    html_text = text_elem[0].text
    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(html_text)
    print("Got competition description")
    return str(text)


# Description:
#   Get evaluation data of a competition from its Kaggle page.
# Inputs:
#   [OBJ] data_browser - Selenium browser object with relevant page.
# Return:
#   [STR] - The string of the evaluation section of the dataset.
def comp_get_eval(data_browser):
    # Going to 'Evaluation' tab.
    desc_btn = data_browser.find_element_by_id('pageheader-nav-item--evaluation')
    desc_btn.click()
    time.sleep(1)
    # Locating the text element and convert the HTML to text.
    text_elem = data_browser.find_elements_by_class_name('markdown-converter__text--rendered')
    html_text = text_elem[0].text
    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(html_text)
    print("Got competition evaluation")
    return str(text)


# Description:
#   Get overview data of dataset from its Kaggle page.
# Inputs:
#   [OBJ] data_browser - Selenium browser object with relevant page.
# Return:
#   [STR] - The string of the overview section of the dataset.
def dataset_get_overview(data_browser):
    # Locating the text element and convert the HTML to text.
    text_elem = data_browser.find_elements_by_class_name('markdown-converter__text--rendered')
    html_text = text_elem[0].text
    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(html_text)
    print("Got dataset overview")
    return str(text)


# Description:
#   Get relevant data from dataset page, either it is a dataset or a competition.
# Inputs:
#   [STR] data_link - full link for the dataset
#   [STR] name - name of the dataset
#   [BOOL] is_comp - True if it is a competition, False otherwise.
# Return:
#   [BOOL] - True if the function was able to start download the data.
def get_data(data_link, name, is_comp=True):
    print("Getting data from " + data_link)
    meta_link = data_link
    # Setting up the metadata link of the dataset
    if is_comp is False:
        meta_link += "/home"
    data_browser = login(meta_link, name + "\\input")
    # if it is a competition we will accept the rules.
    if is_comp:
        comp_accept_rules(data_browser)
    try:
        # Try to get the dataset tags.
        tags_elements = data_browser.find_elements_by_xpath("//a[contains(@href, '/tags/')]")
        tags = list(map(lambda x: x.text, tags_elements))
        # Setting up the folder in which the metadata will be saved.
        metadata_folder = consts.CWD + "\\datasets\\" + name + "\\"
        if not os.path.isdir(metadata_folder):
            os.mkdir(metadata_folder)
        # Writing the tags into txt file
        with open(metadata_folder + "tags.txt", "w+") as f_tags:
            print(tags)
            f_tags.write(str(tags))
    except:
        consts.log_error("error_creating_tags_file_under: " + metadata_folder)
    # Getting dataset metadata overview / (description, evaluate)
    if is_comp:
        try:
            # Getting description and saves into desc.txt
            data_desc = comp_get_desc(data_browser)
            with open(metadata_folder + "desc.txt", "w+", encoding="utf-8") as f_desc:
                f_desc.write(data_desc)
        except:
            consts.log_error("error_creating_desc_file_under: " + metadata_folder)
        try:
            # Getting evaluation and saves into desc.txt
            data_eval = comp_get_eval(data_browser)
            with open(metadata_folder + "eval.txt", "w+", encoding="utf-8") as f_eval:
                f_eval.write(data_eval)
        except:
            consts.log_error("error_creating_eval_file_under: " + metadata_folder)
    else:
        try:
            # Getting overview and saves into desc.txt
            data_over = dataset_get_overview(data_browser)
            with open(metadata_folder + "over.txt", "w+", encoding="utf-8") as f_over:
                f_over.write(data_over)
        except:
            consts.log_error("error_creating_over_file_under: " + metadata_folder)
    # Closing the browser...
    data_browser.close()
    time.sleep(1)

    # # # NOTE NOTE NOTE # # #
    # The following code snnipet is used to download the dataset actual datasets.
    # Those files may be big / compressed and the section is known to be not stable.
    # We did not found any other way to get those files, and since it is only a handful number of datasets,
    # we completed any missing one manually.

    # Opens new browser with the dataset date.
    # The actual data, the datasets, tsv, csv and any other file which is provided by kaggle.
    data_browser = login(data_link + "/data", name + "\\input")
    try:
        # Try to click 'Download All'
        download_data = data_browser.find_element_by_xpath("//span[text()='Download All']")
        time.sleep(3)
        download_data.click()
        time.sleep(3)
        time.sleep(5)
        print("Downloading " + name + " - Browser will remain open")
        return True
    except:
        # In case of an error the code will sleep for 100, so there is enough time to debug.
        # After that time the browser page will be closed to save computer CPU.
        print("Can not find download button, sleeps 100 secs for debugging")
        time.sleep(100)
        data_browser.close()
        return False


# Description:
#   Checks if a folder for datasets does exist.
# Inputs:
#   [STR] name - name of dataset
# Return:
#   [BOOL] - True if a folder exist, False otherwise.
def does_exist(name):
    download_path = consts.DATASETS + name
    exists = os.path.isdir(download_path)
    return exists


# Description:
#   Wrapper function of all the above ones.
#   For each dataset link that found link_list it will download relevant data (input, description, evaluation, etc...)
#   It also get the links to each of dataset's kernels so we could pull them later on, and write them in TXT file.
# Inputs:
#   [LIST] link_list - list of datasets link
#   [BOOL] stop_np - if True at the begging of the run it will stop any active notebooks on kaggle.
#   [INT] earlystop - if you want to stop after a specific number of datasets, set earlystop accordingly
# Return:
#   Does not return. NOTE: It uses get_kernel_links which write to an outer file.
def download_data_and_kernels_link(link_list, stop_nb=False, earlystop=None):
    print("Got total of " + str(len(link_list)) + " datasets")
    dup = 0
    total_nb = 0
    # Iterating each link (dataset) found in link list.
    for j in range(0, len(link_list)):
        if earlystop != None:
            if earlystop == j:
                return
        print("Starting with dataset " + str(j+1))
        dataset_name, is_comp = get_name(link_list[j])
        print("Dataset name is " + dataset_name)
        if does_exist(dataset_name):
            print("Dataset already downloaded")
            print("Dataset already downloaded")
            dup += 1
            print("So far found " + str(dup) + " duplicates datasets")
        else:
            if stop_nb:
                stop_notebooks()
            # Gets the actual link of the dataset.
            data_link = link_list[j][0: link_list[j].find(dataset_name) + len(dataset_name)]
            # Get dataset metadata.
            get_data(data_link, dataset_name, is_comp)
            # Setting up the kernel link of the dataset (Varies between competition and regular dataset)
            if is_comp:
                kernel_link = link_list[j] + "kernels?sortBy=scoreDescending&group=everyone&pageSize=20" \
                                             "&language=Python&kernelType=Notebook"
            else:
                kernel_link = link_list[j] + "kernels?sortBy=voteCount&group=everyone&pageSize=20" \
                                             "&language=Python&kernelType=Notebook"
            # Gets the dataset kernels and saves it into external TXT file for later use.
            total_nb += get_kernels_links(kernel_link, dataset_name, is_comp)
        print("Done with dataset " + str(j+1))
        print("So far total notebooks is: " + str(total_nb))
        print("- - - - - - - - - -\n\n")


# Description:
#   Pulling all relevant kernels from earlier function to local machine, the flow is as follow:
#   Open the TXT file to get links for kernels (which was build in earlier functions),
#   then uses Kaggle API to pull them locally.
#   This function maintains several external TXT file, in case of crush you can re-run it and it will continue last run.
#   NOTE: To use Kaggle API you must have Kaggle credentials set up.
#   Follow instruction at: https://github.com/Kaggle/kaggle-api#api-credentials
# Inputs:
#   The function doesn't require any input to run (downloads notebooks that appear in outer list file).
#   @earlystop - if you want to stop downloading after a specific number of notebooks set earlystop accordingly.
# Return:
#   Does not return any value.
def pull_kernels(earlystop = None):
    # Counters
    pulled = 0
    skipped = 0
    # Creating list of any know invalids kernels, in order to skip them
    try:
        with open(consts.NOT_VALID_KERNELS, "r") as f:
            not_valid = f.read().split('\n')
    except:
        open(consts.NOT_VALID_KERNELS, "a+")
        not_valid = []
    # Creating list of all the kernels
    with open(consts.LINKS_TSV, "r") as f:
        lines = f.read().split('\n')
        try:
            lines.remove('')
        except ValueError:
            print("Did not found empty line")

        # Iterating all links, split the link from its name and dataset name
        for kernel in lines:
            ds_name = kernel.split("\t")[0]
            path = kernel.split("\t")[1]
            # Checks if the link is known as invalid.
            if path in not_valid:
                print(path + " was checked before and is not valid | skipping...")
                continue
            score = kernel.split("\t")[2]
            if score == "-":
                score = "X"
            user = path.split("/")[0]
            nb = path.split("/")[1]
            # Creating kernels file name as the convention.
            new_file_name = score + "---" + user + "---" + nb + ".ipynb"
            old_file_name = nb + ".ipynb"
            ds_folder = os.path.join(consts.DATASETS, ds_name)
            location = os.path.join(ds_folder, "kernels")
            # If relevant dataset folder does not exist it will create it.
            if not os.path.exists(ds_folder):
                os.mkdir(ds_folder)
            if not os.path.exists(location):
                os.mkdir(location)
            # If file already exist it will skip it
            if os.path.exists(os.path.join(location, new_file_name)):
                continue
            # Trying to pull the kernel - There are several known exceptions we will handle.
            try:
                kaggle.api.kernels_pull(kernel=path, path=location)
            # Any case of special character raise exception - Japanese for example.
            # In this case the kernel becomes invalid and loop will continue.
            except UnicodeEncodeError:
                print("encoding error with - " + kernel + "  | skipping...")
                with open(consts.NOT_VALID_KERNELS, "a+") as f_nvd:
                    f_nvd.write(path + "\n")
                continue
            # Any other exception may result of several issues,
            # so we sleep (sometimes Kaggle blocks it due to flood of requests) and tries again.
            except:
                try:
                    print("*** SHORT SLEEP ***")
                    time.sleep(10)
                    kaggle.api.kernels_pull(kernel=path, path=location)
                # In case of 2nd error for the kernel we insert it to invalid kernel list.
                # We also keeps tracks of the unknown error kernels so it can be reviewed later
                except Exception as e:
                    print("2nd unknown error with - " + kernel + "  | skipping...")
                    skipped += 1
                    with open(consts.UNKNOWN_ERRORS, "a+") as f_ue:
                        f_ue.write(path + "\n")
                    with open(consts.NOT_VALID_KERNELS, "a+") as f_nvd:
                        f_nvd.write(path + "\n")

                        # Every 13 kernels that we skipped we sleep a little longer to prevent Kaggle from blocking us.
                        if skipped % 13 == 0:
                            print("*** SLEEPS ***")
                            time.sleep(20)
                    continue
            # After pulling a kernels we renaming it to support our naming convention.
            # Sometimes error occur while pulling kernel and it is not exist, so we use try-excpet
            try:
                os.rename(os.path.join(location, old_file_name), os.path.join(location, new_file_name))
                pulled += 1
                print(str(pulled) + " - Done with notebook: " + nb)

                if earlystop != None:
                    if pulled == earlystop or skipped == earlystop:
                        return

                # Every 13 successfully pulled kernels we sleep a little longer to prevent Kaggle from blocking us.
                if pulled % 13 == 0:
                    print("*** SLEEPS ***")
                    time.sleep(15)

            except FileNotFoundError:
                print("file not found error with - " + os.path.join(location, old_file_name))
                with open(consts.NOT_VALID_KERNELS, "a+") as f_nvd:
                    f_nvd.write(path + "\n")


