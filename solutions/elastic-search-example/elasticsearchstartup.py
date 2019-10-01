from elasticsearch import Elasticsearch

import logging

es_object = None


def hi():
    print("hi")


# starting elasticsearch
def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def create_index(es_object, index_name='recipes'):
    created = False
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "salads": {
                "dynamic": "strict",
                "properties": {
                    "title": {
                        "type": "text"
                    },
                    "submitter": {
                        "type": "text"
                    },
                    "description": {
                        "type": "text"
                    },
                    "ready_in": {
                        "type": "text"
                    },
                    "calories": {
                        "type": "integer"
                    },
                    "ingredients": {
                        "type": "nested",
                        "properties": {
                            "step": {"type": "text"}
                        }
                    },
                    "directions": {
                        "type": "text"
                    }
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, body=settings)
            created = True
    except Exception as ex:
        print(ex)
    finally:
        return created


def delete_index(es_obj, index="salads"):
    if es_obj.indices.exists(index):
        es_obj.indices.delete(index=index)


def store_record(es_object, index_name="recipes", record=None, id=None):
    try:
        result = es_object.index(index=index_name, doc_type="salads", body=record, id=id)
        print(result)
    except Exception as ex:
        print(ex)


def main():
    logging.basicConfig(level=logging.INFO)
    es = connect_elasticsearch()
    global es_object
    es_object = es
    # delete_index(es,index="recipes")
    # delete_index(es,index="salads")
    # created = create_index(es)
    # print(created)


if __name__ == '__main__':
    main()


def search(es_obj, search_object, index="recipes"):
    return es_obj.search(index=index, body=search_object)
