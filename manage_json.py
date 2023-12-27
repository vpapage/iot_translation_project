import json
from ngsi_ld.manage_ngsi_ld import ManageNGSILD
from wot.manage_wot import ManageWoT

class ManageJSON():

    def __init__(self, source_metamodel):
        if source_metamodel == "WoT":
            self.target_metamodel = "NGSI-LD"
            # self.manage_source_metamodel = ManageWoT()
            # self.manage_target_metamodel = ManageNGSILD()
        elif source_metamodel == "NGSI-LD":
            self.target_metamodel = "WoT"
            # self.manage_source_metamodel = ManageNGSILD()
            # self.manage_target_metamodel = ManageWoT()
        else:
            raise Exception("The metamodel that you suggested is not supported.")

    def read_json_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise Exception(f"Error decoding JSON: {e}")       

    def write_json_file(self, data, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    def translate_try(self, data):
        final_data = self.manage_source_metamodel.translate_from_wot_to_ngsild(data)
        print("final_data:")
        print(final_data)
        # final_json = self.manage_target_metamodel.create_json(final_data)
        # print("final data:")
        # print(final_json)
        return final_data
