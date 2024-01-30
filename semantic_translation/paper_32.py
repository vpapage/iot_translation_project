import ngsi_ld.saref
import wot.ssn

def m01(ssn_sensingDevice):
    """
        1 IN: ssn_sensingDevice
        2 var saref_sensor = saref:Sensor
        3 saref_sensor.rdfs = ssn_sensingDevice.rdfs
        4 var saref_function = saref:SensingFunction
        5 var saref_hasFunction = saref:hasFunction
        6 createTriple ( saref_sensor saref_hasFunction saref_function )
    """
    saref = saref.Saref()
    saref_sensor = saref.sensor()
    saref_sensor.set_rdf(ssn_sensingDevice.rdf)
    saref_function = saref.SensingFunction()
    saref_has_function = saref.SensingHasFunction()
    return saref_sensor, saref_has_function, saref_function
    
def m02(ssn_sensingDevice, saref_sensor):
    """
        1 IN: ssn_sensingDevice , saref_sensor
        2 for each ssn_system in ssn_sensingDevice.ssn:hasSubSystem
        3   var saref_device_component = saref:Device

        5   if ssn_system is ssn:SensingDevice then
        6       saref_device_component = Map( M01 , ssn_system )

        7   else if ssn_system is ssn:Device then
        8       saref_device_component.rdfs = ssn_system.rdfs

        10  var saref_consistsOf = saref:consistsOf
        11  createTriple ( saref_sensor saref_consistsOf saref_device_component )

        12 end for
    """
    for ssn_system in ssn_sensingDevice.hasSubSystem:
        saref_device_component = saref.Device
    
    
def m03(ssn_sensingDevice , saref_sensor):
    """
        1 IN: ssn_sensingDevice , saref_sensor
        2 for each p in ssn_sensingDevice.observes
        3   var ssn_property = p
        4   var saref_property = saref:Property
        5   saref_property = GetPropertyInSAREF ( ssn_property )
        6
        7   if not isnull ( saref_property ) then
        8       saref_property.rdfs = ssn_property.rdfs
        9
        10  var saref_measuresProperty = saref:measuresProperty
        11  var saref_sensor saref_measuresProperty saref_property
        12  var saref_isMeasuredByDevice = saref:isMeasuredByDevice
        13  createTriple ( saref_property saref_isMeasuredByDevice saref_sensor )
        14 end for
    """
