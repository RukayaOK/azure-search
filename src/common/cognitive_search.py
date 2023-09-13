import os
import logging
import json
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient 
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (  
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,
    ComplexField,
    SearchIndex,  
    SemanticConfiguration,  
    PrioritizedFields,  
    SemanticField,  
    SemanticSettings,  
)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls] 

# https://github.com/Azure/azure-sdk-for-python/tree/azure-search-documents_11.3.0/sdk/search/azure-search-documents/samples
class AzureIndexSearch(metaclass=Singleton):
    def __init__(self, search_service_name, search_service_admin_key):
        self.service_name = search_service_name
        self.admin_key = search_service_admin_key
        self.endpoint = "https://{}.search.windows.net/".format(self.service_name)
        self.search_client = self.create_admin_client()
    
    def create_admin_client(self):
        admin_client = SearchIndexClient(endpoint=self.endpoint,
                        credential=AzureKeyCredential(self.admin_key))
        return admin_client
    
    def get_semantic_settings(self, semantic_config):
        prioritized_keywords_fields = []
        for prioritized_keywords_field in semantic_config['prioritized_fields']['prioritized_keywords_fields']:
            #print(prioritized_keywords_field)
            prioritized_keywords_fields.append(SemanticField(field_name=prioritized_keywords_field))

        prioritized_content_fields = []
        for prioritized_content_field in semantic_config['prioritized_fields']['prioritized_content_fields']:
            #print(prioritized_content_field)
            prioritized_content_fields.append(SemanticField(field_name=prioritized_content_field))

        # semantic config
        semantic_config = SemanticConfiguration(
            name=semantic_config['name'],
            prioritized_fields=PrioritizedFields(
                title_field=SemanticField(field_name=semantic_config['prioritized_fields']['title_field']),
                prioritized_keywords_fields=prioritized_keywords_fields,
                prioritized_content_fields=prioritized_content_fields
            ))

        return SemanticSettings(configurations=[semantic_config])
    
    def get_index_fields(self, fields):
        index_fields = []
        for simple_field in fields['simple_fields']:
            if simple_field['type'] == 'String':
                type=SearchFieldDataType.String
            elif simple_field['type'] == 'Boolean':
                type=SearchFieldDataType.Boolean
            elif simple_field['type'] == 'DateTimeOffset':
                type=SearchFieldDataType.DateTimeOffset
            elif simple_field['type'] == 'Double':
                type=SearchFieldDataType.Double

            index_fields.append(
                SimpleField(
                    name=simple_field['name'],
                    type=type,
                    analyzer_name=simple_field['analyzer_name'],
                    facetable=simple_field['facetable'],
                    filterable=simple_field['filterable'],
                    sortable=simple_field['sortable'],
                    key=simple_field['key'],
                )
            )
        
        for seachable_field in fields['seachable_fields']:
            if seachable_field['type'] == 'String':
                type=SearchFieldDataType.String
            elif seachable_field['type'] == 'Boolean':
                type=SearchFieldDataType.Boolean
            elif seachable_field['type'] == 'DateTimeOffset':
                type=SearchFieldDataType.DateTimeOffset
            elif seachable_field['type'] == 'Double':
                type=SearchFieldDataType.Double
                         
            index_fields.append(
                SearchableField(
                    name=seachable_field['name'],
                    type = type,   
                    analyzer_name=seachable_field['analyzer_name'],
                    facetable=seachable_field['facetable'],
                    filterable=seachable_field['filterable'],
                    sortable=seachable_field['sortable'],
                    key=seachable_field['key'],
                )
            )
        
        for complex_field in fields['complex_fields']:
            complex_fields = []
            for field in complex_field['fields']:
                if field['type'] == 'String':
                    type=SearchFieldDataType.String
                elif field['type'] == 'Boolean':
                    type=SearchFieldDataType.Boolean
                elif field['type'] == 'DateTimeOffset':
                    type=SearchFieldDataType.DateTimeOffset
                elif field['type'] == 'Double':
                    type=SearchFieldDataType.Double
                complex_fields.append(SearchableField(
                    name=field['name'],
                    type=type,
                    analyzer_name=field['analyzer_name'],
                    facetable=field['facetable'],
                    filterable=field['filterable'],
                    sortable=field['sortable'],
                    key=field['key'],
                ))
            index_fields.append(
                ComplexField(name=complex_field['name'],
                         fields=complex_fields))
        
        return index_fields


    def create_index(self, index_name, fields, semantic_config, suggester, cors_options, scoring_profiles=[]):
        if semantic_config or len(semantic_config) == 0:
            semantic_config = self.get_semantic_settings(semantic_config)
        else: 
            semantic_config = None
        
        if fields or len(fields) == 0:
            fields = self.get_index_fields(fields)
        
        index = SearchIndex(
            name=index_name,
            fields=fields,
            semantic_settings=semantic_config,
            scoring_profiles=scoring_profiles,
            suggesters = suggester,
            cors_options=cors_options
            )

        try:
            result = self.search_client.create_index(index)
            logging.info('Index', result.name, 'created')
            return result
        except Exception as ex:
            logging.error(ex)

    def list_indexes(self):
        try:
            result = self.search_client.list_index_names()
            logging.info('Indexes retrieved:', result)
            return result
        except Exception as ex:
            logging.error(ex)

    def get_index(self, index_name): 
        try:
            result = self.search_client.get_index(index_name)
            logging.info('Index', result.name, 'retrieved')
            return result
        except Exception as ex:
            logging.error(ex)

    def update_index(self, index_name, fields, semantic_config, suggester, cors_options, scoring_profiles=[]):
        
        if semantic_config or len(semantic_config) == 0:
            semantic_config = self.get_semantic_settings(semantic_config)
        else: 
            semantic_config = None
        
        if fields or len(fields) == 0:
            fields = self.get_index_fields(fields)
        
        index = SearchIndex(
            name=index_name,
            fields=fields,
            semantic_settings=semantic_config,
            scoring_profiles=scoring_profiles,
            suggesters = suggester,
            cors_options=cors_options
            )

        try:
            result = self.search_client.create_or_update_index(index)
            logging.info('Index', result.name, 'created')
            return result
        except Exception as ex:
            logging.error(ex) 

    def delete_index(self, index_name):
        try:
            result = self.search_client.delete_index(index_name)
            logging.info('Index', index_name, 'Deleted')
            return result
        except Exception as ex:
            logging.error(ex) 
        

