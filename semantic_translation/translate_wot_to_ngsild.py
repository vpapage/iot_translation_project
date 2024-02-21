import logging
from semantic_translation.unit_measurement import find_unitCode
from semantic_translation.type_definitions import find_value
from data.ngsi_datamodel_template import yaml_tamplate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        logging.info("Initializing translation from WoT to NGSI-LD.")
    
    def manage_properties(self):
        """ 
        A mapping from WoT properties to NGSI-LD properties -->
        A property in WoT, like "temperature", would map directly 
        to a property in NGSI-LD with similar characteristics.
        """
        properties = self.data.get("properties")
        if properties is not None:
            for prop in properties:
                self.ngsi_ld_data[prop] = find_value(properties.get(prop))

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
                    "type": "Property",
                    "value": {
                        "action": "execute",
                        "status": "pending",
                        act: None     # like this the input could be anything
                    },
                    "description": actions.get(act).get("description")
                }

    def add_default_location(self):
        """ Assumption that the device is here, in the location of NTUA"""
        self.ngsi_ld_data["location"] = {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [37.979037, 23.782899]
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
    
    def translate(self):
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



    def data_model_properties(self):
        """ A mapping from WoT properties to NGSI-LD data-model properties. """
        data_model_properties = {}
        properties = self.data.get("properties")
        if properties is None:
            logging.info("None properies found.")  
        else:
            for prop in properties:
                entity_property = properties.get(prop)
                data_model_properties[prop] = {}
                description = entity_property.get("description")
                data_model_properties[prop]["description"] = f"'{description}'"
                # optional fields
                fields = ["maximum", "minimum"]
                for field in fields:
                    if entity_property.get(field): 
                        data_model_properties[prop][field] = entity_property.get(field)
                # required fields 
                property_type = entity_property.get("type")
                if property_type=="number":
                    data_model_properties[prop]["x-ngsi"] = {"units": entity_property.get("unit")}
                data_model_properties[prop]["type"] = property_type
        return data_model_properties

    def data_model_generator(self):
        """ Convert the WoT thing description (TD) into a NGSI-LD Informtion Model. """
        
        # generic info
        title = self.data.get("title")
        description = self.data.get("description")
        
        schemas = {
            title : {
                "description": f"'The data model describes: {description}'",
                "properties": self.data_model_properties()
            }
        }
        data_model_yaml = yaml_tamplate
        data_model_yaml["components"]["schemas"] = schemas

        return data_model_yaml