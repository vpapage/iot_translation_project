from unit_measurement import find_type, units

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
        
    def translate_value(self, value, unitCode):
        """ Work In Progress!  
        This function should detect a range of values and return the appropriate values back.
        """
        print(value, unitCode)
        return "prop_type", "prop_unit"

    def manage_properties(self):
        avail_properties = {}
        for key in self.data:
            if self.data[key].get("type")=="Property":
                avail_properties[key] = {
                    "type": find_type(self.data[key].get("value")),
                    "description": self.description,
                    "unit": units(self.data[key].get("unitCode")),
                    "readOnly": True,
                    "observable": True,
                    # "forms": [{
                    #     "href": f"http://example.com/sensor/{key}",
                    #     "contentType": "application/json"
                    # }],
                }
            print(avail_properties)
        return avail_properties

    def translate_from_ngsild_to_wot(self):
        """ The real translation """
        
        # id manipulation
        ngsild_id = self.data.get("id")
        parts = ngsild_id.split(":")
        title = parts[-2]
        id_num = parts[-1]
        
        # update default dictionary
        self.wot_data.update(
            {
                "id": f"urn:wot:{title}:{id_num}",
                "title": self.data.get("type"), # or title
                "description": self.data["name"].get("value"),
                "properties": self.manage_properties()
            }
        )
        return self.wot_data