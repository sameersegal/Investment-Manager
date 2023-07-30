import openai
from pymilvus import (
    connections,
    Collection,
)

def get_embedding(text):
    response = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=text)
    return response["data"][0]["embedding"]


def search(query: str, **kwargs):

    connections.connect('default', host='localhost', port='19530')
    collection_name = 'malkauns'
    collection = Collection(collection_name)
    collection.load()

    search_params = {
        "metric_type": "L2"
    }

    results = collection.search(
        data=[get_embedding(query)],  # Embeded search value
        anns_field="embeddings",  # Search across embeddings
        param=search_params,
        limit=5,  # Limit to five results per search
        output_fields=['id', 'title', 'url', 'body',
                       'date']  # Include title field in result
    )

    ret = []
    for hit in results[0]:
        row = {
            "id": hit.id,
            "score": hit.score,
            "title": hit.entity.get('title'),
            "url": hit.entity.get('url'),
            "date": hit.entity.get('date'),
            "body": hit.entity.get('body')
        }
        ret.append(row)
    return ret
