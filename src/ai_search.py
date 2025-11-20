import logging
import json
import pandas
from api_handler import ApiHandler


class AISearch():
    def __init__(self):
        logging.getLogger(__name__).init("AISearch initialized")
        self.api_handler = ApiHandler()


    def parse_msg(self, msg):
        parsed = None
        try:
            parsed = json.loads(msg)
        except Exception as X:
            logging.getLogger(__name__).info("Parsing failed at first clean try, running advanced parsing measures")

            parsed_msg = msg
            if '```json' in parsed_msg:
                logging.getLogger(__name__).info("Parser: Replacing \`\`\`json")
                parsed_msg = parsed_msg.replace("```json", "")
                parsed_msg = parsed_msg.replace("```", "")
                
            logging.getLogger(__name__).info(parsed_msg)
            parsed = json.loads(parsed_msg)


        logging.getLogger(__name__).info("Message after parsing:")
        logging.getLogger(__name__).info(parsed)

        return parsed

    def verify_values(self, msg):
        for idx, item in enumerate(msg):
            checked_val = int(msg[item]) # check if it's a number
            # check if the value is in correct bonds (0-100)
            if checked_val >= 0 and checked_val <= 100:
                continue
            else:
                raise Exception("Value was not in expected bounds:", msg[item])

        logging.getLogger(__name__).info("Values verified")
        return msg



    def get_response(self, query, db, model):
        response = self.api_handler.send_request(query, db, "huggingface", model)
        msg = response.choices[0].message.content
        logging.getLogger(__name__).info(msg)

        return msg


    def search(self, query, db, model):
        msg = self.get_response(query, db, model)

        try:
            msg = self.parse_msg(msg)
            msg = self.verify_values(msg)
        except Exception as X:
            logging.getLogger(__name__).error(X)

            #try 2nd time if first request failed
            msg = self.get_response(query, db, model)
            msg = self.parse_msg(msg)
            msg = self.verify_values(msg)

        return msg








