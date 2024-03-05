import logging
from semantic_translation.unit_measurement import find_unit
from wot.security_definition import every_security_option  # more security options


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TranslateNGSILDtoWoT():

    def __init__(self, data):
        self.data = data 
        logging.info("Initializing translation from NGSI-LD to WoT.")

    def _find_property_type(self, prop):
        """ A Mapping from NGSI-LD property value to Wot property type. """
        data_class = type(prop.get("value"))
        conversion = None
        if data_class==type(None):
            conversion = {
                "description": prop.get("description", ""),
                "type": "string",
                "forms": []
            }
        elif data_class==type(10) or data_class==type(10.10):
            conversion = {
                "description": prop.get("description", ""),
                "type": "number",
                "init": find_unit(prop.get("unitCode")),
                "forms": []
            }
        elif data_class==type("str"):
            conversion = {
                "description": prop.get("description", ""),
                "type": "string",
                "forms": []
            }
        elif data_class==type(True):
            conversion = {
                "description": prop.get("description", ""),
                "type": "boolean",
                "forms": []
            }
        elif data_class==type([]): 
            conversion = {
                "description": prop.get("description", ""),
                "type": "array",
                "forms": []
            }
        elif data_class==type({}):
            # not supported yet 
            conversion = {
                "description": prop.get("description", ""),
                "type": "object",
                "forms": []
            }
        else:
            raise Exception("NGSI-LD value to Wot type could not be done.")
        return conversion

    def manage_forms(self, item, placeholder_ip="PLACEHOLDER_IP"):
        forms = [{
            "contentType": "application/json",
            "href": f"http://{placeholder_ip}/{item}"
        }]
        return forms

    def manage_properties(self):
        avail_properties = {}
        for key, value in self.data.items():
            if isinstance(value, dict) and value.get("type")=="Property" and not isinstance(value.get("value"), dict):
                prop = self.data.get(key)
                avail_properties[key] = self._find_property_type(prop)
                avail_properties[key]["forms"] = self.manage_forms(item=key)
        print(avail_properties)
        return avail_properties

    def manage_actions(self):
        avail_actions = {}
        for key, value in self.data.items():
            print(key, value)
            if isinstance(value, dict) and value.get("type")=="Property" and isinstance(value.get("value"), dict) and value.get("action") is not None:
                act = value.get("value")
                avail_actions[key] = {
                    "description": act.get("description", ""),
                    "forms": self.manage_forms(key)
                }
        print(avail_actions)
        return avail_actions

    def translate(self):
        """ The real translation """
        
        # base info 
        context = "https://www.w3.org/2019/wot/td/v1"
        title = self.data.get("type")
        description = self.data.get("description", "")
        
        # cross models id number
        ngsild_id = self.data.get("id")
        parts = ngsild_id.split(":")
        id_num = parts[-1]

        # results dictionary
        wot_data = {
            "@context": context,
            "id": f"urn:wot:{title}:{id_num}",
            "title": title, 
                "description": description,
            "securityDefinitions": {
                "no_sec": {
                "scheme": "nosec"
                }
            },
            "security": ["no_sec"],
            "properties": self.manage_properties(),
            "actions": self.manage_actions()
        }

        return wot_data