class AzureSearch(metaclass=Singleton):
    def __init__(self, search_service_name, search_service_admin_key, index_name):
        self.service_name = search_service_name
        self.admin_key = search_service_admin_key
        self.index_name = index_name
        self.endpoint = "https://{}.search.windows.net/".format(self.service_name)
        self.search_client = self.create_search_client()
    
    def create_search_client(self):
        search_client = SearchClient(endpoint=self.endpoint,
                        index_name=self.index_name,
                        credential=AzureKeyCredential(self.admin_key))
        return search_client

    def get_document(self, key):
        result = self.search_client.get_document(key=key)
        return result
    
    def upload_documents(self, documents):
        result = self.search_client.upload_documents(documents=documents)
        
        logging.info("Upload of new document succeeded: {}".format(result[0].succeeded))
        return result
    
    def bulk_upload_documents(self, batch_size, mapped_documents):
        #batch_array = []
        count = 0
        batch_counter = 0
        for i in mapped_documents:
            count += 1

            # In this sample, we limit batches to 1000 records.
            # When the counter hits a number divisible by 1000, the batch is sent.
            if count % batch_size == 0:
                self.search_client.upload_documents(documents=mapped_documents)
                batch_counter += 1
                print(f"Batch sent! - #{batch_counter}")
                mapped_documents = []

        # This will catch any records left over, when not divisible by 1000
        if len(mapped_documents) > 0:
            self.search_client.upload_documents(documents=mapped_documents)
            batch_counter += 1
            print(f"Final batch sent! - #{batch_counter}")

        print("Done!")

    def merge_documents(self, documents):
        result = self.search_client.merge_documents(documents=documents)

        logging.info("Merge into new document succeeded: {}".format(result[0].succeeded))
        # [END merge_document]
        return result

    def delete_document(self, documents):
        # [START delete_document]
        result = self.search_client.delete_documents(documents=documents)

        logging.info("Delete new document succeeded: {}".format(result[0].succeeded))
        return result

    def simple_query(self, search_text, search_fields=None, select=None, include_total_count=True, query_language="en-gb", facets=None, filter=None, order_by=None):

        results = self.search_client.search(
            query_type="simple",
            query_language=query_language,
            search_text=search_text,
            search_fields=search_fields,
            select=select,
            include_total_count=include_total_count,
            # semantic_configuration_name=semantic_configuration_name,
            # query_caption=query_caption,
            # query_answer=query_answer,
            facets=facets,
            filter=filter,
            order_by=order_by
        )

        logging.info(f"Item containing {search_text} in the name (or other fields)")
        
        return results
    
    def semantic_query(self, search_text, search_fields=None, select=None, include_total_count=True, query_language="en-gb", facets=None, semantic_configuration_name=None, query_caption=None, query_answer=None, filter=None, order_by=None):
        results = self.search_client.search(
            query_type="semantic",
            query_language=query_language,
            search_text=search_text,
            search_fields=search_fields,
            select=select,
            include_total_count=include_total_count,
            semantic_configuration_name=semantic_configuration_name,
            query_caption=query_caption,
            query_answer=query_answer,
            facets=facets,
            filter=filter,
            order_by=order_by
        )

        logging.info(f"Item containing {search_text} in the name (or other fields)")
        
        return results 

    def autocomplete(self, search_text, suggester_name, mode):
        results = self.search_client.autocomplete(
            search_text=search_text,
            suggester_name=suggester_name,
            mode=mode
        )

        logging.info(f"Items suggested from text: {search_text} in fields:")
        
        return results

