from dicts import users


def user_exists(message):
    return message.from_user is not None and message.from_user.id in users

def user_not_exists(message):
    return not user_exists(message)

def selects_info(message):
    return message.from_user is not None and message.from_user.id in users and users[message.from_user.id]['selects_info']

def selects_dish(message):
    return message.from_user is not None and message.from_user.id in users and users[message.from_user.id]['selects_dish']