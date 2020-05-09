# Dataset Builder

Our first task is to create a repository of reproducible data science code-snippets. <br>
We'de like to methodically download datasets, jupyter notebooks, and all relevant metadata from Kaggle.com (online community of data scientists). <br>
Then, we'de like to parse this repository into tsv files that will be used as input to our models in the following stages.

This process is implemented across multiple python files:
* In [consts.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/consts.py) we configure paths and constants (They are set to the default value which we used, all are configurable).
* We use [kaggleapi.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/kaggleapi.py) to get a list of datasets (and competitions) to download.
* Then, we use [download.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/download.py) to download the notebooks and their metadata for each dataset.
* [execute_nb.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/execute_nb.py) is used to run the downloaded notebooks, using web drivers, to get the outputs for each cell.
* Now we have a repository. The rest of the python files where used to parse the downloaded data into different tsv files (for different models training):
    * [ds_csv_generator.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/ds_csv_generator.py) creates a tsv of datasets data.
    * [nb_csv_generator.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/nb_csv_generator.py) creates a tsv of notebooks data and a tsv of cells data.
    * [masking.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/masking.py) is used to create a Masked code from the original source code of the cells, as explained in the documentation.
    * [convert_to_chatbot_input.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/convert_to_chatbot_input.py) is used to convert a tsv with cells data into a tsv of cells pairs, that we used to train our [Chatbot](https://github.com/TAU-DB/guided-ds/tree/master/Chatbot).


[example.ipynb](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/example.ipynb) demonstrates the entire process, but keep in mind that the system was used by running the relevant functions from the python files directly.

For more information about the implementation see- <a href="https://github.com/TAU-DB/guided-ds/tree/master/Documentation">Documentation</a>. <br>
In addition, each function is well-documented within the mentiond python files.

Downloaded Datasets, notebooks and metadata are stored in the <a href="https://github.com/TAU-DB/guided-ds/tree/master/datasets">datasets</a> directory. <br>
The parsed tsv files that were used to train our models are stored in the <a href="https://github.com/TAU-DB/guided-ds/tree/master/data">Data</a> directory.

<em>The system was tested and used on a Windows10 machine with Python 3.6</em>

**prerequisite:** <br>
In order to use the dataset builder you must have Kaggle credentials set up. <br>
Follow the instructions from: https://github.com/Kaggle/kaggle-api#api-credentials
You also need to set you kaggle username and password in [consts.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/consts.py).
<br>For the Dataset Builder, we also used: [Selenium](https://selenium-python.readthedocs.io/installation.html), [Patool](https://pypi.org/project/patool/), [Pickle](https://docs.python.org/3/library/pickle.html), [html2text](https://pypi.org/project/html2text/)




