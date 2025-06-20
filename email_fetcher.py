import imaplib
import email
import os

SAVE_DIR = "resumes"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_resumes(user_email, app_password):
    IMAP_SERVER = "imap.gmail.com"
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(user_email, app_password)
    mail.select("inbox")
    status, messages = mail.search(None, '(UNSEEN SUBJECT "Resume")')

    for num in messages[0].split():
        _, msg_data = mail.fetch(num, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    if filename and (filename.endswith(".pdf") or filename.endswith(".docx")):
                        filepath = os.path.join(SAVE_DIR, filename)
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
    mail.logout()
