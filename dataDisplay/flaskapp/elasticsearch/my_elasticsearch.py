# -*- coding: utf-8 -*-
"""
# @Time    :2017/11/1 上午9:49
# @Author  :Xuxian
"""
from elasticsearch import Elasticsearch

es = Elasticsearch()

# es.index(index='index_1', doc_type='test_type_1',  body={"name": "苏州昆山", "addr":"工业技术大学"})


"""
查询
"""


def fulltext_search(keyword):
    _query_name_contains = {
        "query": {
            "match": {
                "_all": {
                    "query": keyword,
                    "operator": "and"
                }
            }
        }
    }

    _searched = es.search(body=_query_name_contains)
    #
    # print _searched
    # source = _searched['hits']['hits'][0]
    # print source[u'_source']
    return _searched