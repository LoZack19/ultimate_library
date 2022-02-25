from threading import TIMEOUT_MAX
import telegram
import config
import parse
import time


TIMEOUT_MSG = "Timeout: sleeping for %d seconds"


def get_token(filename: str) -> str:
    with open(filename, 'r') as infile:
        token = infile.readline().strip()
    
    return token


def post_file_in_channel(filename: str, channel: str) -> str:
    token = get_token(config.token)

    with open(filename, 'rb') as document:
        message_data = telegram.Bot(token=token).send_document("@" + channel, document)

    link = 'https://t.me/{}/{}'.format(channel, message_data['message_id'])
    return link


def fix_file_links(works: list, backup_path="."):
    for work in works:
        if work["link"] != None and "://" not in work["link"]:
            filename = backup_path.rstrip('/') + '/' + work["link"]
            
            done = False
            while not done:
                try:
                    link = post_file_in_channel(filename, "ul_archive")
                    work["link"] = link
                    done = True
                except:
                    timeout = 2
                    print(TIMEOUT_MSG % timeout)
                    time.sleep(2)


def post_message_in_channel(channel: str, text: str):
    token = get_token(config.token)
    message_data = telegram.Bot(token=token).send_message('@' + channel, text, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    return "https://t.me/%s/%d" % (channel, message_data['message_id'])


def post_works_on_channel(works: list, channel: str):
    months = parse.init_months(config.months)

    for work in works:
        bsl = parse.bsl_format(work, months)

        done = False
        while not done:
            try:
                post_message_in_channel(channel, bsl)
                time.sleep(2)
                done = True
            except telegram.error.TimedOut:
                timeout = 4
                time.sleep(timeout)
                print(TIMEOUT_MSG % timeout)
            except telegram.error.RetryAfter as timeout:
                print("[WARNING] : Flood detected")
                print(TIMEOUT_MSG % timeout)
                time.sleep(timeout)