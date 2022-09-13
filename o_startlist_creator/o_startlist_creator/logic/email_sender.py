from asyncio.log import logger
from o_startlist_creator.logic.event import Event
from o_startlist_creator.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
import logging
import datetime

DEFAULT_MSG = ''
DEFAULT_SUBJECT = ''

class EmailSender:
    def __init__(self, msg:str, subject:str) -> None:
        self.msg = msg if msg else DEFAULT_MSG
        self.subject = subject if subject else DEFAULT_SUBJECT
        self.sender = 'v.kostejn.vk@gmail.com'

    def send(self, receiver:str, event: Event) -> str:
        attachement = event.export_final_data_to_csv()

        email = EmailMessage(
            self.subject,
            self.msg,
            self.sender,
            [receiver],
        )
        email.attach(f'startovni_rost_{event.id}.csv', attachement, 'text/csv')
        try:
            email.send(fail_silently=False)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"{datetime.datetime.now()} - {e.args}")
        return attachement

