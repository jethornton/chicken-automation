import os, getpass
print "Env thinks the user is [%s]" % (os.getlogin());
print "Effective user is [%s]" % (getpass.getuser());
