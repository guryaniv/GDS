# DEPRECATED - DO NOT USE THIS FILE
# It will be deleted later, we keep it in case we decide to revert any updates.

print("DEPRECATED!!! !!! !!!")

# import data_gathering.consts as consts
# import data_gathering.download as dn
# import data_gathering.ds_csv_generator as ds
# # import data_gathering.execute_nb as exec
# import data_gathering.nb_csv_generator as nb
# import data_gathering.kaggleapi as kg
# import data_gathering.convert_to_chatbot_input as cb
#
#
# # Step 1 - Collecting metadata on relevant Kaggle datasets and competitions.
# # We need to create search_terms, which those keyword will be searched via Kaggle API to collect datasets.
#
# # in order to download datasets related to money we will write the search term and call get_competitions \ get_datasets
# # The outputs are 2 txt file for later use:
# # 1. consts.NOT_VALID_DATA_LINKS_NAME - holds data for non-relevant datasets so we won't search them again
# # 2. consts.DATA_LINKS_NAME - holds data for relevant datasets that will be used in "download.py" file.
# # Then we can decide to get info on datasets or competitions, or both.
#
#
# # search_terms = "finance money bank"
# # kg.get_kaggle_metadata(search_terms, comp=True, ds=True)
#
# # After we collected information on Kaggle relevant link, we would like to use it.
# # The following line will read the TXT link file and will use WebDriver to scrape Kaggle website.
# # After scraping Kaggle and getting a links to all relevant notebooks we will use kaggle API to pull them.
# # Note - You need to configure Kaggle username and password and consts file (KAGGLE_USER, KAGGLE_PW)
#
# # link_list = dn.read_links()
# # dn.download_data_and_kernels_link(link_list, stop_nb=False)
# # dn.pull_kernels()
#
# # Now, we would like to generate our own datasets, we will make 3 of them at this point.
# # 1. Contains info on the Kaggle datasets we gathered.
# # 2. Contains info on the notebooks and relates it to the first dataset
# # 3. Contains info on the cells we gathered.
#
# # ds.generate_ds_tsv()
# nb.generate_nb_tsv()
#
# # Now we can use the cells.tsv dataset to check our hypothesis with the Classification sub-project.
# # You may skip to Classification folder, it has all the file and information you may need.
#
#
# # In order to continue to Chatbot sub-project we need to make 3 new datasets,
# # which will be the input for the chatbot model
# # Each input contains representation of a cell and its successor.
# # 1. Each source cell
# # 2. Each source cell formatted at AST
# # 3. Each source cell after custom masking.
#
# cb.cells_to_masked_pairs()
# cb.cells_to_ast_pairs()
# cb.cells_to_source_pairs()
#
# print("\n###################\nFinished with example")
#
#
