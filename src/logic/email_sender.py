from asyncio.log import logger
from ..entities.event import Event
from src.o_startlist_creator.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from src.static_paths import STATIC_PATH
import logging
import datetime

class EmailSender:
    def __init__(self) -> None:
        self.msg = DEFAULT_MSG
        self.subject = DEFAULT_SUBJECT
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
        email.send(fail_silently=False)
        return attachement

