"""
Some helper functions to be used along slackbot package
"""

def is_in_channel(message, src_name):
    """
    filters message by source. `src_name` can either be channel name or user name
    returns true if message is from source
    """
    if message.body.get('channel', '') == message._client.find_channel_by_name(src_name):
        return True
    return False

def rename(newname):
    def decorator(f):
        f.__name__ = newname
        return f
    return decorator

def in_channel(channel_name):
    """
    a decorator filters message by channel. `channel_name` can either be channel name or user name
    
    Can be used as:

        @listen_to('hello bot')
        @in_channel('general')
        def reply(message):
            message.reply('hi!')

    """
    def do_filter(func):
        @rename(func.__name__)
        def wrapper(message):
            func.__name__
            if is_in_channel(message, channel_name):
                func(message)
        return wrapper
    return do_filter
