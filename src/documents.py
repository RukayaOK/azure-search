import config
import json 
import sys
import os
import common.cognitive_search as cognitive_search

def load_config(config_path):
    with open(config_path) as file:
        config = json.load(file)
    
    return config

def upload_documents(data_directory):
    data=[]
    for filename in os.listdir(data_directory):
        with open(os.path.join(data_directory, filename)) as file:
            data.append(json.load(file))
    
    azure_search_client.upload_documents(documents=data)

"""
# Map documents to index
mapped_documents = []
for document in sample_data:
    mapped_documents = {
        "HotelId": str(document["HotelId"]),
        "HotelName": int(document["HotelName"]),
        "Description": int(document["Description"]),
        "Description_fr": int(document["Description_fr"]),
        "Category": document["Category"] if document["books_count"] else 0,
        "ParkingIncluded": str(document["ParkingIncluded"]),
        "LastRenovationDate": str(document["LastRenovationDate"]),
        "Rating": document["authors"].split(",") if document["authors"] else None,
        "Address": document["original_publication_year"]
    }
"""

if __name__ == "__main__":
    config_directory=os.getenv('INDEX_CONFIG_PATH')
    config=load_config(config_directory)
    
    azure_search_client = cognitive_search.AzureSearch(
        os.getenv('TF_VAR_SEARCH_SERVICE_NAME')
        , os.getenv('SEARCH_SERVICE_API_KEY')
        , config['index_name']
    )

    if sys.argv[1] == 'upload_documents':
        data_directory=os.getenv('DATA_DIRECTORY')
        upload_documents(data_directory)
    else:
        pass