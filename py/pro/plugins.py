#-*- encoding:utf-8 -*-

class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)

class PasswordValidator(object):
    """
    Plugins extending this class will be used to validte password.
    """

    __metaclass__ = PluginMount

def is_valid_password(password):
    for plugin in PasswordValidator.plugins:
        try:
            plugin().validate(password)
        except ValueError:
            return False
    return True

def get_password_errors(password):
    errors = []
    for plugin in PasswordValidator.plugins:
        try:
            plugin().validate(password)
        except ValueError, e:
            errors.append(str(e))
    return errors

class MinimumLength(PasswordValidator):
    def validate(self, password):
        if len(password) < 6:
            raise ValueError("Passwords must be at least 6 characters.")

class SpecialCharacters(PasswordValidator):
    def validate(self, password):
        if password.isalnum():
            raise ValueError("Passwords must contain one special character.")

for password in ('pass', 'password', 'p@ssword!'):
    print ('Checking %r...' % password)
    if is_valid_password(password):
        print 'valid'
    else:
        for error in get_password_errors(password):
            print ' %s' % error
