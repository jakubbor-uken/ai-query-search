import logging
from api_handler import ApiHandler



class AISearch():
    def __init__(self):
        logging.getLogger(__name__).init("AISearch initialized")
        self.api_handler = ApiHandler()


    def search(self, query, db, model):
        response = self.api_handler.send_request(query, db, "huggingface", model)
        msg = response.choices[0].message.content
        logging.getLogger(__name__).info(msg)
        return msg








