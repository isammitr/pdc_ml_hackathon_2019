import sys
import json

sys.path.append('../')
from Config import Config

def injest_json(dimentions_list, output_file_loc):
    '''
    :param dimentions_list: list of dimensions to be extracted out of input data
    :param output_file_loc: string of location+filename to be saved as output of this method
    :return:
    '''

    # sanitize arguments
    validationErrors = {}
    if not isinstance(dimentions_list, list):
        validationErrors['dimentions_list'] = 'Invalid Dimension List'
    if not output_file_loc or not isinstance(output_file_loc, str):
        validationErrors['output_file_loc'] = 'Invalid Output File Loc'

    if validationErrors:
        raise Exception('InjestionResources: injest_json: Invalid arguments passed: %r' % (validationErrors))
    # sanitize arguments over

    # response = {}
    json_path = Config.INJEST_DYNAMIC_CONFIG_DICT["repo_root"] + '\\' + Config.INJEST_DYNAMIC_CONFIG_DICT["data_location"]
    with open(json_path, 'r') as f:
        dataset_list = json.load(f)

        for one_dataset in dataset_list:
            # delete_keys_list = [key for key in one_dataset.keys() if key not in dimentions_list]
            delete_keys_list = [key for key in one_dataset if key not in dimentions_list]
            for key in delete_keys_list:
                # remove this key from one_dataset
                del one_dataset[key]

        fout = open(output_file_loc, 'w')
        fout.write(json.dumps(dataset_list))
        fout.close()
