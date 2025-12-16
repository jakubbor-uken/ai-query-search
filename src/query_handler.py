import json
import logging
from ai_search import AISearch


class QueryHandler:
    """Class serving as an intermediary between high and low levels."""
    def __init__(self):
        logging.getLogger(__name__).init("QueryHandler initialized")
        self.ai_search = AISearch()
        self.db = None

    def load_database(self, path):
        """Load a JSON database from a file and store it in memory."""
        logging.getLogger(__name__).info(f"Loading database from: {path}")
        try:
            with open(path, 'r') as f:
                self.db = json.load(f)
                logging.getLogger(__name__).info(f"Database loaded successfully")

        # Path errors are operational issues, not programmer errors.
        except FileNotFoundError:
            logging.getLogger(__name__).error(f"Error: File not found at {path}")
            self.db = None

        # Indicates malformed input data.
        except json.JSONDecodeError:
            logging.getLogger(__name__).error(f"Error: Invalid JSON in {path}")
            self.db = None

    def send_query(self, query, model):
        """Execute a query with the currently loaded database using a model."""
        if self.db is None:
            # This is a programmer / workflow error, not a runtime failure.
            raise ValueError("Database was not read correctly, ensure correct path and format")

        logging.getLogger(__name__).info(f"Sending query to AI search: {query}")

        # Delegate actual computation/search to AISearch.
        result = self.ai_search.search(query, self.db, model)

        return result
