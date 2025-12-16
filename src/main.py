import os
import logging

from logger import Logger
from ai_analysis import AI_Analysis


if __name__ == '__main__':
    """Hierarchy of our project's encapsulation is as follows:
    
    main
      └── ai_analysis
            └── query_handler
                  └── ai_search
                        └── api_handler
            
    with each of them using logger
    """
    logs = Logger()
    
    # Load enviroment variables for api keys:
    if "AI_API_KEYS" not in os.environ:
        os.environ["AI_API_KEYS"] = os.getcwd() + "/api_keys.json"

    logging.getLogger(__name__).info(f"API keys path: {os.environ['AI_API_KEYS']}")

    # Test configuration
    model_list = [
        # "meta-llama/Llama-3.1-8B-Instruct", # Removed because of inconsistent results
        "deepseek-ai/DeepSeek-V3-0324",
        "moonshotai/Kimi-K2-Instruct-0905",
        "openai/gpt-oss-20b:groq",
        # "CohereLabs/command-a-translate-08-2025:cohere", # Not used in target database tests for dbs bigger than 50 records
        # "inclusionAI/Ling-1T:featherless-ai" # Not used in target database tests for dbs bigger than 200 records
    ]

    dbs_and_queries = [
        # {"query": "Znajdź buty o najmniejszej cenie", "db": os.getcwd() + "/databases/db_buty.json"},
        # {"query": "Znajdź narzędzia kuchenne", "db": os.getcwd() + "/databases/db_kuchnia.json"},
        # {"query": "Znajdź najbardziej wydajny laptop", "db": os.getcwd() + "/databases/db_laptopy.json"},
        # {"query": "Znajdź wakacje które są najbliżej Polski", "db": os.getcwd() + "/databases/db_wakacje.json"}

        # Target database tests
        # {"query": "Znajdź dzieła wykonane w trakcie wojny w danym państwie", "db": os.getcwd() + "/databases/sampledb50.json"},
        # {"query": "Znajdź dzieła wykonane w trakcie wojny w danym państwie", "db": os.getcwd() + "/databases/sampledb100.json"},
        # {"query": "Znajdź dzieła wykonane w trakcie wojny w danym państwie", "db": os.getcwd() + "/databases/sampledb200.json"},
        # {"query": "Znajdź dzieła wykonane w trakcie wojny w danym państwie", "db": os.getcwd() + "/databases/sampledb500.json"},
        # {"query": "Znajdź dzieła wykonane w trakcie wojny w danym państwie", "db": os.getcwd() + "/databases/sampledb.json"},

        # {"query": "Znajdź dzieła które są łatwopalne", "db": os.getcwd() + "/databases/sampledb50.json"},
        # {"query": "Znajdź dzieła które są łatwopalne", "db": os.getcwd() + "/databases/sampledb100.json"},
        # {"query": "Znajdź dzieła które są łatwopalne", "db": os.getcwd() + "/databases/sampledb200.json"},
        # {"query": "Znajdź dzieła które są łatwopalne", "db": os.getcwd() + "/databases/sampledb500.json"},
        # {"query": "Znajdź dzieła które są łatwopalne", "db": os.getcwd() + "/databases/sampledb.json"},

        # {"query": "Znajdź dzieła przedstawiające ludzi", "db": os.getcwd() + "/databases/sampledb50.json"},
        # {"query": "Znajdź dzieła przedstawiające ludzi", "db": os.getcwd() + "/databases/sampledb100.json"},
        # {"query": "Znajdź dzieła przedstawiające ludzi", "db": os.getcwd() + "/databases/sampledb200.json"},
        # {"query": "Znajdź dzieła przedstawiające ludzi", "db": os.getcwd() + "/databases/sampledb500.json"},
        {"query": "Znajdź dzieła przedstawiające ludzi", "db": os.getcwd() + "/databases/sampledb.json"},

    ]

    analyzer = AI_Analysis()
    analyzer.run_analysis(model_list, dbs_and_queries)
