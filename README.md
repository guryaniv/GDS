<img src="https://github.com/TAU-DB/guided-ds/blob/master/Documentation/GDS_icon.png" width="100"/><br>
# Guided Data Science
 
 We present a recommendation system for Data Scientists that given a user cell of code  will recommend what the next line of code should be.
 
The recommendation system is built of three main parts (that are thoroughly explained <a href="https://github.com/TAU-DB/guided-ds/tree/master/Documentation">here</a>):

* <b>Data-set Builder</b> : Collects the necessary data to build our system (see- <a href="https://github.com/TAU-DB/guided-ds/tree/master/data_gathering">data_gathering</a>).
  * Downloaded Datasets, notebooks and metadata are stored in the <a href="https://github.com/TAU-DB/guided-ds/tree/master/datasets">datasets</a> directory.
  * The parsed tsv files that were used to train our models are stored in the <a href="https://github.com/TAU-DB/guided-ds/tree/master/data">Data</a> directory.
* <b>Workflow-Stage Classifier</b> : Classifies the code to the relevant Data Science workflow stage and provides context to the code (see- <a href="https://github.com/TAU-DB/guided-ds/tree/master/Classification">Classification</a>).
* <b>Recommendation Engine</b> : Generates the next-line recommendation (see- <a href="https://github.com/TAU-DB/guided-ds/tree/master/Chatbot">Chatbot</a>). 

The <b>system architecture</b> scheme:<br>

<img src="https://github.com/TAU-DB/guided-ds/blob/master/Documentation/system_arch.png" width="800"/>

The entire flow of creating the system is explained in the [Flow.ipynb](https://github.com/TAU-DB/guided-ds/blob/master/Flow.ipynb) notebook.

### Prerequisites:

Required libraries can be installed using the [requirements.txt](https://github.com/TAU-DB/guided-ds/blob/master/requirements.txt) file. Alternatively, you can create an environment using the [environment.yml](https://github.com/TAU-DB/guided-ds/blob/master/environment.yml) file.<br>
Notice that in order to use the Dataset Builder you must have Kaggle credentials set up.<br>
Follow instruction at: https://github.com/Kaggle/kaggle-api#api-credentials <br>
You also need to configure your kaggle username and password in the [data_gathering/consts.py](https://github.com/TAU-DB/guided-ds/blob/master/data_gathering/consts.py) file.
<br>For the weak supervision process in [Classification/Exploration_and_WeakSupervision.ipynb](https://github.com/TAU-DB/guided-ds/blob/master/Classification/Exploration_and_WeakSupervision.ipynb) you must have snorkel v0.7 installed.
snorkel does not support pip install. Follow instructions at: https://github.com/HazyResearch/snorkel#installation
