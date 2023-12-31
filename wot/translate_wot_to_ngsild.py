class TranslateWoTtoNGSILD():
    
    ngsi_ld_data = {
        "id": "urn:ngsi-ld:TemperatureSensor:001",
        "type": "TemperatureSensor",
        "name": {
            "type": "Text",
            "value": "Temperature Sensor 001"
            },
        # "temperature": {
        #     "type": "Property",
        #     "value": 25.5,
        #     "unitCode": "CEL",
        #     "observedAt": "2023-12-24T12:00:00Z"
        #     },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [-123.12345, 45.67890]
                }
            }
    }
    
    def __init__(self, data):
        self.data = data 
        self.id = data.get("id")
        self.title = data.get("title")
        self.description = data.get("description")
    
    def translate_value(self, prop_type, prop_unit):
        print(prop_type, prop_unit)
        return "value", "unitCode"
    
    def manage_properties(self):
        properties = self.data.get("properties")
        if properties is not None:
            for prop in properties:
                prop_type = properties.get(prop).get("type")
                prop_unit = properties.get(prop).get("unit")
                value, unitCode = self.translate_value(prop_type, prop_unit)
                self.ngsi_ld_data[prop] = {
                    "type": "Property",
                    "value": value,
                    "unitCode": unitCode,
                    "observedAt": "2023-12-24T12:00:00Z"
                    }
    
    def translate_from_wot_to_ngsild(self):
        self.manage_properties()
        self.ngsi_ld_data.update(
            {
                "id": self.id,
                "type": self.title,
                "name": {
                    "type": "Text",
                    "value": self.description
                
                    },
                }
            )
        return self.ngsi_ld_data
        