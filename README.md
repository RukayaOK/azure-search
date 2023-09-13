# Learn Azure Cognitive Search 


## Useful Links

Quick Starts:
https://github.com/Azure-Samples/azure-search-python-samples/

RBAC:
- https://techcommunity.microsoft.com/t5/azure-ai-services-blog/secure-your-azure-cognitive-search-indexes-and-queries-with/ba-p/2973033

Semantic Search:
- https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Semantic-Search/semantic-search-quickstart.ipynb
- https://learn.microsoft.com/en-us/azure/search/semantic-search-overview
- https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-request?tabs=portal%2Cportal-query
- https://learn.microsoft.com/en-us/azure/search/semantic-search-overview#how-semantic-ranking-works
- https://learn.microsoft.com/en-us/azure/search/index-ranking-similarity

Indexer:
https://blog.novanet.no/writing-an-azure-cognitive-search-indexer/

API:
https://learn.microsoft.com/en-us/rest/api/searchservice/addupdate-or-delete-documents
```
@search.action	Required. Valid values are "upload", "delete", "merge", or "mergeOrUpload". Defaults to "upload". You can combine actions, one per document, in the same batch.

"upload": An upload action is similar to an 'upsert' where the document will be inserted if it's new and updated/replaced if it exists. All fields are replaced in the update case.

"delete": Delete removes the specified document from the index. Any field you specify in a delete operation, other than the key field, will be ignored. If you want to remove an individual field from a document, use merge instead and set the field explicitly to null.

"mergeOrUpload": This action behaves like merge if a document with the given key already exists in the index. If the document doesn't exist, it behaves like upload with a new document.

"merge": Merge updates an existing document with the specified fields. If the document doesn't exist, the merge fails. Any field you specify in a merge will replace the existing field in the document. This also applies to collections of primitive and complex types.

In primitive collections, if the document contains a Tags field of type Collection(Edm.String) with a value of ["budget"], and you execute a merge with a value of ["economy", "pool"] for Tag, the final value of the Tags field will be ["economy", "pool"]. It will not be ["budget", "economy", "pool"].

In complex collections, if the document contains a complex collection field named Rooms with a value of [{ "Type": "Budget Room", "BaseRate": 75.0 }], and you execute a merge with a value of [{ "Type": "Standard Room" }, { "Type": "Budget Room", "BaseRate": 60.5 }], the final value of the Rooms field will be [{ "Type": "Standard Room" }, { "Type": "Budget Room", "BaseRate": 60.5 }]. It will not be either of the following:
[{ "Type": "Budget Room", "BaseRate": 75.0 }, { "Type": "Standard Room" }, { "Type": "Budget Room", "BaseRate": 60.5 }] (append elements)
[{ "Type": "Standard Room", "BaseRate": 75.0 }, { "Type": "Budget Room", "BaseRate": 60.5 }] (merge elements in order, then append any extras)
```

Search Vectors
https://github.com/Azure/cognitive-search-vector-pr/tree/main/demo-python

