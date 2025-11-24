import logging
import os
from query_handler import QueryHandler

class AI_Analysis:
    def __init__(self):
        logging.getLogger(__name__).init("AI_Analysis initialized")

    def run_analysis(self, model_list, dbs_and_queries):
        logging.getLogger(__name__).info(f"Running analysis")
        query_handler = QueryHandler()

        output_list = []
        for i in range(0, len(model_list)):
            logging.getLogger(__name__).info(f"Loading model: {model_list[i]}")
            model = model_list[i]
            for j in range(0, len(dbs_and_queries)):
                query_handler.load_database(dbs_and_queries[j]["db"])
                query = dbs_and_queries[j]["query"]

                output = query_handler.send_query(query, model)
                output_list.append({"output": output['msg'], "model": model, "query": query, "elapsed_time": output['elapsed_time']})
                logging.getLogger(__name__).info(f"Added output for model: {model}, query: {query} to output_list")

        output_path = os.path.join(os.getcwd(), "output.log")
        logging.getLogger(__name__).info(f"Saving analysis results to file: {output_path}")
        
        with open(output_path, 'w') as f:
            for output in output_list:
                f.write(str(output) + '\n')
        
        return output_list
        

        
        

        
