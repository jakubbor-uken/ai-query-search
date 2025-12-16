import logging
import json
from timeit import default_timer as timer

from api_handler import ApiHandler


class AISearch():
    def __init__(self):
        logging.getLogger(__name__).init("AISearch initialized")
        self.api_handler = ApiHandler()

    def parse_msg(self, msg):
        """Parse model output into Python objects (expected: JSON)."""
        parsed = None
        try:
            parsed = json.loads(msg)

        # model failed and has not given us what we expected (json format)
        except Exception as X:
            logging.getLogger(__name__).info("Parsing failed at first clean try, running advanced parsing measures")

            # model could, however, give us json enclosed in characters as below
            parsed_msg = msg
            if '```json' in parsed_msg:
                logging.getLogger(__name__).info("Parser: Replacing \`\`\`json")

                # here we strip this common formatting
                parsed_msg = parsed_msg.replace("```json", "")
                parsed_msg = parsed_msg.replace("```", "")
                
            logging.getLogger(__name__).info(parsed_msg)
            parsed = json.loads(parsed_msg)


        logging.getLogger(__name__).info("Message after parsing:")
        logging.getLogger(__name__).info(parsed)

        return parsed

    def verify_values(self, msg):
        """Validate parsed output values."""
        for idx, item in enumerate(msg):
            checked_val = int(msg[item]) # check if it's a number

            # check if the value is in correct bonds (0-100),
            # this is the expected scope of priorities values
            if checked_val >= 0 and checked_val <= 100:
                continue
            else:
                raise Exception("Value was not in expected bounds:", msg[item])

        logging.getLogger(__name__).info("Values verified")
        return msg



    def get_response(self, query, db, model):
        """Wrapper for sending query."""
        response = self.api_handler.send_request(query, db, "huggingface", model)
        msg = response.choices[0].message.content
        logging.getLogger(__name__).info(msg)

        return msg


    def search(self, query, db, model):
        """Full search pipeline.

        Consists of:
            - measuring time for one model call
            - parsing json
            - validating values
            - retry query upon failure
        """

        # we measure the time it takes to process our queries
        # they will be compared between models
        start = timer()
        msg = self.get_response(query, db, model)
        end = timer()
        elapsed_time = round(end - start, 3)  # rounds to 3 decimal places (0.001 precision)

        try:
            msg = self.parse_msg(msg)
            msg = self.verify_values(msg)
        except Exception as X:
            logging.getLogger(__name__).error(X)

            # try 2nd time if first request failed
            msg = self.get_response(query, db, model)
            msg = self.parse_msg(msg)
            msg = self.verify_values(msg)

        return {"msg": msg, "elapsed_time": elapsed_time}
