import imaplib
import email
import getpass


class eMessage:
    """Login to mail server to query for emails in rea-only mode""" 
    def __init__(self, server, user, **kwargs):
        """set server and user e.g eMessage('imap.example.com, bob@emample.com
        optional key word argument of folder (default is INBOX)"""
        self.user = user
        self.server = server
        self.folder = kwargs.get('folder', 'INBOX')
        self.logged_in = False
    
    def login(self, password=None):
        """Takes option password string. 
        Recommended to leave blank and user will be prompted"""
        self.mail = imaplib.IMAP4_SSL(self.server)
        if not password:
            password = getpass.getpass('password: ')
        self.mail.login(self.user, password)
        self.mail.select(self.folder, readonly=True)
        self.logged_in = True
    
    def get_uids_search(self, query):
        """Returns list of UIDs for emails that match the search query
        example query string: '(FROM "John Doe")' """
        result, data = self.mail.search(None, query)
        return data[0].split() 

    def get_email(self, uid):
        """returns dictionary of raw email, email body, to and from headers
        for given UID"""
        email_result, email_data = self.mail.fetch(uid, "(RFC822)")
        raw_email = email_data[0][1]
        email_message = email.message_from_string(raw_email)
        if email_message.is_multipart():
            body = ' '
            #print(email_message.get_payload())
            #payloads = []
            #for payload in email_message.get_payload():
            #    payloads.append(payload.get_payload())
            #body = '\n'.join(payloads)    
        else:
            body = email_message.get_payload()
        email_parts =  {
                'raw_email': raw_email,
                'to': email_message['To'],
                'from': email_message['From'],
                'body': body
                }
        return email_parts


