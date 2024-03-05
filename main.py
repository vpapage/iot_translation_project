from iot_model_translator import IoTModelTranslator


def main():

    wot_to_ngsild = IoTModelTranslator("WoT", "data/wot_property_action.td.json")
    wot_to_ngsild.translate_wot_to_ngsild_data_model_and_save_to("data/results/ngsild-property-action-data-model.yaml")
    wot_to_ngsild.translate_and_save_to("data/results/ngsild-property-action.json")

    ngsild_to_wot = IoTModelTranslator("NGSI-LD", "examples/ngsild_property_action.json")
    ngsild_to_wot.translate_and_save_to("examples/results/wot_property_action.td.json")

    print("Main function displaying basic usage of the the project's capabilities")

if __name__ == "__main__":
    main()
