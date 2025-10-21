import json
from ai_search import AISearch


class QueryHandler:
    def __init__(self):
        print("QueryHandler initialized")
        self.ai_search = AISearch()
        self.db = None


    def load_database(self, path):
        print(f"Loading database from: {path}")
        try:
            with open(path, 'r') as f:
                self.db = json.load(f)
                print(f"Database loaded successfully")
        except FileNotFoundError:
            print(f"Error: File not found at {path}")
            self.db = None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {path}")
            self.db = None

    def send_query(self, query):
        if (self.db is None):
            raise ValueError("Database was not read correctly, ensure correct path and format")

        print("Sending query to AI search:", query)
        self.ai_search.search(query, self.db)
