class CommsLink:
    messageDest = None
    def send(self, message):
        self.messageDest(message)


class PrivateLink(CommsLink):

    def __init__(self, messageDest, faction):
        self.messageDest = messageDest
        self.faction = faction


class PublicLink(CommsLink):

    def __init__(self):
        self.connected_channels = []

    def registerChannel(self, private_link):
        self.connected_channels.append(private_link)

    def messageDest(self, message):
        for channel in self.connected_channels:
            if channel.faction != message["sender"]:
                channel.messageDest(message)
