class Message(object):
    '''Объект: письмо с полями:
    date - дата
    receiver - получатель
    sender - отправитель
    data - тело письма'''
    def __init__(self, date, receiver, sender, data):
        self.date = date
        self.receiver = receiver
        self.sender = sender
        self.data = data


