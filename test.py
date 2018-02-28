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
    imap_conn.debug = 0
    imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
    imap_conn.select('INBOX')
    result, data = imap_conn.uid('search', None, "ALL")  # Выполняет поиск и возвращает UID писем.
    latest_email_uid = data[0].split()[-1]
    result, data = imap_conn.uid('fetch', latest_email_uid, 'RFC822')  # Вовзращает тело письма
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    return get_first_text_block(None, email_message)


def get_first_text_block(self, email_message_instance):
    '''Парсинг последнего сообщения. Возвращает дату,
    почту получателя, почту отправителя, текст письма
    '''
    Date = email_message_instance['Date'][:-6]  # Дата получения письма
    Receiver = email_message_instance['To']  # Почта получателя
    Sender = email_message_instance['Envelope-From']  # Почта отправителя
    Data = email_message_instance.get_payload()  # Тело письма
    return Date, Receiver, Sender, Data


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


if __name__ == '__main__':
    user = 'alexander.shiplen'
    access_token = 'AQAAAAAj6ki9AATVmv5dS7d1c0_YkkIr_UV2PKw'
    Date, Receiver, Sender, Data = TestImapAuthentication(user, GenerateOAuth2String(user, access_token))
