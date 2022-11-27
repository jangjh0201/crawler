import imaplib
import email
from email.header import decode_header, make_header
import schedule

class Email():
    __socket = None
    def __init__(self, id, pw):
        self.__socket = imaplib.IMAP4_SSL("imap.gmail.com", port=993)
        self.__socket.login(id, pw)

    def searchMail(self):
        self.__socket.select('INBOX')

        self.__socket.literal = u"주문내역".encode('utf-8')

        resp, lst = self.__socket.uid('search', 'CHARSET', 'UTF-8', 'ALL', 'SUBJECT') # 미확인 메일 : "ALL" -> "UNSEEN"

        for i in lst[0].split():
            result, data = self.__socket.uid('fetch', i, '(RFC822)')
            raw_email = data[0][1]

            print("-"*80)
            message = email.message_from_bytes(raw_email)
            date = make_header(decode_header(message.get('Date')))
            print(date)
            frm = make_header(decode_header(message.get('From')))
            print(frm)
            subject = make_header(decode_header(message.get('Subject')))
            print(subject)

    def __del__(self):
        self.__socket.close()
        self.__socket.logout()

if __name__ == '__main__':
    mail = Email('id', 'pw')
    mail.searchMail()
    schedule.every(10).hours.do(mail.searchMail)
    while True:
        schedule.run_pending()
