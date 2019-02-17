{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## Multiple Linear Regression\n",
    "\n",
    "# Importing the libraries\n",
    "import numpy as np\n",
    "#import matplotlib.pyplot as plt\n",
    "import pandas as pd\n",
    "#import Json library \n",
    "import json as js\n",
    "\n",
    "import pandas_profiling\n",
    "\n",
    "import sys\n",
    "import json\n",
    "\n",
    "sys.path.append('../')\n",
    "from Config import Config\n",
    "\n",
    "\n",
    "input_path = r\"/Users/abhijit/Documents/GitHub/pdc_ml_hackathon_2019/data/\"\n",
    "input_file = \"train.json\"\n",
    "#with open(input_path+input_file, 'r') as f:\n",
    "#    distros_dict = json.load(f)\n",
    "\n",
    "    \n",
    "    \n",
    "dataset = pd.read_json(input_path+input_file)    \n",
    "AnalysisColumnList = []  \n",
    "\n",
    "dataset1 = dataset.replace({'petition_is_victory': {'True': 1, 'False': 0}})\n",
    "\n",
    "\n",
    "print (\"success\")\n",
    "\n",
    "\n",
    "for ColumnName in list(dataset):\n",
    "    if ColumnName not in (\"petition_is_victory\"):\n",
    "        #print(ColumnName,dataset[ColumnName].unique().size)\n",
    "        if dataset[ColumnName].unique().size < 1000:\n",
    "            ds = dataset[[\"petition_is_victory\",ColumnName]] \n",
    "            ConvertedDataset = pd.get_dummies( ds )\n",
    "            correlation = ConvertedDataset.corr(method='pearson')\n",
    "            #print(type(correlation[ColumnName][\"petition_is_victory\"]))\n",
    "            #print(ColumnName)\n",
    "            #print(type(correlation[\"petition_is_victory_True\"]))\n",
    "                                  \n",
    "            for element in correlation[\"petition_is_victory_True\"]:\n",
    "                if np.less(0,element) and np.not_equal(1,element) :\n",
    "                    AnalysisColumnList.append(ColumnName)\n",
    "                    #print(ColumnName)\n",
    "                    break\n",
    "\n",
    "                    \n",
    "print(AnalysisColumnList)                     \n",
    "print(\"Complete\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
