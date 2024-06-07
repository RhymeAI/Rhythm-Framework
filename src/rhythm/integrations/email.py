"""A module containing all EMail API integrations."""

import os
import ssl
from smtplib import SMTP_SSL
from email.message import EmailMessage

class EMail():
    """An interface with EMail Servers."""

    def __init__(self, smtp_server_address : str | None = None, smtp_server_port : int | None = None, sender_address : str | None = None, sender_application_password : str | None = None) -> None:
        """An interface with EMail Servers.

        Arguments:

            `smtp_server_address`: The smpt server address of the EMail service, leave as `None` to use the enviorment variable `EMAIL_SERVER_ADDRESS`.
            `smtp_server_port`:  The smpt server port of the EMail service, leave as `None` to use the enviorment variable `EMAIL_SERVER_PORT`.
            `sender_address`: The EMail address of the EMail account, leave as `None` to use the enviorment variable `EMAIL_ADDRESS`.
            `sender_application_password`: The application password of the EMail account, leave as `None` to use the enviorment variable `EMAIL_PASSWORD`.
                
        Examples:

            .. code-block:: python
            from rhythm.integrations import EMail
        
            email = EMail()"""

        smtp_server_address = smtp_server_address or os.environ.get("EMAIL_SERVER_ADDRESS")
        smtp_server_port = smtp_server_port or os.environ.get("EMAIL_SERVER_PORT")
        sender_address = sender_address or os.environ.get("EMAIL_ADDRESS")
        sender_application_password = sender_application_password or os.environ.get("EMAIL_PASSWORD")

        self.__smpt_server_address = smtp_server_address
        self.__smpt_server_port = smtp_server_port
        self.__sender_address = sender_address
        self.__sender_application_password = sender_application_password

    def send_mail(self, reciver_address : str, subject : str, mail_text : str) -> None:
        """Send an Email to the reciver.
        
        Arguments:

            `reciver_address`: The EMail address of the recivers EMail account.
            `subject`: The subjectline of the EMail.
            `mail_text`: The text content of the EMail."""

        mail = EmailMessage()
        mail['From'] = self.__sender_address
        mail['to'] = reciver_address
        mail['Subject'] = subject
        mail.set_content(mail_text)
        context = ssl.create_default_context()
        with SMTP_SSL(self.__smpt_server_address, self.__smpt_server_port, context=context) as smtp:
            smtp.login(self.__sender_address, self.__sender_application_password)
            smtp.sendmail(self.__sender_address ,reciver_address, mail.as_string())
            smtp.quit()
