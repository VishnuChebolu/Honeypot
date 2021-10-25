from twisted.conch import avatar, recvline
from twisted.conch.interfaces import IConchUser, ISession
from twisted.conch.ssh import factory, keys, session
from twisted.conch.insults import insults
from twisted.cred import portal, checkers
from twisted.internet import reactor
from zope.interface import implementer
 
class SSHProtocol(recvline.HistoricRecvLine):
    def __init__(self, user):
       self.user = user
 
    def connectionMade(self):
        recvline.HistoricRecvLine.connectionMade(self)
        self.terminal.write("Connected to the server via SSH.")
        self.terminal.nextLine()
        self.help()
        self.showPrompt()
 
    def showPrompt(self):
        self.terminal.write("ssh > ")
 
    def lineReceived(self, line):
        line = line.strip().decode()
        if line:
            print(line)
            f = open('logfile.log', 'w')
            f.write(line + '\n')
            f.close
            cmdAndArgs = line.split()
            cmd = cmdAndArgs[0]
            args = cmdAndArgs[1:]
            func = getattr(self, cmd, None)
            if func:
                try:
                    func(*args)
                except Exception as e:
                    self.terminal.write(f"Error: {e}")
                    self.terminal.nextLine()
            else:
                self.terminal.write("No such command.")
                self.terminal.nextLine()
        self.showPrompt()
 
    def help(self):
        self.terminal.write("Commands: help, whoami, quit, echo, clear")
        self.terminal.nextLine()
 
    def echo(self, *args):
        self.terminal.write(" ".join(args))
        self.terminal.nextLine()
 
    def whoami(self):
        self.terminal.write(self.user.username)
        self.terminal.nextLine()
 
    def quit(self):
        self.terminal.write("Session terminated!")
        self.terminal.nextLine()
        self.terminal.loseConnection()
 
    def clear(self):
        self.terminal.reset()

@implementer(ISession)
class SSHAvatar(avatar.ConchUser):
     
    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({b'session': session.SSHSession})
 
 
    def openShell(self, protocol):
        serverProtocol = insults.ServerProtocol(SSHProtocol, self)
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))
 
 
    def getPty(self, terminal, windowSize, attrs):
        return None
 
 
    def execCommand(self, protocol, cmd):
        raise NotImplementedError()
 
 
    def closed(self):
        pass
 
@implementer(portal.IRealm)
class SSHRealm(object):
     
    def requestAvatar(self, avatarId, mind, *interfaces):
        if IConchUser in interfaces:
            return interfaces[0], SSHAvatar(avatarId), lambda: None
        else:
            raise NotImplementedError("No supported interfaces found.")


def getRSAKeys():
  
    with open(r'/home/kali/.ssh/id_rsa', "rb") as privateFile:
        privateKeyStr = privateFile.read()
        privateKey = keys.Key.fromString(data=privateKeyStr)
 
 
    with open(r'/home/kali/.ssh/id_rsa.pub', "rb") as publicFile:
        publicKeyStr = publicFile.read()
        publicKey = keys.Key.fromString(data=publicKeyStr)
 
 
    return publicKey, privateKey
 
 
if __name__ == "__main__":
    sshFactory = factory.SSHFactory()
    sshFactory.portal = portal.Portal(SSHRealm())
 
 
users = {'admin': b'aaa', 'guest': b'bbb'}
sshFactory.portal.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse(**users))
pubKey, privKey = getRSAKeys()
sshFactory.publicKeys = {b'ssh-rsa': pubKey}
sshFactory.privateKeys = {b'ssh-rsa': privKey}
reactor.listenTCP(222, sshFactory)
reactor.run()