import json


class ManageJSON():
    """ This class is developed to manage json files """

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

