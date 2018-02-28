import imaplib
from imap_parser import *


def GenerateOAuth2String(username, access_token):
    """Генерирует Oauth2 строку
    Base64 не нужна, так как imap4 сам шифрует
    Generates an IMAP OAuth2 authentication string.
    
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
    return auth_string


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
    imap_conn.debug = 0
    imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
    imap_conn.select('INBOX')
    result, data = imap_conn.uid('search', None, "ALL")  # Выполняет поиск и возвращает UID писем.
    latest_email_uid = data[0].split()[-1]
    result, imap_data = imap_conn.uid('fetch', latest_email_uid, 'RFC822')  # Вовзращает тело письма
    return get_first_text_block(imap_data[0][1])
