import os
import dotenv

class Variables:
    def __init__(self, path = ".env"):
        self.path = path
        dotenv.load_dotenv(self.path, override=True)
        self.token = os.getenv("TOKEN")
        self.date = os.getenv("DATE")
        self.problem_number = int(os.getenv("PROBLEM_NUMBER"))
        self.problem_source = os.getenv("PROBLEM_SOURCE")
        self.problem_images = os.getenv("PROBLEM_IMAGES")
        self.problem_anskey = os.getenv("PROBLEM_ANSKEY")
        self.players        = os.getenv("PLAYERS")
        
    def reload(self):
        self.__init__(".env")
        
    def update(self, key, value):
        dotenv.load_dotenv(".env", override=True)
        dotenv.set_key(".env", key, value, quote_mode="never")