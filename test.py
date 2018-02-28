from imap_authentication import *
from Message_class import Message

if __name__ == '__main__':
    user = 'alexander.shiplen'
    access_token = 'AQAAAAAj6ki9AATVmv5dS7d1c0_YkkIr_UV2PKw'
    message = TestImapAuthentication(user, GenerateOAuth2String(user, access_token))
    message = Message(message[0], message[1], message[2], message[3])
    print(message.date)
