from get_arguments import *
import json
import csv
import pickle
import ast
from sklearn import svm


class ScoringModel:

    def __init__(self):
        self.file_path = args.filepath
        self.cont_processor = None

    def load_file(self):
        """
        load file input json parameters
        """
        row_one = ["petition_id", "predicted_petition_category", "predicted_petition_is_vectory"]
        with open('submission.csv', 'w', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row_one)

        pickle_in_on = open("outputs/country_index.pkl", "rb")
        self.cont_processor = pickle.load(pickle_in_on)

        f = open(self.file_path, encoding='utf-8')
        file_object = json.load(f)

        pickle_in_on = open("outputs/category.pkl", "rb")
        cat_processor = pickle.load(pickle_in_on)

        for each in file_object:
            id_param = each['petition_id']
            highlighted = each["highlight_ask"]
            highlighted = highlighted.split('<mark>')[1].split('</mark>')[0].lower()
            category = cat_processor[highlighted]
            result = self.transform(category, each)
            row = [id_param, category, result]
            with open('submission.csv', 'a', encoding='utf-8') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
        csvFile.close()

    # noinspection PyAttributeOutsideInit
    def transform(self, category, json_data):
        """
        start transforming data in to valid feature vector
        :param category: category of the model
        :param json_data: input json data
        :return: result of prediction
        """
        model_path = 'models/' + str(category) + '.pkl'
        pickle_model = open(model_path, "rb")
        model_processor = pickle.load(pickle_model)
        sponsor = "True"
        self.value_victory = 0
        value_profit = 0
        if json_data['_source_sponsorship_active'] is None:
            sponsor = "False"
        if json_data['petition_petition_status'] == 'victory':
            self.value_victory = 1
        if json_data['petition_organization_non_profit'] == "True":
            value_profit = 1
        feature_vector = [self.value_victory,
                          int(bin(ast.literal_eval(json_data['_source_sponsored_campaign']))[2]),
                          int(bin(ast.literal_eval(sponsor))[2]),
                          int(bin(ast.literal_eval(json_data['petition_primary_target_is_person']))[2]),
                          value_profit]
        result_list = model_processor.predict([feature_vector])
        result = result_list[0]
        return bool(result)


if __name__ == '__main__':
    split_obj = ScoringModel()
    split_obj.load_file()
