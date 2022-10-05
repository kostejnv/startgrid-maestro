from asyncio.log import logger
from o_startlist_creator.logic.event import Event
from o_startlist_creator.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
import logging
import datetime

DEFAULT_MSG = """Hezký den,
váš startovní rošt byl vytvořen. Naleznete ho v příloze.

Pokud máte jakékoli připomínky nebo nápady na vylepšení, stačí odpovědět na tento email. Budu rád za každou zpětnou vazbu.
Víťa Koštejn
"""
DEFAULT_SUBJECT = 'Startovní rošt vytvořen'

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

