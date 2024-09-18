from src.client.email import EmailClient, Email, Attachment
from logging import Logger
from src.static_paths import StaticPaths
from src.entities.event import Event

class Postman:
    email_client: EmailClient
    logger: Logger
    
    def __init__(self, email_client: EmailClient, logger: Logger) -> None:
        self.email_client = email_client
        self.logger = logger
        
    def send_email(self, receiver: str, subject: str, message: str) -> None:
        try:
            self.logger.info(f'Sending email to {receiver}')
            email = Email(
                reciever=receiver,
                subject=subject,
                message=message
            )
            self.email_client.send(email)
            self.logger.info('Email sent')
        except Exception as e:
            msg = f'Postman.send_email failed: {str(e)}'
            self.logger.error(msg)
            raise Exception(msg) from e
        
    def deliver_startgrid(self, receiver: str, event:Event) -> None:
        try:
            self.logger.info(f'Delivering startgrid to {receiver}')
            startgrid = event.export_final_data_to_csv()
            with open(StaticPaths.POSTMAN_STARTGRID_MSG, 'r', encoding='utf-8') as file:
                msg = file.read()
            with open(StaticPaths.POSTMAN_STARTGRID_SUBJECT, 'r', encoding='utf-8') as file:
                subject = file.read()
                
            email = Email(
                reciever=receiver,
                subject=subject,
                message=msg,
                attachement=Attachment(
                    name=f'startovni_rost_{event.id}.csv',
                    data=startgrid,
                    mimetype='text/csv'
                )
            )
            self.email_client.send(email)
            self.logger.info('Startgrid delivered')
        except Exception as e:
            msg = f'Postman.deliver_startgrid failed: {str(e)}'
            self.logger.error(msg)
            raise Exception(msg) from e
        