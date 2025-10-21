from api_handler import ApiHandler



class AISearch():
    def __init__(self):
        print("AISearch initialized")
        self.api_handler = ApiHandler()


    def search(self, query, db):
        response = self.api_handler.send_request(query, db, "huggingface")
        msg = response.choices[0].message
        print(msg)








