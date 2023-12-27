from manage_json import ManageJSON
from ngsi_ld.manage_ngsi_ld import ManageNGSILD
from wot.manage_wot import ManageWoT

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
    manage = ManageJSON(source_metamodel="WoT")
    # row_data = manage.read_json_file("data/temperatureSensor.td.json")
    row_data = manage.read_json_file("data/chatNGSILD.json")
    print(row_data)
    # translated_data = manage.translate(row_data)
    # manage.write_json_file(translated_data, "./data/trial.json")
    
    manage = ManageNGSILD()
    simp_data = manage.manage_properties(row_data)
    print(simp_data)
    main()