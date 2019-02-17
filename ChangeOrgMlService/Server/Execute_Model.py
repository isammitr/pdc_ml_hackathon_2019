{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'Config'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-16-211ed8d38c02>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      9\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     10\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 11\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mConfig\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mConfig\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     12\u001b[0m \u001b[0msys\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mappend\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'../'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     13\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'Config'"
     ]
    }
   ],
   "source": [
    "\n",
    "#Importing global libraries\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import json as js\n",
    "import sklearn as skl\n",
    "import pandas_profiling\n",
    "import sys\n",
    "\n",
    "\n",
    "from Config import Config\n",
    "sys.path.append('../')\n",
    "\n",
    "from Learning import funtion \n",
    "\n",
    "import LearningResource\n",
    "\n",
    "\n",
    "\n",
    "import InjestionResources\n",
    "from Config import Config\n",
    "\n",
    "#Variable declaration\n",
    "input_path  = r\"/Users/abhijit/Documents//\"\n",
    "input_file  = \"train_clean.json\"\n",
    "ColNameList = [] \n",
    "dimentions_list =[]\n",
    "\n",
    "\n",
    "dimentions_list = Generate_AnalysisColumnList(Input_Json)\n",
    "\n",
    "out_path_json = Config.INJEST_DYNAMIC_CONFIG_DICT[\"repo_root\"] + r'\\data\\train_clean.json'\n",
    "InjestionResources.injest_json(dimentions_list, out_path_json)\n",
    "\n",
    "\n",
    "#Reading JSON Object into dataframes\n",
    "dataset = pd.read_json(out_path_json) \n",
    "DependantVar_List, Prediction_List = Prepare_Model_data(dataset,\"petition_is_victory\")\n",
    "Prediction_List = Run_Model(\"Gradient Boost Classifier\",DependantVar_List,Prediction_List,DependantVar_List)   \n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
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
