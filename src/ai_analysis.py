import logging
import os
from query_handler import QueryHandler

class AI_Analysis:
    """Class responsible for high level management of models, queries with their databases and outputs.

    It iterates over each model, sending queries to it with databases attached to them.
    After, it collects the overall output and prints it to file.
    """
    def __init__(self):
        logging.getLogger(__name__).init("AI_Analysis initialized")

    def run_analysis(self, model_list, dbs_and_queries):
        """Execute analysis for all model and database/query combinations."""
        logging.getLogger(__name__).info(f"Running analysis")
        query_handler = QueryHandler()

        output_list = []

        # Iterate over models
        for i in range(0, len(model_list)):

            logging.getLogger(__name__).info(f"Loading model: {model_list[i]}")
            model = model_list[i]

            # Iterate over queries/databases
            for j in range(0, len(dbs_and_queries)):

                # databases are loaded from json files
                query_handler.load_database(dbs_and_queries[j]["db"])
                query = dbs_and_queries[j]["query"]

                # delegate actual search to QueryHandler
                output = query_handler.send_query(query, model)

                # these records will be written as they are to a file
                output_list.append(
                    {"output": output['msg'],
                     "model": model,
                     "query": query,
                     "elapsed_time": output['elapsed_time']
                     }
                )

                logging.getLogger(__name__).info(f"Added output for model: {model}, query: {query} to output_list")

        # Save all results to a file
        output_path = os.path.join(os.getcwd(), "output.log")
        logging.getLogger(__name__).info(f"Saving analysis results to file: {output_path}")
        
        with open(output_path, 'w') as f:
            for output in output_list:
                f.write(str(output) + '\n')
        
        return output_list
        

        
        

        
