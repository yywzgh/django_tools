
class Const:

    @staticmethod
    def redis_nodes_dict():

        return {"test": [
                    {'host': '10.25.16.253', 'port': 9701}, {'host': '10.25.16.253', 'port': 9702},
                    {'host': '10.25.16.253', 'port': 9703}, {'host': '10.25.16.253', 'port': 9704},
                    {'host': '10.25.16.253', 'port': 9705}, {'host': '10.25.16.253', 'port': 9706}
                ],
                "uat": [
                    {'host': '10.25.16.128', 'port': 6301}, {'host': '10.25.16.128', 'port': 6302},
                    {'host': '10.25.16.128', 'port': 6303}, {'host': '10.25.16.128', 'port': 6304},
                    {'host': '10.25.16.128', 'port': 6305}, {'host': '10.25.16.128', 'port': 6306}
                ],
                "pre": [
                    {'host': '10.25.15.211', 'port': 6379}, {'host': '10.25.15.211', 'port': 6380},
                    {'host': '10.25.15.212', 'port': 6379}, {'host': '10.25.15.212', 'port': 6380},
                    {'host': '10.25.15.213', 'port': 6379}, {'host': '10.25.15.213', 'port': 6380}
                ],
    }

    @staticmethod
    def mysql_nodes_dict():

        return {
                    "test": {"host": "10.25.16.253", "user": "root", "port": 3337, "password": "qazwsx123edc", "database": "jqd_test", "charset": "utf8"},
                    "uat": {"host": "10.25.16.128", "user": "root", "port": 3336, "password": "qazwsx123edc", "database": "jqd_test", "charset": "utf8"},
                    "pre": {"host": "10.25.15.196", "user": "root", "port": 3336, "password": "qazwsx123edc", "database": "jqd_pre", "charset": "utf8"},
                }