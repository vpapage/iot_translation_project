from unit_measurement import unitCode

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
        # # is location necessary ??
        # "location": {
        #     "type": "GeoProperty",
        #     "value": {
        #         "type": "Point",
        #         "coordinates": [-123.12345, 45.67890]
        #         }
        #     }
    }
    
    def __init__(self, data):
        self.data = data 
    
    def translate_value(self, prop_type, prop_unit):
        """ Work In Progress!  
        This function should detect a range of values and return the appropriate values back.
        """
        print(prop_type, prop_unit)
        return "value", "unitCode"
    
    def manage_properties(self):
        properties = self.data.get("properties")
        if properties is not None:
            for prop in properties:
                self.ngsi_ld_data[prop] = {
                    "type": "Property",
                    "value": None,
                    "unitCode": unitCode(properties.get(prop).get("unit")),
                    "observedAt": "2023-12-24T12:00:00Z"
                    }

    def add_default_location(self):
        self.ngsi_ld_data["location"] ={
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [-123.12345, 45.67890]
                }
            }
    
    def translate_from_wot_to_ngsild(self):
        """ The real translation """
        
        # id manipulation and generic info
        wot_id = self.data.get("id")
        parts = wot_id.split(":")
        title = parts[-2]
        id_num = parts[-1]
        
        self.ngsi_ld_data.update(
            {
                "id": f"urn:ngsi-ld:{title}:{id_num}",
                "type": self.data.get("title"),
                "name": {
                    "type": "Text",
                    "value": self.data.get("description"),
                },
            }
        )
        
        # add properties to the default dictionary
        self.manage_properties()
        self.add_default_location()
        
        return self.ngsi_ld_data
        