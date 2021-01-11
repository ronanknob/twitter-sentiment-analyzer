import re

def _do_regex_text_substitution(pattern, text, replacement_value=None):
    pattern = re.compile(pattern)
    if replacement_value:
        return pattern.sub(replacement_value, text)
    else:
        return pattern.sub(r'', text)

def parse_tweet(tweet):
    if tweet is None or not isinstance(tweet, str):
        return None
    
    # Remove line breaks
    tweet_treated = _remove_breaklines(tweet)
    # Ajust the white spaces
    tweet_treated = _fix_whitespaces_excess(tweet_treated)
    # Remove the twitter users from the message
    tweet_treated = _remove_twitter_usernames(tweet_treated)
    # Remove the emoji characters
    tweet_treated = _remove_emojis(tweet_treated)
    # Remove the hastags
    tweet_treated = _remove_hastags(tweet_treated)
    # Remove the links
    tweet_treated = _remove_http_links(tweet_treated)
    # Remove quotes excess if exist (ex: """Ronan")
    tweet_treated = _remove_quotes_excess(tweet_treated)

    return tweet_treated

def _fix_whitespaces_excess(tweet):
    return _do_regex_text_substitution(r'[ ]{2,}', tweet, r' ')
    
def _remove_retweet_twitter_username(tweet):
    return _do_regex_text_substitution(r'RT\s{1}@.[^:]*:', tweet).strip()

def _remove_twitter_usernames(tweet):
    return _do_regex_text_substitution(r'@.[^\s]*', tweet).strip()

def _remove_emojis(tweet):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', tweet).strip()

def _remove_hastags(tweet):
    return _do_regex_text_substitution(r'#[^\s]*', tweet).strip()

def _remove_http_links(tweet):
    return _do_regex_text_substitution(r'https:\/\/t.co\/.[^\s]*', tweet).strip()

def _remove_quotes_excess(tweet):
    return _do_regex_text_substitution(r'"{2,}', tweet, '"').strip()

def _remove_breaklines(tweet):
    return _do_regex_text_substitution(r'\n\s*', tweet, r' ')