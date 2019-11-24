import telebot
import feedparser
import pickle
import os
import time

class KyberBot(object):
    """
    Send something to channel using the official clients and then
    retrieve the chat id by sending following message:
    https://api.telegram.org/bot<token>/getUpdates?offset=0
    and find out chat id from the response message
    """
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN') #
        self.bot = telebot.TeleBot(self.token)
        self.chatID = 1068475610
        self.last_msg_send = time.gmtime(0)
        self.posted = None          

    def feed_parser(self, url):
        """
        Return markdown formatted message to be sent 
        """
        self.feed = feedparser.parse(url)
        if 'description' in self.feed.entries[0]:
            bot_msg = f"*{self.feed.entries[0].title}*\n[{self.feed.entries[0].description}]({self.feed.entries[0].link})"
        else:
            bot_msg = f"*{self.feed.entries[0].title}*\n{self.feed.entries[0].link}"

        self.posted = self.feed.entries[0].published_parsed
        # Last time message send to telegram
        return bot_msg
    
    def send_message(self, msg="test"):
        if self.posted > self.last_msg_send:
            return self.bot.send_message(self.chatID, msg, parse_mode='markdown')
        


if __name__ == "__main__":
    import argparse
    import pickle
    feeds = [
            "https://www.kyberturvallisuuskeskus.fi/feed/rss/fi",
            "https://www.kyberturvallisuuskeskus.fi/feed/rss/fi/400",
            "https://www.kyberturvallisuuskeskus.fi/feed/rss/fi/399",
            "https://www.kyberturvallisuuskeskus.fi/feed/rss/fi/401"
            ]
    
    def url_to_filename(url: str):
        return url.replace('/', '_')

    parser = argparse.ArgumentParser(description=
    f"""
    Read kyberturvallisuuskeskus RSS feed and post updates to Telegram channel.
    Environment variable TELEGRAM_BOT_TOKEN must be found.
    One of these urls can be given:
    {feeds} 
    """
    )
    parser.add_argument("url", help="Give a url for a RSS feed.")
    args = parser.parse_args()
    bot = KyberBot()
    try:
        bot.last_msg_send = pickle.load(open(f"{url_to_filename(args.url)}.db", 'rb'))
    except (EOFError, FileNotFoundError, NameError) as e :
        print(f"Error happened: {e}")

    bot.send_message(bot.feed_parser(args.url))
    pickle.dump(bot.posted, open(f"{url_to_filename(args.url)}.db", 'wb'))








