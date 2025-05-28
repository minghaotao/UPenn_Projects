import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import gs_main


def send_email_func(sender_email, recipient_email, subject, message,attachment_file_path):
    # password = os.environ.get('EMAIL_PASSWORD')
    
    password = gs_main.load_json()['IDD_Email']

    print(password)




    if not password:
        raise ValueError('EMAIL_PASSWORD environment variable is not set')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    with open(attachment_file_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=f.name)
        msg.attach(attachment)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(sender_email, password)
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())






if __name__ == '__main__':

    sender_email = ""
    recipient_email = ""
    subject = "GS Late Submission Report"
    message = "This is a TEST for the email notification"
    attachment_file_path = ''

    send_email_func(sender_email,recipient_email,subject,message,attachment_file_path)



