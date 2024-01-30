from semantic_translation.unit_measurement import find_unitCode, find_value

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
        # "turnOnRadiator": {
        #     "type": "Command",
        #     "description": "Command to turn on the radiator",
        #     "value": "inactive"
        #     },
        # "location": {
        #     "type": "GeoProperty",
        #     "value": {
        #         "type": "Point",
        #         "coordinates": [-123.12345, 45.67890]
        #         }
        #     }
    }
    
    ngsi_ld_context = {
            # Here will be collected all the extra context info for this Entity
        }
    
    def __init__(self, data):
        self.data = data 
    
    def manage_properties(self):
        """ 
        A mapping from WoT properties to NGSI-LD properties -->
        A property in WoT, like "temperature", would map directly 
        to a property in NGSI-LD with similar characteristics.
        """
        properties = self.data.get("properties")
        if properties is not None:
            for prop in properties:
                self.ngsi_ld_data[prop] = {
                    "type": "Property",
                    "value": find_value(properties.get(prop).get("type")),
                    "unitCode": find_unitCode(properties.get(prop).get("unit")),
                    "observedAt": "2023-12-24T12:00:00Z"
                    }

    def get_action_value(self): # TODO
        """ Available status values: 
        Pending, Delivered, In Progress, Completed, Failed, Expired.
        """
        # TODO better investigation
        return "pending"  # set as initial value and in real time the device will change it properly

    def manage_actions(self):
        """
        A mapping from WoT actions to NGSI-LD commands -->
        An action in WoT, such as "turnOnRadiator", can be mapped to a command in NGSI-LD. 
        The command in NGSI-LD may need to include additional logic to represent the action's effect.
        """
        actions = self.data.get("actions")
        if actions is not None:
            for act in actions:
                self.ngsi_ld_data[act] = {
                    # "description": actions.get(act).get("description"),
                    "type": "Property",
                    "value": {
                        "action": "execute",
                        "status": self.get_action_value(),
                    },
                }

    def add_default_location(self):
        """ Assumption that the device is here, in the location of NTUA"""
        self.ngsi_ld_data["location"] = {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [-123.12345, 45.67890]
                }
            }
    
    def set_context(self):
        """ Add the @context field at the ngsi-ld configuration 
        Call this function at the end so this field will be at the end of the configuration (the last one).
        """
        if self.ngsi_ld_context=={}:
            self.ngsi_ld_data["@context"] = "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context-v1.6.jsonld"
        else:
            self.ngsi_ld_data["@context"] = [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context-v1.6.jsonld",
                {
                    self.ngsi_ld_context
                }                
            ]
    
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
        
        # add everything to the config dictionary
        self.manage_properties()
        self.manage_actions()
        self.add_default_location()
        self.set_context()
        
        return self.ngsi_ld_data
        