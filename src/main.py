import sys
import os

from query_handler import QueryHandler

    

if __name__ == '__main__':
    
    #Load enviroment variables for:
    #api keys:
    if "AI_API_KEYS" not in os.environ:
        os.environ["AI_API_KEYS"] = os.getcwd() + "/api_keys.json"

    print("API keys path:", os.environ["AI_API_KEYS"])

    #database path:
    if "AI_DB_PATH" not in os.environ:
        os.environ["AI_DB_PATH"] = os.getcwd() + "/db.json"

    print("Database path:", os.environ["AI_DB_PATH"])
    




    if len(sys.argv) < 2:
        raise ValueError("No query specified")

    query = sys.argv[1]
    print(f"Query: {query}")

    query_handler = QueryHandler()

    query_handler.load_database(os.environ["AI_DB_PATH"])
    query_handler.send_query(query)
    