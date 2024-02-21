 
components_tamplate = {
  "components": {
    "schemas": {
      "Data_model_name": {
        "description": "'Give a description of your data model, its scope and what it is used for.'",
        "properties": {
          "Entity 1": {
            "description": "'Description of entity 1'",
            "minimum": "0",
            "maximum": "1",
            "type": "e.g array, boolean, integer, number, object, string"
          },
          "Entity N": {
            "description": "'Description of entity N'",
            "type": "e.g array, boolean, integer, number, object, string"
          }
        }
      }
    }
  },
  "info": {
    "description": "'Base Model Definitions from Smart Data Models'",
    "title": "Data model title",
    "version": "1.0.0"
  },
  "openapi": '3.0.0'
}

paths_tamplate = {
  "paths": {
    "/ngsi-ld/v1/entities": {
      "get": {
        "responses": {
          "200": {
            "description": "'OK'",
            "content": {"application/ld+json":{"schema": {"type": "object"}}}
          },
          "400": {
            "description": "'Invalid input'"
          },
          "422": {
            "description": "'Validation exception'"
          }
        }
      }
    }
  }
}


yaml_tamplate = [ components_tamplate, paths_tamplate]