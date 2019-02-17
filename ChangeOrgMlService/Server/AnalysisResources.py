import InjestionResources
from Config import Config

def main():
    dimentions_list = ["petition_is_victory","_score","petition_calculated_goal","petition_total_signature_count","petition_progress","petition_category"]
    out_path_json = Config.INJEST_DYNAMIC_CONFIG_DICT["repo_root"] + r'\data\train_clean.json'
    InjestionResources.injest_json(dimentions_list, out_path_json)
    # print ("xxxxxxxxx MAIN FINISHED xxxxxxxxxxxx")

main()