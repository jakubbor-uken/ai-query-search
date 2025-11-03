import json
import logging
from ai_search import AISearch


class QueryHandler:
    def __init__(self):
        logging.getLogger(__name__).init("QueryHandler initialized")
        self.ai_search = AISearch()
        self.db = None


    def load_database(self, path):
        logging.getLogger(__name__).info(f"Loading database from: {path}")
        try:
            with open(path, 'r') as f:
                self.db = json.load(f)
                logging.getLogger(__name__).info(f"Database loaded successfully")
        except FileNotFoundError:
            logging.getLogger(__name__).error(f"Error: File not found at {path}")
            self.db = None
        except json.JSONDecodeError:
            logging.getLogger(__name__).error(f"Error: Invalid JSON in {path}")
            self.db = None

    def send_query(self, query, model):
        if (self.db is None):
            raise ValueError("Database was not read correctly, ensure correct path and format")

        logging.getLogger(__name__).info(f"Sending query to AI search: {query}")
        result = self.ai_search.search(query, self.db, model)
        return result
