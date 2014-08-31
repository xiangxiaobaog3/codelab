#!/usr/bin/env python
# encoding: utf-8


class Publisher:
    def __init__(self):
        pass

    def register(self):
        raise NotImplemented

    def unregister(self):
        raise NotImplemented

    def notifyAll(self):
        raise NotImplemented


class TechForum(Publisher):
    def __init__(self):
        self.__listOfUsers = []
        self.postname = None

    def register(self, userObj):
        if userObj not in self.__listOfUsers:
            self.__listOfUsers.append(userObj)

    def unregister(self, userObj):
        if userObj in self.__listOfUsers:
            self.__listOfUsers.remove(userObj)

    def notifyAll(self):
        for objs in self.__listOfUsers:
            objs.notify(self.postname)

    def writeNewPost(self, postname):
        # User writes a post
        self.postname = postname
        # When submits the post is published and notification is sent to all
        self.notifyAll()


class Subscriber:
    def __init__(self):
        pass

    def notify(self):
        raise NotImplemented


class User1(Subscriber):
    def notify(self, postname):
        print "User1 notfied of a new post %s" % postname


class User2(Subscriber):
    def notify(self, postname):
        print "User2 notfied of a new post %s" % postname


class SisterSites(Subscriber):
    def __init__(self):
        self.__sisterWebsites = ["Site1", "Site2", "Site3"]

    def notify(self, postname):
        for site in self.__sisterWebsites:
            print "Sent notification to site: %s" % site


def main():
    techForum = TechForum()
    u1 = User1()
    u2 = User2()
    sites = SisterSites()

    techForum.register(u1)
    techForum.register(u2)
    techForum.register(sites)

    techForum.writeNewPost('Observer pattern in Python')
    techForum.unregister(u2)
    techForum.writeNewPost('MVC pattern in Python')

if __name__ == '__main__':
    main()
