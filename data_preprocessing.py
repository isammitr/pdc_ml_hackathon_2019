import numpy as np
import pandas as pd
import json
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
import os 


def calc_sponsor_success_ratio(train):
    
    # Success Ratio
    a = train[train.petition_sponsored_campaign == 'True']['petition_is_victory'].value_counts(normalize=True)

    success_ratio_sponsored = a['True']

    b = train[train.petition_sponsored_campaign == 'False']['petition_is_victory'].value_counts(normalize=True)

    success_ratio_non_sponsored = b['True']
    
    return success_ratio_sponsored, success_ratio_non_sponsored

def extract_features(train, success_ratio_sponsored, success_ratio_non_sponsored):
    
    import re
    new_feat_list = []
    
    # Signature Ratio
    train['signature_ratio'] = train['petition_total_signature_count']/train['petition_calculated_goal']
    
    new_feat_list.append('signature_ratio')
    

    
    # Applying it back to dataframe
    train['sponsor_success_ratio'] = None

    train.loc[train.petition_sponsored_campaign == 'True', 'sponsor_success_ratio'] = success_ratio_sponsored

    train.loc[train.petition_sponsored_campaign == 'False', 'sponsor_success_ratio'] = success_ratio_non_sponsored

    new_feat_list.append('sponsor_success_ratio')
    
    
    # remove html tags
    remove_tag = lambda desc : re.sub('<.*?>', '', desc)

    remove_url = lambda desc : re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', desc)

    calc_length = lambda x: len(str(x).split(' '))

    s = train.petition_description.apply(remove_tag)

    s = s.apply(remove_url)
    
    # Calc length of Description
    train['len_pet_desc'] = s.apply(calc_length)
    
    new_feat_list.append('len_pet_desc')
    
    
    # Calc length of title
    train['len_pet_disp_title'] = train.petition_display_title.apply(calc_length)
    
    new_feat_list.append('len_pet_disp_title')
    
    return train[new_feat_list], new_feat_list

# utility functions
def merge_lists(l):
    # merge lists and return unique words as string
    tmp=[]
    for i in range(len(l)):
         tmp=tmp+l[i]
    tmp= set(tmp)
    return ' '.join(tmp)

# Preproc 
def preprocess_word(word):
    # Remove punctuation
    word = word.strip('\'"?!,.():;')
    # Convert more than 2 letter repetitions to 2 letter
    # funnnnny --> funny
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - & '
    word = re.sub(r'(-|\')', '', word)
    
    if word in stop_words:
        return ''

    return word


def is_valid_word(word):
    # Check if word begins with an alphabet
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)


def preprocess_desc(desc,use_stemmer=True):
    processed_desc = []
    # Convert to lower case
    desc = desc.lower()
    # Replaces URLs with the word URL
    desc = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', desc)
    # Replaces #hashtag with hashtag
    desc = re.sub(r'#(\S+)', r' \1 ', desc)
    # Remove RT (redesc)
    desc = re.sub(r'\brt\b', '', desc)
    # Replace 2+ dots with space
    desc = re.sub(r'\.{2,}', ' ', desc)
    # Strip space, " and ' from desc
    desc = desc.strip(' "\'')
    # Replace multiple spaces with a single space
    desc = re.sub(r'\s+', ' ', desc)
    # remove html tags
    desc = re.sub('<.*?>', '', desc)
    
    words = desc.split()

    #remove stop words
    words=[w for w in words if w not in stop_words]

    for word in words:
        word = preprocess_word(word)
        if is_valid_word(word):
            if use_stemmer:
                word = str(porter_stemmer.stem(word))
            processed_desc.append(word)

    return ' '.join(processed_desc)


def preprocess_json_file(file_path,train_or_test):
    df=pd.read_json(file_path)
    
    # Generate numerical features
    # Get success ratio wrt sponcered variable for train data
    # Use this ratio for test data
    if train_or_test=='train':
    	# Exclude 'active' petitions as we do not have 'is_victory' variable for them
        train_df=df[df['petition_petition_status'].isin(['closed','victory'])]
        success_ratio_sponsored, success_ratio_non_sponsored = calc_sponsor_success_ratio(train_df)
    else:
    	# 'active' petitions included in test dataset
        train_df=df
        success_ratios=joblib.load('data/split/train/success_ratios.pkl')
        success_ratio_sponsored=success_ratios[0]
        success_ratio_non_sponsored=success_ratios[1]
        
    num_df, new_feat_list = extract_features(train_df, success_ratio_sponsored, success_ratio_non_sponsored)

    # Standard Scaling
    scaler = StandardScaler()
    num_df = scaler.fit_transform(num_df)
    num_df = pd.DataFrame(num_df,columns=new_feat_list)

    # Preprocess text columns

    # These are text columns. They have some redundace/repitative information. Merge all unique words across al the columns
    title_cols=['_source_ask','highlight_ask','petition_display_title','petition_title']
    description_cols=['highlight_description','highlight_letter_body',
                      'petition_description','petition_letter_body']
    target_description_cols=['highlight_targeting_description',
                             'petition_primary_target_description',
                            'petition_primary_target_display_name']

    # Merge words from similar columns
    train_df['text_data']=train_df[title_cols+description_cols+target_description_cols].apply(lambda x:[i.split() for i in x],axis=1).apply(lambda x: merge_lists(x))

    # Process text data
    train_df['text_data']=train_df['text_data'].apply(lambda x: preprocess_desc(x))

    text_df=train_df[['text_data']]

    # Create pipeline to futher process text data -> count-vectorizer, tf-idf, SVD
    pipeline = Pipeline([
        ('bow', CountVectorizer()),  # strings to token integer counts
        ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
        ('pca',TruncatedSVD(n_components=100,random_state=51)),
    ])

    text_df=pipeline.fit_transform(text_df['text_data'])
    text_df=pd.DataFrame(text_df)

    #concat text and num df
    X=pd.concat([text_df,num_df],axis=1)
    
        
    if train_or_test=='train':
        root_dir='data/split/train/'
        
        # save success ratios wrt sponsorship
        success_ratios=[success_ratio_sponsored,success_ratio_non_sponsored]
        joblib.dump(success_ratios,root_dir+'success_ratios.pkl')
        
        y=train_df['petition_is_victory']
        y_cat=train_df['petition_category']
        
        # Save X and y to files for category prediction
        X.to_csv(root_dir+'X_cat100.csv',index=False)
        y_cat.to_csv(root_dir+'y_cat100.csv',index=False)

        # Add prediction category column to X and save files for is_victory prediction
        X['petition_category']=train_df['petition_category'].values
        X.to_csv(root_dir+'X100.csv',index=False)
        y.to_csv(root_dir+'y100.csv',index=False)
    
    else:
        root_dir='data/split/test/'
        # save file for category prediction
        X.to_csv(root_dir+'X_cat100.csv',index=False)


        
   

if __name__ == '__main__':
	use_stemmer=True
	porter_stemmer=PorterStemmer()
	stop_words=set(stopwords.words('english'))
	stop_words.add('url')
    train_path = os.path.join(os.getcwd(), 'data/train/train.json')
    test_path = os.path.join(os.getcwd(), 'data/validation/validation.json')

	print('Preprocessing train file')
	preprocess_json_file(train_path,'train')

	print('Preprocessing test file')
	preprocess_json_file(test_path,'test')

	print('Preprocessing Done')