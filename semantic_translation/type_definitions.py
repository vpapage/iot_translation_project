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


def find_value(property_type):
    """ A Mapping from Wot type to NGSI-LD value. """

    if  property_type is None:
        return None
    elif property_type=="number":
        return 0
    elif property_type=="string":
        return ""
    elif property_type=="boolean":
        return False
    elif property_type=="array":
        return []
    elif property_type=="object":
        return {}
    else:
        return "unknown"
