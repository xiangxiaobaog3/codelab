# -*- encoding:utf-8 -*-

class ChineseGetter:
    """A simple localizer a la gettext"""

    def __init__(self):
        self.trans = dict(dog='狗', cat='猫')

    def get(self, msgid):
        """we'll punt if we don't have a translation"""

        try:
            return unicode(self.trans[msgid], 'utf-8')
        except KeyError:
            return unicode(msgid)

class EnglishGetter:
    """Simply echoes the msg ids"""
    def get(self, msgid):
        return unicode(msgid)

def get_localizer(language="English"):
    """The factory method"""
    languages = dict(English=EnglishGetter,
                     Chinese=ChineseGetter)
    return languages[language]()

# Create our localizers
e, c = get_localizer("English"), get_localizer("Chinese")

# Localize some text
for msgid in "dog parrot cat".split():
    print e.get(msgid), c.get(msgid)
