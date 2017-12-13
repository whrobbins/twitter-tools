import smtplib

from email.mime.text import MIMEText
from time import sleep


class EmailService(object):
    """
    Use SMTP to send specified emails
    """
    def __init__(self, sender_address):

        self.gmail_sender = sender_address
        self.gmail_passwd = str(input('What is your password, {}? '.format(self.gmail_sender)))

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.gmail_sender, self.gmail_passwd)

    def log_off(self):
        """
        Log out from server
        """
        self.server.quit()

    def send_message(self, a, b, template, vars_, subject, sleep_time=3):
        """
        Send email to specified users
        :param a: Member to send to
        :param b: Member to send to
        :param template: str template for email body to follow
        :param vars_: dict variables to insert into template
        :param subject: subject line
        :param sleep_time: time to wait after a send (anti-spam)
        """
        content = template.format(**vars_)

        # construct a message
        msg = MIMEText(content)
        sender = self.gmail_sender
        recipients = [a.email_address, b.email_address]
        msg['Subject'] = subject
        msg['From'] = self.gmail_sender
        msg['To'] = ", ".join(recipients)

        try:
            self.server.sendmail(sender, recipients, msg.as_string())
            print('email sent!')
        except Exception as e:
            print('error sending mail...')

        if sleep_time:
            sleep(sleep_time)
