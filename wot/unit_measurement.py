assumption_about_the_available_measurement_units = {
    # Physical Quantities
    "Temperature": ['celsius', 'fahrenheit', 'kelvin'],
    "Distance": ['meters', 'kilometers'],
    "Weight-Mass": ['grams', 'kilograms', 'pounds'],
    "Volume": ['liters', 'milliliters', 'cubic meters'],
    "Speed": ['meters per second', 'kilometers per hour', 'miles per hour'],
    "Pressure": ['pascals', 'bar', 'atmospheres'],
    "Energy": ['joules','calories'],
    # Electrical Quantities
    "Power": ['watts', 'kilowatts'],
    # Time
    "Time": ['seconds', 'minutes', 'hours', 'days'],
}


# Translation from NGSI-LD to WoT

units = {
    # Temperature
    "CEL": "celsius",
    "FAH": "fahrenheit",
    "K": "kelvin",

    # Length/Distance
    "m": "meters",
    "km": "kilometers",

    # Mass/Weight
    "kg": "kilograms",
    "g": "grams",
    "lb": "pounds",

    # Volume
    "l": "liters",
    "L": "liters",
    "ml": "milliliters",
    "mL": "milliliters",
    "m3": "cubic meters",

    # Time
    "s": "seconds",
    "min": "minutes",
    "h": "hours",
    "d": "days",

    # Pressure
    "Pa": "pascals",
    "bar": "bar",
    "atm": "atmospheres",

    # Speed 
    "m/s": "meters per second",
    "km/h": "kilometers per hour",
    "mph": "miles per hour",

    # Energy
    "J": "joules",
    "cal": "calories",

    # Power
    "W": "Watts",
    "kW": "kilowatts",

}

def find_type(value):
    data_class = type(value)
    if  value is None:
        return "null"
    elif data_class=="<class 'int'>" or data_class=="<class 'float'>":
        return "number"
    elif data_class=="<class 'str'>": 
        return "string"
    elif data_class=="<class 'bool'>":
        return "boolean"
    elif data_class=="<class 'list'>":
        return "array"
    elif data_class=="<class 'dict'>":
        return "object"
    else:
        return "unknown"

def find_unit(unitCode):
    return units.get(unitCode)



# Translation from WoT to NGSI-LD 

unitCode = {
    # Temperature
    "celsius": "CEL",
    "fahrenheit": "FAH",
    "kelvin": "K",

    # Length/Distance
    "meters": "m",
    "kilometers": "km",

    # Mass/Weight
    "kilograms": "kg",
    "grams": "g",
    "pounds": "lb",

    # Volume
    "liters": "l",
    "liters": "L",
    "milliliters": "ml",
    "milliliters": "mL",
    "cubic meters": "m3",

    # Time
    "seconds": "s",
    "minutes": "min",
    "hours": "h",
    "days": "d",

    # Pressure
    "pascals": "Pa",
    "bar": "bar",
    "atmospheres": "atm",

    # Speed 
    "meters per second": "m/s",
    "kilometers per hour": "km/h",
    "miles per hour": "mph",

    # Energy
    "joules": "J",
    "calories": "cal",

    # Power
    "Watts": "W",
    "kilowatts": "kW",

}

def find_unitCode(units):
    return unitCode.get(units)