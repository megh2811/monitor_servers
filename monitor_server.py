'''Program to monitor servers and send an email alert with log file attachment if server(s) cannot be pinged.'''

import os

import smtplib
import mimetypes
from email.message import EmailMessage

import logging
from datetime import datetime


log_path = r'filepath\monitor_server_log.txt'
attachment = os.path.basename(log_path)
logging.basicConfig(filename=log_path, level=logging.CRITICAL)

server_list_path = r'C:\Users\Meghana\Desktop\Academic\PYTHON\Scripts\monitor_server_list.txt'

server_down = []

sender_id = os.environ.get('email_id')
sender_pass = os.environ.get('email_password')
receivers = ['megh1128uk@gmail.com']

msg = EmailMessage()


def log(error, time):
    '''Logs the ping response and the time of the unsuccessful ping.'''

    logging.critical(error)
    logging.critical(f'Time: {time}')


def send_alert(servers):
    '''Sends email alert to receiver(s) alongwith the log file as an attachment.'''

    msg['From'] = sender_id
    msg['To'] = receivers
    msg['Subject'] = "Server Down!"
    if len(servers) == 1:
        msg.set_content(
            f'\nPing to server {servers} unsuccessful.\nPlease check!')
    else:
        msg.set_content(
            f'\nPing to servers {servers} unsuccessful.\nPlease check!')

    mime_type, _ = mimetypes.guess_type(log_path)
    mime_type, mime_subtype = mime_type.split('/', 1)
    with open(log_path, 'rb') as attach:
        msg.add_attachment(attach.read(), maintype=mime_type,
                           subtype=mime_subtype, filename=attachment)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_id, sender_pass)
        smtp.send_message(msg)


def main():
    with open(server_list_path, 'r') as list:
        ip_addrs = list.read()
        ip_addrs = ip_addrs.splitlines()
        for ip in ip_addrs:
            r = os.popen(f"ping {ip}").read()
            if ("Lost = 0") not in r:
                now = datetime.now()
                log(r, now)
                server_down.append(ip)
        if server_down:
            send_alert(server_down)


if __name__ == '__main__':
    main()
