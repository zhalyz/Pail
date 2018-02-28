import email


def get_first_text_block(imap_bytes):
    '''Парсинг последнего сообщения. Возвращает дату,
    почту получателя, почту отправителя, текст письма
    '''
    email_message = email.message_from_bytes(imap_bytes)
    Date = email_message['Date'][:-6]  # Дата получения письма
    Receiver = email_message['To']  # Почта получателя
    Sender = email_message['Envelope-From']  # Почта отправителя
    Data = email_message.get_payload()  # Тело письма
    return Date, Receiver, Sender, Data
