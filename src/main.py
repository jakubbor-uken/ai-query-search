import sys
import os
import logging

from logger import Logger
from query_handler import QueryHandler
from ai_analysis import AI_Analysis    







if __name__ == '__main__':
    logs = Logger()
    
    #Load enviroment variables for api keys:
    if "AI_API_KEYS" not in os.environ:
        os.environ["AI_API_KEYS"] = os.getcwd() + "/api_keys.json"

    logging.getLogger(__name__).info(f"API keys path: {os.environ['AI_API_KEYS']}")


    #Test configuration
    model_list = [
        "deepseek-ai/DeepSeek-V3-0324",
        "moonshotai/Kimi-K2-Instruct-0905",
        # "meta-llama/Llama-3.1-8B-Instruct", //Removed because of inconsistent results
        "openai/gpt-oss-20b:groq",
        "CohereLabs/command-a-translate-08-2025:cohere",
        "inclusionAI/Ling-1T:featherless-ai"
    ]

    dbs_and_queries = [
        {"query": "Znajdź buty o najmniejszej cenie", "db": os.getcwd() + "/databases/db_buty.json"},
        {"query": "Znajdź narzędzia kuchenne", "db": os.getcwd() + "/databases/db_kuchnia.json"},
        {"query": "Znajdź najbardziej wydajny laptop", "db": os.getcwd() + "/databases/db_laptopy.json"},
        {"query": "Znajdź wakacje które są najbliżej Polski", "db": os.getcwd() + "/databases/db_wakacje.json"}
    ]

    analyzer = AI_Analysis()
    analyzer.run_analysis(model_list, dbs_and_queries)








    #Load user query (testing)
    # if len(sys.argv) < 2:
    #     raise ValueError("No query specified")

    # query = sys.argv[1]
    # logging.getLogger(__name__).info(f"Query: {query}")


    # query_handler = QueryHandler()

    # query_handler.load_database(os.environ["AI_DB_PATH"])
    # query_handler.send_query(query, "deepseek-ai/DeepSeek-V3-0324")
    