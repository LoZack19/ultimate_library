import telegram
import config


def get_token(filename: str) -> str:
    with open(filename, 'r') as infile:
        token = infile.readline().strip()
    
    return token


def post_file_in_channel(filename: str, channel: str) -> str:
    token = get_token(config.token)

    with open(filename, 'rb') as document:
        message_data = telegram.Bot(token=token).send_document("@" + channel, document)

    link = 't.me/{}/{}'.format(channel, message_data['message_id'])
    return link