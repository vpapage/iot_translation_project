class ManageNGSILD():

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


    def manage_properties(self, data):
        keywords = ["id", "type", "name"]
        for key in data:
            if key not in keywords:
                avail_property = data.get(key)
                print(avail_property)
        return avail_property
    
    def create_json(self, simplified_data):
        data = simplified_data.get("simplified_data")
        ngsi_ls_json = {
            "new-new": data
        }
        return ngsi_ls_json
    
    def translate_from_ngsild_to_wot(self, data):
        new_id = data.get("id")
        new_title = data.get("title")
        new_description = data.get("description")
        self.ngsi_ld_data.update(
            {
                "id": new_id,
                "title": new_title,
                "description": new_description
            }
        )
        return self.ngsi_ld_data