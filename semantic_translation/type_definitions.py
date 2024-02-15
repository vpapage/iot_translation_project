from semantic_translation.unit_measurement import find_unitCode

assumption_about_conversions_of_data_structures = {

}

def find_type(property_value):
    """ A Mapping from NGSI-LD value to Wot type. """
    # TODO Να δίνει όλα τα data αυτην η συνάρτηση να επιστρέφει ετοιμο το property

    data_class = type(property_value)
    if  property_value is None:
        return "null"
    elif data_class==type(10) or data_class==type(10.10):
        return "number"
    elif data_class==type("str"): 
        return "string"
    elif data_class==type(True):
        return "boolean"
    elif data_class==type([]):
        return "array"
    elif data_class==type({}):
        return "object"
    else:
        return "unknown"


def find_value(prop):
    """ A Mapping from Wot type to NGSI-LD value. """
    property_type = prop.get("type")
    conversion = None
    if property_type=="number":
        conversion = {
            "type": "Property",
            "value": 0,
            "unitCode": find_unitCode(prop.get("unit"))
        }
    elif property_type=="string":
        conversion = {
            "type": "Property",
            "value": ""
        }
    elif property_type=="boolean":
        conversion = {
            "type": "Property",
            "value": False,
            "observedAt": "2023-12-24T12:00:00Z"
        }
    elif property_type=="array":
        # in python you can save in this list anything
        conversion = []
    elif property_type=="object":
        # not supported yet
        conversion = {}
    else:
        conversion = "unknown"
    return conversion
