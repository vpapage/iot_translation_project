import logging
from semantic_translation.unit_measurement import find_unitCode
from ngsild_datamodel_template import yaml_template

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TranslateWoTtoNGSILD():
    
    ngsi_ld_data = {
        "id": "urn:ngsi-ld:TemperatureSensor:001",
        "type": "TemperatureSensor",
        "description": "Temperature Sensor 001"
    }
    
    ngsi_ld_context = {
            # Here will be collected all the extra context info for this Entity
        }
    
    def __init__(self, data):
        self.data = data 
        logging.info("Initializing translation from WoT to NGSI-LD.")
    
    
    def _find_property_value(self, prop):
        """ A Mapping from Wot property type to NGSI-LD property value. """
        property_type = prop.get("type")
        conversion = None
        if property_type=="number":
            conversion = {
                "type": "Property",
                "value": 0,
                "unitCode": find_unitCode(prop.get("unit")),
                "description": prop.get("description", "")
            }
        elif property_type=="string":
            conversion = {
                "type": "Property",
                "value": "",
                "description": prop.get("description", "")
            }
        elif property_type=="boolean":
            conversion = {
                "type": "Property",
                "value": False,
                "observedAt": "2023-12-24T12:00:00Z",
                "description": prop.get("description", "")
            }
        elif property_type=="array":
            # in python you can save in this list anything
            conversion = {
                "type": "Property",
                "value": [],
                "description": prop.get("description", "")
            }
        elif property_type=="object":
            # not supported yet
            conversion = {
                "type": "Property",
                "value": {},
                "description": prop.get("description", "")
            }
        else:
            raise Exception("Wot type to NGSI-LD value could not be done.")
        return conversion
    
    def manage_properties(self):
        """ 
        A mapping from WoT properties to NGSI-LD properties -->
        A property in WoT, like "temperature", would map directly 
        to a property in NGSI-LD with similar characteristics.
        """
        properties = self.data.get("properties")
        if properties is not None:
            for prop in properties:
                self.ngsi_ld_data[prop] = self._find_property_value(properties.get(prop))

    def manage_actions(self):
        """
        A mapping from WoT actions to NGSI-LD -->
        An action in WoT, such as "turnOnRadiator", cannot be mapped directly in NGSI-LD.
        We create property attributes in order to retain the information.
        The command in NGSI-LD may need to include additional logic to represent the action's effect.
        """
        actions = self.data.get("actions")
        if actions is not None:
            for act in actions:
                self.ngsi_ld_data[act] = {
                    "type": "Property",
                    "value": ""
                }
            # input/output not supported yet

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
                "description": self.data.get("description", "")
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
        
        # WoT properties collected
        properties = self.data.get("properties")
        if properties is None:
            logging.info("Properties not found.")  
        else:
            for prop in properties:
                entity_property = properties.get(prop)
                data_model_properties[prop] = {}
                # optional fields
                description = entity_property.get("description", "")
                if description: data_model_properties[prop]["description"] = f"'{description}'"     # weird quotes it is a string message
                fields = ["maximum", "minimum"]
                for field in fields:
                    if entity_property.get(field): 
                        data_model_properties[prop][field] = entity_property.get(field)
                # required fields 
                property_type = entity_property.get("type")
                if property_type=="number":
                    data_model_properties[prop]["x-ngsi"] = {"units": entity_property.get("unit")}
                data_model_properties[prop]["type"] = property_type

        # WoT actions collected  TODO wip
        actions = self.data.get("actions")
        if actions is None:
            logging.info("Actions not found.")  
        else:
            for act in actions:
                data_model_properties[act] = {
                    "format": "command",
                    "type": "string"
                }
        
        return data_model_properties

    def data_model_generator(self):
        """ Convert the WoT thing description (TD) into a NGSI-LD Data Model. """
        
        # generic info
        title = self.data.get("title")
        description = self.data.get("description", "")
        
        schemas = {
            title: {
                "description": f"'{description}'",
                "properties": self.data_model_properties()
            }
        }

        data_model_yaml = yaml_template
        data_model_yaml["components"]["schemas"] = schemas
        data_model_yaml["info"]["description"] = f"'The data model describes: {description}'"
        data_model_yaml["info"]["title"] = f"'{title}Models'"
        
        return data_model_yaml