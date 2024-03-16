from src.settings import Settings
from logging import Logger
from flask import Flask
from flask_mail import Mail, Message

class EmailClient:
    logger: Logger
    settings: Settings
    
    def __init__(self, logger: Logger, app: Flask, settings: Settings = None) -> None:
        self.logger = logger
        self.settings = settings
        
        # mail configuration
        app.config['MAIL_SERVER'] = settings.MAIL_SERVER
        app.config['MAIL_PORT'] = settings.MAIL_PORT
        app.config['MAIL_USERNAME'] = settings.MAIL_USERNAME
        app.config['MAIL_PASSWORD'] = settings.MAIL_PASSWORD
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        
        self.mail = Mail()
        self.mail.init_app(app)
        
    def send(self, email: 'Email') -> None:
        try:
            self.logger.debug(f'Sending email to {email.reciever}')
            msg = Message(email.subject, sender=self.settings.MAIL_USERNAME, recipients=[email.reciever])
            msg.body = email.message
            if email.attachement:
                self.logger.debug(f'Attaching {email.attachement.name}')
                msg.attach(email.attachement.name, email.attachement.mimetype, email.attachement.data)
            self.mail.send(msg)
            self.logger.debug('Email sent')
        except Exception as e:
            msg = f'EmailClient.send failed: {str(e)}'
            self.logger.error(msg)
            raise Exception(msg) from e
        
    
    
class Email:
    reciever: str
    subject: str
    message: str
    attachement: 'Attachment'
    
    def __init__(self, reciever: str, subject: str, message: str, attachement: 'Attachment' = None) -> None:
        self.reciever = reciever
        self.subject = subject
        self.message = message
        self.attachement = attachement
        
class Attachment:
    name: str
    data: bytes
    mimetype: str
    
    def __init__(self, name: str, data: bytes, mimetype: str) -> None:
        self.name = name
        self.data = data
        self.mimetype = mimetype