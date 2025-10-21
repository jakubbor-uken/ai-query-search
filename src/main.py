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
    

    #Model list:
    #deepseek-ai/DeepSeek-V3-0324
    #moonshotai/Kimi-K2-Instruct-0905
    #meta-llama/Llama-3.1-8B-Instruct
    #openai/gpt-oss-20b:groq
    #CohereLabs/command-a-translate-08-2025:cohere
    #inclusionAI/Ling-1T:featherless-ai



    if len(sys.argv) < 2:
        raise ValueError("No query specified")

    query = sys.argv[1]
    print(f"Query: {query}")

    query_handler = QueryHandler()

    query_handler.load_database(os.environ["AI_DB_PATH"])
    query_handler.send_query(query, "inclusionAI/Ling-1T:featherless-ai")
    