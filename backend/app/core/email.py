import smtplib
import ssl
from email.message import EmailMessage
from app.models import SendEmailModel
from app import constants



## TO DO Update this method We will use free third party provider to send email
def send_email(email_data:SendEmailModel):
    try:
        subject = email_data.subject
        body = email_data.body
        for email in email_data.email_list:
            try:

                msg = EmailMessage()
                msg["From"] = constants.EMAIL_USER
                msg["To"] = email
                msg["Subject"] = subject
                msg.set_content(body)


                context = ssl.create_default_context()
                with smtplib.SMTP(constants.EMAIL_HOST, constants.EMAIL_PORT) as server:
                    server.starttls(context=context)
                    server.login(constants.EMAIL_USER, constants.EMAIL_PASSWORD)
                    server.send_message(msg)
            
            except Exception as e:
                print('Some error occured', e)

        
    except Exception as e:
        print("Some error occured while sending email", e)