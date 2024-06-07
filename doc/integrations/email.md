# EMail (Class)

An interface with EMail Servers.

## Initialization

#### Arguments

> `smtp_server_address`: The smpt server address of the EMail service, leave as `None` to use the enviorment variable `EMAIL_SERVER_ADDRESS`.
> `smtp_server_port`: The smpt server port of the EMail service, leave as `None` to use the enviorment variable `EMAIL_SERVER_PORT`.
> `sender_address`: The EMail address of the EMail account, leave as `None` to use the enviorment variable `EMAIL_ADDRESS`.
> `sender_application_password`: The application password of the EMail account, leave as `None` to use the enviorment variable `EMAIL_PASSWORD`.

#### Examples

```python
from rhythm.integrations import EMail

email = EMail()
```

## Methods

### send_mail

Send an Email to the receiver.

#### Arguments:

> `reciver_address`: The EMail address of the recivers EMail account.  
> `subject`: The subjectline of the EMail.  
> `mail_text`: The text content of the EMail.

#### Examples

```python
email.send_mail(reciver_address="example@gmail.com", subject="Test Message", mail_text="This is a test message!")
```
