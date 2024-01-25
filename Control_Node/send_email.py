import sys
import smtplib
import ssl
from email.message import EmailMessage

def send_email(subject, body, recipient):
    em = EmailMessage()
    em['From'] = 'group14jda@gmail.com'
    em['To'] = recipient
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login('group14jda@gmail.com', 'ujzc yrui fuut acbu')
        smtp.sendmail('group14jda@gmail.com', recipient, em.as_string())

if __name__ == "__main__":
    web_instance_a1_ip = sys.argv[1]
    web_instance_b1_ip = sys.argv[2]
    db_instance_a1_ip = "11.0.16.46"
    db_instance_b1_ip = "11.0.17.23"
    email = str(sys.argv[5])
    body = f"Web Instance A1 IP: {web_instance_a1_ip}\nWeb Instance B1 IP: {web_instance_b1_ip}\nDB Instance A1 IP: {db_instance_a1_ip}\nDB Instance B1 IP: {db_instance_b1_ip}"
    send_email('New EC2 Instances', body, email )
