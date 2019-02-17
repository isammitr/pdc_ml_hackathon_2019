import sys
import json

path_train_json = r"C:\Projects\PDC_Hackathon_2019\pdc_ml_hackathon_2019-master\data\train.json"
path_trainout_json = r"C:\Projects\PDC_Hackathon_2019\pdc_ml_hackathon_2019-master\data\trainout.json"
dimentions_list = ["petition_organization_slug","_score", "xxxxx"]
# dimentions_list = ["petition_organization_slug","petition_restricted_location","petition_relevant_location_lat","_score","petition_primary_target_slug","petition_description","highlight_description","petition_letter_body","petition_goal","petition_organization_id","petition_user_description","petition_total_signature_count","petition_primary_target_email","petition_organization_non_profit","petition_primary_target_type","highlight_ask","petition_display_title","petition_organization_zipcode","petition_organization_name","petition_category","_source_discoverable","petition_primary_target_is_person","petition_organization_city","petition_primary_target_display_name","filename"]
response = {}
with open(path_train_json, 'r') as f:
    dataset_list = json.load(f)
    print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("dataset length: ", len(dataset_list))
    print("dataset size: ", sys.getsizeof(dataset_list))
    print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    # print(len(dataset_list))
    # print(dataset_list[0])
    for one_dataset in dataset_list:
        # print("one_dataset: ", one_dataset)
        delete_keys_list = [key for key in one_dataset if key not in dimentions_list]
        # print("delete_keys_list length: ", len(delete_keys_list))

        for key in delete_keys_list:
            # remove this key from one_dataset
            del one_dataset[key]
            # sys.getsizeof(x)
        # print("one_dataset: ", one_dataset)
        # print("dataset size: ", sys.getsizeof(dataset_list))
        # str(input('Continue:'))
        # print(x)
    print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("dataset length: ", len(dataset_list))
    print("dataset size: ", sys.getsizeof(dataset_list))
    print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    fout = open(path_trainout_json, 'w')
    fout.write(json.dumps(dataset_list))
    fout.close()
'''
for one_dataset in dataset_list:
delete_keys_list = [key for key in one_dataset.keys() if key not in dimentions_list]
print(delete_keys_list)
print(len(delete_keys_list))
print(sys.getsizeof(one_dataset))
for k in delete_keys_list:
print("deleting")
del one_dataset[k]
print(sys.getsizeof(one_dataset))
break
'''