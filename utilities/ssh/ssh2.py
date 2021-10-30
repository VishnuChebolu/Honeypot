from types import CellType
from twisted.conch import avatar, recvline
from twisted.conch.interfaces import IConchUser, ISession
from twisted.conch.ssh import factory, keys, session
from twisted.conch.insults import insults
from twisted.cred import portal, checkers,error, credentials
from twisted.internet import reactor, defer
from zope.interface import implementer
from twisted.python import failure
 
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
 
 

 


@implementer(checkers.ICredentialsChecker)
class InMemoryUsernamePasswordDatabaseDontUse:

    credentialInterfaces = (
        credentials.IUsernamePassword,
        credentials.IUsernameHashedPassword,
    )

    def __init__(self, **users):

        self.users = {x.encode("ascii"): y for x, y in users.items()}

    def addUser(self, username, password):
        self.users[username] = password

    def _cbPasswordMatch(self, matched, username):
        if matched:
            return username
        else:
            return failure.Failure(error.UnauthorizedLogin())

    def requestAvatarId(self, credentials):
        print(credentials.username, credentials.password)
        if credentials.username in self.users:
            return defer.maybeDeferred(
                credentials.checkPassword, self.users[credentials.username]
            ).addCallback(self._cbPasswordMatch, credentials.username)
        else:
            return defer.fail(error.UnauthorizedLogin())

class SSHFactoryRedefined(factory.SSHFactory):

    def buildProtocol(self, addr):
        print (addr)
        return factory.SSHFactory.buildProtocol(self, addr)

sshFactory = SSHFactoryRedefined()
sshFactory.portal = portal.Portal(SSHRealm())
 
users = {'admin': b'admin', 'adminstrator': b'password', 'root':b'toor'}
sshFactory.portal.registerChecker(InMemoryUsernamePasswordDatabaseDontUse(**users))
pubKey, privKey = getRSAKeys()
sshFactory.publicKeys = {b'ssh-rsa': pubKey}
sshFactory.privateKeys = {b'ssh-rsa': privKey}
reactor.listenTCP(222, sshFactory)
reactor.run()

