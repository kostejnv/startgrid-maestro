from o_startlist_creator.logic.event import Event
from o_startlist_creator.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage

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
        email.send(fail_silently=True)
        return attachement

