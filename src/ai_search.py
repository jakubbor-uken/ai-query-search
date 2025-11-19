import logging
import json
from api_handler import ApiHandler


class AISearch():
    def __init__(self):
        logging.getLogger(__name__).init("AISearch initialized")
        self.api_handler = ApiHandler()


    def parseMsg(self, msg):
        parsed = None
        try:
            parsed = json.loads(msg)
        except Exception as X:
            logging.getLogger(__name__).info("Parsing failed at first clean try, running advanced parsing measures")

            parsedMsg = msg
            if '```json' in parsedMsg:
                logging.getLogger(__name__).info("Parser: Replacing \`\`\`json")
                parsedMsg = parsedMsg.replace("```json", "")
                parsedMsg = parsedMsg.replace("```", "")
                
            logging.getLogger(__name__).info(parsedMsg)
            parsed = json.loads(parsedMsg)


        logging.getLogger(__name__).info("Message after parsing:")
        logging.getLogger(__name__).info(parsed)

        return parsed



    def search(self, query, db, model):
        response = self.api_handler.send_request(query, db, "huggingface", model)
        msg = response.choices[0].message.content
        logging.getLogger(__name__).info(msg)

        msg = self.parseMsg(msg)
        return msg








