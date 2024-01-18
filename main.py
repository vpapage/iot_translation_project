from manage_json import ManageJSON
from semantic_translation.translate_ngsild_to_wot import TranslateNGSILDtoWoT
from semantic_translation.translate_wot_to_ngsild import TranslateWoTtoNGSILD

car = {
    "properties": {
        "name1": {
            "brand": "Ford1",
            "model": "Mustang1",
            "year": 19641
            }, 
        "name2": {
            "brand": "Ford2",
            "model": "Mustang2",
            "year": 19642
            }, 
    }
}

def main():
    print("Hello from the main function!")

if __name__ == "__main__":
    manage_file = ManageJSON()
    
    # from WoT to NGSILD
    row_data = manage_file.read_json_file("data/temperatureSensor.td.json")
    print(row_data)
    translate_model = TranslateWoTtoNGSILD(row_data)
    simp_data = translate_model.translate_from_wot_to_ngsild()
    manage_file.write_json_file(simp_data, "data/results/ngsild_temperatureSensor.json")
    
    # # from NGSILD to WoT
    # row_data = translate_model.read_json_file("data/chatNGSILD.json")
    # print(row_data)
    # translate_model = TranslateNGSILDtoWoT(row_data)
    # simp_data = translate_model.translate_from_ngsild_to_wot()
    # manage_file.write_json_file(simp_data, "data/results/wot_temperatureSensor.td.json")

    print(simp_data)
    main()