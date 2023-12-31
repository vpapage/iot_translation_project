from manage_json import ManageJSON
from ngsi_ld.translate_ngsild_to_wot import TranslateNGSILDtoWoT
from wot.translate_wot_to_ngsild import TranslateWoTtoNGSILD

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
    manage = ManageJSON()
    
    # from WoT to NGSILD
    row_data = manage.read_json_file("data/temperatureSensor.td.json")
    print(row_data)
    manage = TranslateWoTtoNGSILD(row_data)
    simp_data = manage.translate_from_wot_to_ngsild()
    
    # # from NGSILD to WoT
    # row_data = manage.read_json_file("data/chatNGSILD.json")
    # print(row_data)
    # manage = TranslateNGSILDtoWoT(row_data)
    # simp_data = manage.translate_from_ngsild_to_wot()
    
    print(simp_data)
    main()