from ngsi_ld.translate_ngsild_to_wot import TranslateNGSILDtoWoT

class SensingFunction:

    def __init__(self, name):
        self.name = name
        self.state = "state"
        self.commands = "commands"   # ["switch on", "switch off", "toggle"]

    def show_element(self):
        print(f"SensingFunction: ", self.name)


class Sensor:
    
    def __init__(self):
        self.rdf = None
    
    def show_ontology(self):
        print("SAREF: NGSI-LD")
    
    def show_element(self):
        print("Sensor")

    def hasFunction(self, name):
        func = SensingFunction(name)
        print(func.show_element())

    def set_rdf(self, rdf):
        self.rdf = rdf
        print(rdf)
        # # TODO the translation
        # translate_rdf = TranslateNGSILDtoWoT()
        # translate_rdf.translate_from_ngsild_to_wot(rdf)


# ---------------------------------------------- #

class Saref:

    def __init__(self):
        self.sensor = Sensor()
        self.hasFunction = True
        self.sensingFunction = SensingFunction()
        
