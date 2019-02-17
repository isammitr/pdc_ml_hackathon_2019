Updated README

Problem statement:
We were given textual and numerical data on numerous petition application applied in various countries on a number of subject. Data included text columns such as source_ask, petition_description, petition_title, petition_target, etc and numerical data included petition_signature_target, petition_progress, etc.

Approach:
Goal was to predict a petition’s category and petition’s status based on data given. Our approach involved combining text data by applying NLP pipelines and then combining it with numerical features which we engineered through looking at some of the trends in data. We used Logistic regression and XGBoost for predictions which gave us fairly good results on accuracy and f1-score metrics. We tuned the model to improve metrics, but certainly there is scope for future improvements by applying Word2Vec embeddings and using complex modelling techniques such as Glove and Bert.




How to run:
1. Need to unzip train.zip and validation.zip and should be added to repsective folders named train and validation which should be created in '/data' from where the code file will take the path.

2. Create two folders as:
	data/split/train
	data/split/test
   This is done for storing generated csv files.
 
3. Run preprocessing script:
	python data_preprocessing.py
4. Run ML script:
	python training_model.py

- submission.csv and learning_curve.png will be generated in data folder


Included are the visualizations and presentation ppt alongwith final submission_csv for the predictions on validation dataset.

