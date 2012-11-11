#-*- encoding:utf-8 -*-

"""
~~~~~~~~~~
实用的技术
~~~~~~~~~~

跟踪子类
~~~~~~~~~
"""

class SubclassTracker(type):
    def __init__(cls, name, bases, attrs):
        try:
            if TrackedClass not in bases:
                return
        except NameError:
            return
        TrackedClass._registry += (cls,)

class TrackedClass(object):
    __metaclass__ = SubclassTracker
    _registry = ()

class ClassOne(TrackedClass):
    pass

print TrackedClass._registry

class ClassTwo(TrackedClass):
    pass

print TrackedClass._registry

class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)

class PasswordValidator(object):
    """
    Plugins extending this class will be used to validate passwords.
    valid plugins must provide the following method.

    validate(self, password)
        receives a password to test, and either finishes silently or raise
        a ValueError if the password was invalid. The exception may be
        displayed to the user, so make suer it it adequately describes
        what's wrong.

    """
    __metaclass__ = PluginMount


def get_password_errors(password):
    """
    Returns a list of messages indicating any problems that were found
    with the password. If it was fine, this returns an empty list.

    """
    errors = []
    for plugin in PasswordValidator.plugins:
        try:
            plugin().validate(password)
        except ValueError, e:
            errors.append(str(e))
    return errors

def is_valid_password(password):
    """
    Returns True if the password was fine, False if there was a problem.
    """
    for plugin in PasswordValidator.plugins:
        try:
            plugin().validate(password)
        except ValueError:
            return False
    return True

class MinimumLength(PasswordValidator):
    def validate(self, password):
        """Raises ValueError if the password is too short."""
        if len(password) < 6:
            raise ValueError('Password must be at least 6 characters.')

class SpecialCharacters(PasswordValidator):
    def validate(self, password):
        """
        Raises ValueError if the password doesn't contain any special
        characters.
        """

        if password.isalnum():
            raise ValueError("Password must contain one special character.")

for password in ('pass', 'password', 'p@ssword!'):
    print ('Checking %r...' % password),
    if is_valid_password(password):
        print 'valid'
    else:
        print  # Force a new line
        for error in get_password_errors(password):
            print '  %s' % error
