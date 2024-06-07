# Twitter (Class)

An interface with the Twitter API.

## Initialization

#### Arguments

> `consumer_key`: The consumer key of the account, leave as `None` to use the enviorment variable `TWITTER_CONSUMER_KEY`.  
> `consumer_secret`: The consumer secret of the account, leave as `None` to use the enviorment variable `TWITTER_CONSUMER_SECRET`.  
> `access_token`: The access token of the account, leave as `None` to use the enviorment variable `TWITTER_ACCESS_TOKEN`.  
> `access_token_secret`: The access token secret of the account, leave as `None` to use the enviorment variable `TWITTER_ACCESS_TOKEN_SECRET`.  
> `bearer_token`: The bearer token of the account, leave as `None` to use the enviorment variable `TWITTER_BEARER_TOKEN`.

#### Examples

```python
from rhythm.integrations import Twitter

twitter = Twitter()
```

## Methods

### tweet

Post a new tweet with text or images.

#### Arguments

> `textcontent`: The textcontent of the tweet, if left as `None`, `images_path` needs to be given.  
> `images_paths`: The list of file paths of the images to post, needs to be at most length `4`, if left as `None`, `textcontent` needs to be given.

#### Examples

```python
twitter.tweet(textcontent="This is a Test Tweet!")
```

### reply_to_tweet

Reply to a tweet with text or images.

#### Arguments

> `tweet_id`: The ID of the tweet to reply to.  
> `textcontent`: The textcontent of the tweet, if left as `None`, `images_path` needs to be given.  
> `images_paths`: The list of file paths of the images to post, needs to be at most length `4`, if left as `None`, `textcontent` needs to be given.

```python
twitter.reply_to_tweet(tweet_id=123456789, textcontent="This is a Test Reply!")
```

### send_direct_message

Send a direct message with text or image.

#### Arguments

> `user_id`: The ID of the user to send a direct message to.  
> `textcontent`: The textcontent of the message, if left as `None`, `image_path` needs to be given.  
> `image_path`: The file path of the image to post, if left as `None`, `textcontent` needs to be given.

```python
twitter.send_direct_message(user_id=123456789, textcontent="This is a Test DM!")
```

### get_tweets

Get tweets based on a search query.

#### Arguments

> `query`: The search query, needs to be at most `500` characters.  
> `language_code`: The [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) language code to filter by language, leave as `None` to get all languages.  
> `count`: The maximum amount of tweets to return, needs to be at most `100`.  
> `result_type`: The prefered resulting tweets, needs to be one of: `'mixed'`, `'recent'`, `'popular'`.

#### Returns

A list of the filtered tweets. Contains the username and textcontent.

#### Examples

```python
twitter.get_tweets(query="#AI OR @RhymeNetwork", language_code="en", count=10, result_type="popular")
```
