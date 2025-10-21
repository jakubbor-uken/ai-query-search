import sys
import os

from query_handler import QueryHandler

    

if __name__ == '__main__':
    
    if "AI_SEARCH_PATH" not in os.environ:
        os.environ["AI_SEARCH_PATH"] = os.getcwd() + "/api_keys.json"

    print("Execution path:", os.environ["AI_SEARCH_PATH"])
    




    if len(sys.argv) < 2:
        raise ValueError("No query specified")

    query = sys.argv[1]
    print(f"Query: {query}")

    query_handler = QueryHandler()
    query_handler.send_query(query)
    