import json
import csv
import re
import os
import pickle
import numpy as np
import ast
from sklearn import svm


class Scrapper:

    def __init__(self):
        self.country = {}
        self.dump_index = {}
        self.file_object = None
        self.train_data = {}

    def category_process(self):
        """
        creating custom setting for category rule
        """
        f = open("train/train.json", encoding='utf-8')
        self.file_object = json.load(f)
        dump_cat = {}
        count = 0
        counter = 0
        for each in self.file_object:
            highlighted = each["highlight_ask"]

            highlighted = highlighted.split('<mark>')[1].split('</mark>')[0].lower()
            dump_cat[highlighted] = each["petition_category"]
            if each['_source_country_code'] not in list(self.country.keys()):
                self.country[each['_source_country_code']] = counter
                counter = counter + 1
            if each["petition_category"] not in list(self.dump_index.keys()):
                self.dump_index[each["petition_category"]] = count
                count = count + 1

        os.makedirs('outputs', exist_ok=True)
        pickle_out = open("outputs/category.pkl", "wb+")
        pickle.dump(dump_cat, pickle_out)
        pickle_out_new = open("outputs/cat_index.pkl", "wb+")
        pickle.dump(self.dump_index, pickle_out_new)
        pickle_out_cont = open("outputs/country_index.pkl", "wb+")
        pickle.dump(self.country, pickle_out_cont)

    def create_train_data(self):
        """
        creating train data for each of the category findings
        """
        signature_count = {}
        for every_cat in list(self.dump_index.keys()):
            category_value = []
            total_signature_count = 0
            total_details = 0
            total_goal = 0
            for get_one in self.file_object:
                if get_one['petition_category'] == every_cat:
                    total_details = total_details + 1
                    total_goal = total_goal + get_one['petition_calculated_goal']
                    total_signature_count = total_signature_count + get_one['petition_total_signature_count']
                    value = 0
                    value_victory = 0
                    value_profit = 0
                    if get_one['petition_is_victory'] == "True":
                        value = 1
                    sponsor = "True"
                    if get_one['_source_sponsorship_active'] is None:
                        sponsor = "False"
                    if get_one['petition_petition_status'] == 'victory':
                        value_victory = 1
                    if get_one['petition_organization_non_profit'] == "True":
                        value_profit = 1
                    category_value.append(
                        [value_victory,
                         int(bin(ast.literal_eval(get_one['_source_sponsored_campaign']))[2]),
                         int(bin(ast.literal_eval(sponsor))[2]),
                         int(bin(ast.literal_eval(get_one['petition_primary_target_is_person']))[2]), value_profit,
                         value])
            self.train_data[every_cat] = category_value
            signature_count[every_cat] = [total_details, total_goal, round(total_signature_count / total_details)]
        print(json.dumps(self.train_data))
        print(json.dumps(signature_count))

    def start_training(self):
        """
        started training for given category model
        """
        for key, one_value in self.train_data.items():
            model_name = 'models/' + str(key) + '.pkl'
            x_data = []
            y_data = []
            for idx, one in enumerate(one_value):
                y_data.append(one[-1:][0])
                x_data.append(one[:5])
            self.model_store(x_data, y_data, model_name)

    # same for both models
    # noinspection PyAttributeOutsideInit
    def model_store(self, x_train, y_train, model_name):
        """
        data for svm classifier
        :param x_train: X feature vector data
        :param y_train: Y label assigned true or false
        :param model_name: given model path
        """
        self.model_name = model_name
        np.random.seed(0)
        os.makedirs('models', exist_ok=True)
        print(str(model_name), "\nTraining Process going on ....\n")
        model = svm.SVC(gamma='scale')
        model.fit(x_train, y_train)
        print(model.score(x_train, y_train))
        # note file saved in the outputs folder is automatically uploaded into experiment record
        pickle.dump(model, open(model_name, 'wb+'))


if __name__ == '__main__':
    split_obj = Scrapper()
    split_obj.category_process()
    split_obj.create_train_data()
    split_obj.start_training()
