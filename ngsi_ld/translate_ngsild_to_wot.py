class TranslateNGSILDtoWoT():

    wot_data = {
        "@context": "https://www.w3.org/2019/wot/td/v1",
        "id": "urn:dev:wot:com:example:temperaturesensor",
        "title": "TemperatureSensor",
        "description": "A simple temperature sensor",
        "securityDefinitions": {
            "no_sec": {
            "scheme": "nosec"
            }
        },
        "security": ["no_sec"],
        "properties": {
            "temperature": {
                "type": "number",
                "description": "The current temperature in degrees Celsius",
                "unit": "celsius",
                "readOnly": True,
                "observable": True,
                "forms": [{
                    "href": "http://example.com/sensor/temperature",
                    "contentType": "application/json"
                }]
            },
        }
    }
    
    def __init__(self, data):
        self.data = data 
        self.id = data.get("id")
        self.title = data.get("type")
        self.description = data["name"].get("value")
    
    def translate_value(self, value, unitCode):
        print(value, unitCode)
        return "prop_type", "prop_unit"

    def manage_properties(self):
        avail_properties = {}
        prop_type, prop_unit = ""
        for key in self.data:
            if self.data[key].get("type")=="Property":
                prop_type, prop_unit = self.translate_value(self.data[key].get("value"), self.data[key].get("unitCode"))
                avail_properties[key] = {
                    "type": prop_type,
                    "description": self.description,
                    "unit": prop_unit,
                    "readOnly": True,
                    "observable": True,
                    "forms": [{
                        "href": f"http://example.com/sensor/{key}",
                        "contentType": "application/json"
                    }],
                }
            print(avail_properties)
        return avail_properties

    def translate_from_ngsild_to_wot(self):
        self.wot_data.update(
            {
                "id": self.id,  # todo f"urn:dev:wot:{self.title}:123"
                "title": self.title,
                "description": self.description,
                "properties": self.manage_properties()
            }
        )
        return self.wot_data