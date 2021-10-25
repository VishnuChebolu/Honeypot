# SSH Server Using Twisted library in Python 3

` Note ` : This is only the explanation for my code. I am not responsible to anything that you do.

## Why not socket?

I know that, when I showcase my project with twisted, I get questions like, why only twisted?, why not socket? etc.

## Reasons 
   - Socket needs to code in both client and server side, which is not possible in real-life scenario like a honeypot.
   - Socket doesn't allow us to emulate the features of the rel-life shell, whereas twisted does it with the help of ` HistoricRecvLine `
   - socket doesnot allows us to exchange the public key in the SSH protocol.

# Working 

