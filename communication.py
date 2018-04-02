@abs
class CommsLink:

    def send(self, message):
        self.messageDest(message)


class PrivateLink(CommsLink):

    def __init__(self, messageDest):
        self.messageDest = messageDest


class PublicLink(CommsLink):

    def __init__(self, connected_links):
        self.connected_channels = connected_links

    def messageDest(self, message):
        for channel in self.connected_channels:
            channel.messageDest(message)
