class Function:
    
    def __init__(self, name):
        self.name = name

    def show_ontology(self):
        print("SAREF: NGSI-LD")


    def show_element(self):
        print(f"Function: ", self.name)


class SensingFunction(Function):

    # def __init__(self, name):
    #     self.name = name

    def show_element(self):
        print(f"SensingFunction: ", self.name)


# ---------------------------------------------- #


class Device:

    def show_ontology(self):
        print("SAREF: NGSI-LD")

    def show_element(self):
        print("Device")

    # def hasFunction(self, name):
    #     func = Function(name)
    #     print(func.show_element())


class FunctionRelated(Device):

    def show_element(self):
        print("FunctionRelated")


class Sensor(FunctionRelated):
    
    def __init__(self):
        self.rdf = None
    
    def show_element(self):
        print("Sensor")

    # def hasFunction(self, name):
    #     func = SensingFunction(name)
    #     print(func.show_element())

    def set_rdf(self, rdf):
        self.rdf = rdf
        print(rdf)


# ---------------------------------------------- #

class Saref:

    def __init__(self):
        self.sensor = Sensor()
        self.hasFunction = True
        self.sensingFunction = SensingFunction()
        
