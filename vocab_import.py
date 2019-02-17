import pickle
import numpy as np
pickle_in = open("outputs/cat_index.pkl","rb")
vocab_processor = pickle.load(pickle_in)
print(vocab_processor)
pickle_in_on = open("outputs/category.pkl","rb")
vocab_processor_2 = pickle.load(pickle_in_on)
print(vocab_processor_2)
