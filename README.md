# Messenger
This is a peer to peer RSA encrypted messenger.  If you're not running the single file version (messenger.py), you NEED to run server.py first or everything breaks.  The encryption and messages work by juggling the data around in files until it reaches you.  The data is sent over tcp using Python's socket library.  You will need to forward port 5005 or the router throws up.  There is an included script at the top to do this if UPnP is enabled.

## Dependencies
[PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/introduction.html)

[miniupnpc](https://pypi.org/project/miniupnpc/)

## Contributors
[Hayden](https://github.com/propanetank) did a lot of testing for me as well as writing the upnp script.  This would've taken a lot longer without his help.
