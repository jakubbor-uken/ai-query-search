from ai_search import AISearch


class QueryHandler:
    def __init__(self):
        self.aisearch = AISearch()

    def send_query(self, query):
        print("Sending query to AI search:", query)
        AISearch.ai_search(query)
