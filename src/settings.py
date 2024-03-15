import os

class Settings:
    def __init__(self):
        self.MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        self.MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        self.MAIL_SERVER = os.environ.get('MAIL_SERVER')
        self.MAIL_PORT = os.environ.get('MAIL_PORT')