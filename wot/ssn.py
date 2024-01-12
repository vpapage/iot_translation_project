class PhysicalObject:

    def show_ontology(self):
        print("SSN: Web of Things")

    def show_element(self):
        print("PhysicalObject")


class System(PhysicalObject):
    
    def show_element(self):
        print("System")


class Device(System):
    
    def show_element(self):
        print("Device")


# ---------------------------------------------- #


class Sensor(PhysicalObject):
    
    def show_element(self):
        print("Sensor")


class SensingDevice(Device, Sensor):
    
    def show_element(self):
        print("SensingDevice")


