In this directory we created the recommendation engine itself.
There are two jupyter notebooks:
* <a href="https://github.com/TAU-DB/guided-ds/blob/master/Chatbot/Jupyter_Cells_Chatbot_Model.ipynb">Jupyter_Cells_Chatbot_Model</a> - To build and train the seq2seq models
* <a href="https://github.com/TAU-DB/guided-ds/blob/master/Chatbot/Recommendation_Engine.ipynb">Recommendation_Engine</a> - to use the trained models

The recommendation engine workflow:<br>

`OFFLINE:`
<ol>
  <li>Cells were classified using the workflow stage classifier</li>
  <li>Different model was trained for each stage (of the input cell)</li>
</ol><br>

`ONLINE:`
<ol>
  <li>The user’s code is turned into a summed representation using its AST, Variable names are kept in a dictionary</li>
  <li>The user’s code is classified and its representation is passed to the relevant model</li>
  <li>The model outputs a next-cell recommendation</li>
  <li>Specificalization: The recommendation is personalized using the Variables dictionary</li>
  <li>Output: a ready-to-execute next cell recommendation </li>
</ol>

The <b>recommendation engine</b> scheme:<br>
<img src="https://github.com/TAU-DB/guided-ds/blob/master/Documentation/rec_eng.png" alt="recommendation_engine" width="700">

For more information see <a href="https://github.com/TAU-DB/guided-ds/tree/master/Documentation">Documentation</a>








