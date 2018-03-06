
class CommunicationChannel:
    message_log = []
    #TODO: Controller should only have 2 instances of CommunicationChannel; 1 public 1 private
    #Reformat system to allow for proper message handling

class PublicChannel(CommunicationChannel):
    public = True
    #TODO:Implement public channels

class PrivateChannel(CommunicationChannel):
    #Create a new private channel
    def __init__(self, sender, recipient):
        self.sender = sender
        self.recipient = recipient

    def send(self, message):
        self.recipient.perceiveMessage(message)
        self.message_log.append(message)
        message.sent = True

    def reply(self, message):
        self.sender.perceiveMessage(message)
        self.message_log.append(message)


class Message:
    sent = False

    def __init__(self, channel):
        self.channel = channel