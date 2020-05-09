from selenium import webdriver
import os
import time

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
#   Execute all notebooks by browsing to anaconda active localhost server and simulating clicking 'Run All'
# Inputs:
#   [STR] link - the localhost link (with token), you get the link after running 'jupyter notebook' via prompt.
#                local host should run from the main folder of the project
#                For example - http://localhost:8888/?token=c855df1c7f9ac3ed2917a4e0920d3fe32a86523d9de2dec8
#   [INT] to_execute - after that amount of executing datasets (all of the datasets notebooks will be executed)
#                       the code will stop, in order to prevent it from running endlessly. Default value is 3.
# Return:
#   [LIST] - list of the values of each column in the dataset row
def execute_notebooks(link, to_execute=3):
    RUNNING = 0

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False
    })

    loop_size = to_execute + 3
    browsers = [None] * loop_size

    executed = 0
    for j in range(0, loop_size):
        if executed == to_execute:
            print("Done for this run, executed", to_execute, "datasets..")
            break
        browsers[j] = webdriver.Chrome(executable_path=consts.CHROME_WEBDRIVER_PATH, chrome_options=options)
        curr_browser = browsers[j]
        curr_browser.get(link)
        time.sleep(3)
        datasets_folder = curr_browser.find_elements_by_xpath("//span[text()='datasets']")
        datasets_folder[0].click()
        time.sleep(15)
        datasets_list = curr_browser.find_elements_by_class_name("item_link")
        print(datasets_list)
        ds = datasets_list[j]
        if ds.is_displayed() is not True:
            print("inside is_displayed")
            continue
        ds_name = ds.get_attribute("innerText")
        print("ds_name:", ds_name)
        if ds_name == "..":
            continue
        if os.path.isfile(consts.EXECUTED_DS):
            with open(consts.EXECUTED_DS, "w") as f:
                f.write("")
        if ds_name in open(consts.EXECUTED_DS).read():
            print(ds_name, "is inside", consts.EXECUTED_DS)
            continue
        ds.click()
        time.sleep(5)
        ds_folders = curr_browser.find_elements_by_class_name("item_link")
        is_kernels_exist = False
        for folder in ds_folders:
            if ".." in folder.get_attribute("innerHTML"):
                continue
            if "kernels" in folder.get_attribute("innerHTML"):
                folder.click()
                is_kernels_exist = True
                break
        if not is_kernels_exist:
            print("Kernels Folder not exist, skipping", ds_name)
            continue
        time.sleep(3)
    
    
        kernels_num = len(curr_browser.find_elements_by_class_name("item_link"))
        tabs = 1
        for i in range(0, kernels_num):
            try:
                if RUNNING % 4 == 0 and RUNNING > 0:
                    print("Opened 4 new notebooks, sleeps for 400 secs")
                    time.sleep(400)
                ds_kernels = curr_browser.find_elements_by_class_name("item_link")
                kernel = ds_kernels[i]
                kernel_name = kernel.get_attribute("innerText")
                if ".." in kernel.get_attribute("innerHTML"):
                    continue
                if kernel.is_displayed() is not True:
                    continue
                if kernel_name in open(consts.TEMP_NB).read():
                    print(kernel_name, "was executed and marked as TEMP")
                    continue
                print("Starting - ", kernel_name)
                kernel.click()
                time.sleep(3)
                handles = curr_browser.window_handles
                curr_browser.switch_to.window(handles[tabs])
                tabs += 1
                print("Changed window to - ", curr_browser.current_url)
                time.sleep(5)
                print("Sleeping... 5")
                time.sleep(1)
                print("Sleeping... 4")
                time.sleep(1)
                print("Sleeping... 3")
                time.sleep(1)
                print("Sleeping... 2")
                time.sleep(1)
                print("Sleeping... 1")
                time.sleep(1)

                try:
                    kernel_dropdown = curr_browser.find_elements_by_xpath("//a[text()='Kernel']")
                    kernel_dropdown[0].click()
                    restart = curr_browser.find_elements_by_id("restart_run_all")
                    restart[0].click()
                    time.sleep(1)
                    confirm = curr_browser.find_elements_by_xpath("//button[text()='Restart and Run All Cells']")
                    confirm[0].click()
                    print("Restart and running notebook")
                    RUNNING += 1
                    time.sleep(5)
                    print("Waiting...")
                    time.sleep(5)
                    with open(consts.TEMP_NB, "a+") as file:
                        print("Writing current kernel to temp file", kernel_name)
                        file.write(kernel_name + "\n")
                except:
                    print("Error (TYPE 2) occured with kernel number", i, "of DS", ds_name)
                curr_browser.switch_to.window(handles[0])
                print("Done with kernel number", i, "return to kernels folder")
                time.sleep(2)
            except:
                print("Error occured with kernel number", i, "of DS", ds_name)
        with open(consts.EXECUTED_DS, "a+") as file:
            print("Adding DS to completed file", ds_name)
            executed += 1
            file.write(ds_name + "\n")
        with open(consts.TEMP_NB, "w+") as file:
            print("DS Done. Clearing temp file")
            file.write("")
        print("Closing curr_browser...")
        curr_browser.close()
        time.sleep(3)
        print("\n\n-----------------------------------\n\n")

