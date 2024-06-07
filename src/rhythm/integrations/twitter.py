"""A module containing all Twitter / X API integrations."""

import os
import tweepy
from typing_extensions import Literal

class Twitter():
    """An interface with the twitter API."""
     
    def __init__(self, consumer_key : str | None = None, consumer_secret : str | None = None, access_token : str | None = None, access_token_secret : str | None = None, bearer_token : str | None = None) -> None:
        """An interface with the twitter API.

        Arguments:

            `consumer_key`: The consumer key of the account, leave as `None` to use the enviorment variable `TWITTER_CONSUMER_KEY`.
            `consumer_secret`: The consumer secret of the account, leave as `None` to use the enviorment variable `TWITTER_CONSUMER_SECRET`.
            `access_token`: The access token of the account, leave as `None` to use the enviorment variable `TWITTER_ACCESS_TOKEN`.
            `access_token_secret`: The access token secret of the account, leave as `None` to use the enviorment variable `TWITTER_ACCESS_TOKEN_SECRET`.
            `bearer_token`: The bearer token of the account, leave as `None` to use the enviorment variable `TWITTER_BEARER_TOKEN`.
            
        Examples:

        .. code-block:: python
            from rhythm.integrations import Twitter

            twitter = Twitter()"""

        consumer_key = consumer_key or os.environ.get("TWITTER_CONSUMER_KEY")
        consumer_secret = consumer_secret or os.environ.get("TWITTER_CONSUMER_SECRET")
        access_token = access_token or os.environ.get("TWITTER_ACCESS_TOKEN")
        access_token_secret = access_token_secret or os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
        bearer_token = bearer_token or os.environ.get("TWITTER_BEARER_TOKEN")

        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret )
        auth.set_access_token(access_token, access_token_secret)
        self.__api = tweepy.API(auth)
        self.__client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret= consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
        

    def tweet(self, textcontent : str | None = None, images_paths : list[str] | None = None) -> None:
        """Post a new tweet with text or images.

        Arguments:

            `textcontent`: The textcontent of the tweet, if left as `None`, `images_path` needs to be given.
            `images_paths`: The list of file paths of the images to post, needs to be at most length `4`, if left as `None`, `textcontent` needs to be given."""

        media_ids = []
        for image in images_paths[:4]:
            media  = self.__api.simple_upload(filename=image)
            media_ids.append(media.media_id)
        
        self.__client.create_tweet(text=textcontent, media_ids=media_ids)
    
    def reply_to_tweet(self, tweet_id : int, textcontent : str | None = None, images_paths : list[str] | None = None) -> None:
        """Reply to a tweet with text or images.

        Arguments:

            `tweet_id`: The ID of the tweet to reply to.
            `textcontent`: The textcontent of the tweet, if left as `None`, `images_path` needs to be given.
            `images_paths`: The list of file paths of the images to post, needs to be at most length `4`, if left as `None`, `textcontent` needs to be given."""

        media_ids = []
        for image in images_paths[:4]:
            media  = self.__api.simple_upload(filename=image)
            media_ids.append(media.media_id)

        self.__client.create_tweet(in_reply_to_tweet_id=tweet_id, text=textcontent, media_ids=media_ids)

    def send_direct_message(self, user_id : int, textcontent : str | None = None, image_path : str | None = None) -> None:
        """Send a direct message with text or image.

        Arguments:

            `user_id`: The ID of the user to send a direct message to.
            `textcontent`: The textcontent of the message, if left as `None`, `image_path` needs to be given.
            `image_path`: The file path of the image to post, if left as `None`, `textcontent` needs to be given."""

        media_id = None
        if(image_path):
            media  = self.__api.simple_upload(filename=image_path)
            media_id = media.media_id

        self.__api.send_direct_message(recipient_id=user_id, text=textcontent, attachment_type="media", attachment_media_id=media_id)

    def get_tweets(self, query : str, language_code : str | None = None, count : int = 15, result_type : Literal["mixed", "recent", "popular"] = "mixed") -> list[str]:
        """Get tweets based on a search query.
        
        Agruments:
        
            `query`: The search query, needs to be at most `500` characters.
            `language_code`: The [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) language code to filter by language, leave as `None` to get all languages.
            `count`: The maximum amount of tweets to return, needs to be at most `100`.
            `result_type`: The prefered resulting tweets, needs to be one of: `'mixed'`, `'recent'`, `'popular'`.
            
        Returns:

            A list of the filtered tweets. Contains the username and textcontent."""
        
        if(language_code != None):
            tweets = self.__api.search_tweets(q=query, lang=language_code, tweet_mode="extended", count=count, result_type=result_type)
        else:
            tweets = self.__api.search_tweets(q=query, tweet_mode="extended", count=count, result_type=result_type)

        tweet_list = []
        for tweet in tweets.statuses:
            tweet_list.append({"username" : tweet.user.name, "tweet_text" : tweet.text})
        return tweet_list
