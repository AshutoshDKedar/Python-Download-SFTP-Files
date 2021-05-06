import os
import pysftp
from stat import S_IMODE, S_ISDIR, S_ISREG

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None    
sftp=pysftp.Connection('192.168.X.X', username='username',password='password',cnopts=cnopts)

def get_r_portable(sftp, remotedir, localdir, preserve_mtime=False):
    for entry in sftp.listdir(remotedir):
        remotepath = remotedir + "/" + entry
        localpath = os.path.join(localdir, entry)
        mode = sftp.stat(remotepath).st_mode
        if S_ISDIR(mode):
            try:
                os.mkdir(localpath,mode=777)
            except OSError:     
                pass
            get_r_portable(sftp, remotepath, localpath, preserve_mtime)
        elif S_ISREG(mode):
            sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)

remote_path=input("enter the remote_path: ")
local_path=input("enter the local_path: ")

get_r_portable(sftp, remote_path, local_path, preserve_mtime=False)
