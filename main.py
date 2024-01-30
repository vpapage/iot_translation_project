from manage_json import ManageJSON
from semantic_translation.translate_ngsild_to_wot import TranslateNGSILDtoWoT
from semantic_translation.translate_wot_to_ngsild import TranslateWoTtoNGSILD


def main():
    print("Main function displaying basic usage of the the project's capabilities")

if __name__ == "__main__":
    manage_file = ManageJSON()
    
    print("from WoT to NGSILD")
    row_data_wot = manage_file.read_json_file("data/wot_property_action.td.json")
    print("row data:")
    print(row_data_wot)
    translate_model_1 = TranslateWoTtoNGSILD(row_data_wot)
    data_result_ngsild = translate_model_1.translate_from_wot_to_ngsild()
    print("result")
    print(data_result_ngsild)
    manage_file.write_json_file(data_result_ngsild, "data/results/ngsild_result_property_action.json")
    
    print("from NGSILD to WoT")
    row_data_ngsild = manage_file.read_json_file("data/ngsild_property_action.json")
    print("row_data")
    print(row_data_ngsild)
    translate_model_2 = TranslateNGSILDtoWoT(row_data_ngsild)
    data_result_wot = translate_model_2.translate_from_ngsild_to_wot()
    print("result")
    print(data_result_wot)
    manage_file.write_json_file(data_result_wot, "data/results/wot_result_property_action.td.json")

    main()