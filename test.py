import imaplib
import base64
import email

def TestImapAuthentication(user, auth_string):
    """Authenticates to IMAP with the given auth_string.

    Prints a debug trace of the attempted IMAP connection.

    Args:
    user: The Gmail username (full email address)
    auth_string: A valid OAuth2 string, as returned by GenerateOAuth2String.
        Must not be base64-encoded, since imaplib does its own base64-encoding.
    """
    print('-' * 20)
    imap_conn = imaplib.IMAP4_SSL('imap.yandex.com')
    imap_conn.debug = 4
    imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
    print('\n{0}'.format(imap_conn.select('INBOX')))

    result, data = imap_conn.uid('search', None, "ALL") # Выполняет поиск и возвращает UID писем.
    latest_email_uid = data[0].split()[-1]
    result, data = imap_conn.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]

    email_message = email.message_from_string(raw_email)

    print(email_message['To'])

    print(email.utils.parseaddr(email_message['From']))# получаем имя отправителя "Yuji Tomita"

    print(email_message.items())# Выводит все заголовки.

def get_first_text_block(self, email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

def GenerateOAuth2String(username, access_token, base64_encode=True):
    """Generates an IMAP OAuth2 authentication string.

    See https://developers.google.com/google-apps/gmail/oauth2_overview

    Args:
    username: the username (email address) of the account to authenticate
    access_token: An OAuth2 access token.
    base64_encode: Whether to base64-encode the output.

    Returns:
    The SASL argument for the OAuth2 mechanism.
    """
    auth_string = 'user={0}\@yandex.ru\001auth=Bearer {1}\001\001'.format(username, access_token)
    auth_string = str.encode(auth_string)
    if base64_encode:
        auth_string = base64.b64encode(auth_string)
    return auth_string

if __name__ == '__main__':
    user = 'alexander.shiplen'
    access_token = 'AQAAAAAj6ki9AATVmv5dS7d1c0_YkkIr_UV2PKw'

    TestImapAuthentication(user, GenerateOAuth2String(user, access_token, base64_encode = False))
