import os
import json
import sys
import common.cognitive_search as cognitive_search


def load_config(config_path):
    with open(config_path) as file:
        config = json.load(file)
    
    return config

def delete_index():
    azure_search_index_client.delete_index(
        config['index_name']
    )

def create_index():
    if config['index_name'] in azure_search_index_client.list_indexes():
        print("Updating index")
        azure_search_index_client.update_index(config['index_name'],
                                        config['fields'],
                                        config['semantic_config'],
                                        config['suggestor'],
                                        config['cors'],
                                        )
    else: 
        print("Creating index")
        azure_search_index_client.create_index(config['index_name'],
                                        config['fields'],
                                        config['semantic_config'],
                                        config['suggestor'],
                                        config['cors'],
                                        )




if __name__ == "__main__":
    config_directory=os.getenv('INDEX_CONFIG_PATH')
    config=load_config(config_directory)

    azure_search_client = cognitive_search.AzureIndexSearch(
            os.getenv('TF_VAR_SEARCH_SERVICE_NAME')
            , os.getenv('SEARCH_SERVICE_API_KEY')
        )
    
    globals()[sys.argv[1]]()

