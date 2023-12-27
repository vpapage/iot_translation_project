class ManageWoT():
    
    ngsi_ld_data = {
        "id": "urn:ngsi-ld:TemperatureSensor:001",
        "type": "TemperatureSensor",
        "name": {
            "type": "Text",
            "value": "Temperature Sensor 001"
            },
        "temperature": {
            "type": "Property",
            "value": 25.5,
            "unitCode": "CEL",
            "observedAt": "2023-12-24T12:00:00Z"
            },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [-123.12345, 45.67890]
                }
            }
    }
    
    def manage_properties(self, data):
        # TODO maybe translate_wot_to_ngsild for better use. Or better fix/manage properties.
        properties = data.get("properties")
        if properties is not None:
            for prop in properties:
                wot_type = properties.get(prop).get("type")
                wot_unit = properties.get(prop).get("unit")
                wot_description = properties.get(prop).get("description")
        print("come on")
        # print(keys_properties)
        # for prop in properties: # check not empty properties
            
        # simplified_data = {
        #     "simplified_data": data
        # }
        return wot_type, wot_unit, wot_description
    
    def create_json(self, simplified_data):
        data = simplified_data.get("simplified_data")
        ngsi_ls_json = {
            "new-new": data
        }
        return ngsi_ls_json
    
    def translate_from_wot_to_ngsild(self, data):
        new_id = data.get("id")
        new_type = data.get("title")
        new_description = data.get("description")
        self.ngsi_ld_data.update(
            {
                "id": new_id,
                "type": new_type,
                "name": {
                    "type": "Text",
                    "value": new_description
                    },
                }
            )
        return self.ngsi_ld_data
        