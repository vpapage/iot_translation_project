from semantic_translation.unit_measurement import find_type, find_unit

class TranslateNGSILDtoWoT():

    wot_data = {
        "@context": "https://www.w3.org/2019/wot/td/v1",
        "id": "urn:wot:TemperatureSensor:123",
        "title": "TemperatureSensor",
        "description": "A simple temperature sensor",
        "securityDefinitions": {
            "no_sec": {
            "scheme": "nosec"
            }
        },
        "security": ["no_sec"],
        "properties": {
            # "temperature": {
            #     "type": "number",
            #     "description": "The current temperature in degrees Celsius",
            #     "unit": "celsius",
            #     "readOnly": True,
            #     "observable": True,
            #     "forms": [{
            #         "href": "http://example.com/sensor/temperature",
            #         "contentType": "application/json"
            #     }]
            # },
        },
        "actions": {}
    }
    
    def __init__(self, data):
        self.data = data 

    def manage_properties(self):
        avail_properties = {}
        for key, value in self.data.items():
            if isinstance(value, dict) and value.get("type")=="Property" and not isinstance(value.get("value"), dict):
                avail_properties[key] = {
                    "type": find_type(self.data[key].get("value")),
                    "unit": find_unit(self.data[key].get("unitCode")),
                    "readOnly": True,
                    "observable": True,
                    # "forms": [{
                    #     "href": f"http://example.com/sensor/{key}",
                    #     "contentType": "application/json"
                    # }],
                }
        print(avail_properties)
        return avail_properties

    def manage_actions(self):
        avail_actions = {}
        for key, value in self.data.items():
            print(key, value)
            if isinstance(value, dict) and value.get("type")=="Property" and isinstance(value.get("value"), dict) and value.get("action") is not None:
                avail_actions[key] = {
                    "description": "", # TODO
                    # "forms": [{
                    #     "href": f"http://example.com/sensor/{key}",
                    #     "contentType": "application/json"
                    # }],
                }
        print(avail_actions)
        return avail_actions

    def translate_from_ngsild_to_wot(self):
        """ The real translation """
        
        # id manipulation
        ngsild_id = self.data.get("id")
        parts = ngsild_id.split(":")
        title = parts[-2]
        id_num = parts[-1]
        if isinstance(self.data.get("name"), dict) and self.data.get("name").get("value") is not None:
            description = self.data.get("name").get("value")
        else: 
            description = "No description given"

        # update default dictionary
        self.wot_data.update(
            {
                "id": f"urn:wot:{title}:{id_num}",
                "title": self.data.get("type"), # or title
                "description": description,
                "properties": self.manage_properties(),
                "actions": self.manage_actions()
            }
        )
        return self.wot_data