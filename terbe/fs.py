"""
changeDir Change current working directory
makeDir   Make a directory
makeFile  Make a file
move      Move something
copy      Copy something
remove    Remove something
dictTree  Tree based on a dict
listTree  Tree based on a list
getInfo   Informations based on a dict
pwd       Get current working directory
"""

import os, shutil, types
from argparse import Namespace
pwd = os.getcwd
changeDir = os.chdir
def makeDir(*args, **kwargs):
    if "exist_ok" not in kwargs: kwargs["exist_ok"] = True
    os.makedirs(*args, **kwargs)

def makeFile(*args, **kwargs):
    if "mode" not in kwargs: kwargs["mode"] = "w"
    open(*args, **kwargs).close()

move = shutil.move

def copy(source, target):
    if os.path.isfile(source):
        shutil.copy2(source, target)
    elif os.path.isdir(source):
        shutil.copytree(source, target)
    else:
        raise FileNotFoundError(source)

def remove(name):
    if os.path.isfile(name):
        os.remove(name)
    elif os.path.isdir(name):
        shutil.rmtree(name)
    else:
        raise FileNotFoundError(name)

def dictTree(workdir="."):
    cont = dict()
    for tmp in sorted(os.listdir(workdir)):
        if os.path.isdir(os.path.join(workdir, tmp)):
            cont[tmp] = dictTree(os.path.join(workdir, tmp))
        else:
            cont[tmp] = None
    return cont

def listTree(workdir="."):
    cont = set()
    def helper(info):
        cont = set()
        for tmp in info:
            if info[tmp] is None:
                cont.add(tmp)
            else:
                cont.add(tmp + "/")
                for tmp1 in helper(info[tmp]):
                    cont.add(tmp + "/" + tmp1)
        return cont
    return helper(dictTree(workdir))

def Info(path, count=True):
    namespace = Namespace()

    if os.path.isfile(path):
        namespace.type = "File"

        stats = os.stat(path)

        namespace.size = stats.st_size
        namespace.mode = stats.st_mode
        namespace.inodeNumber = stats.st_ino
        namespace.userID = stats.st_dev
        namespace.deviceID = stats.st_uid
        namespace.groupID = stats.st_gid
    elif os.path.isdir(path):
        namespace.type = "Dir"

        if count:
            size = 0
            dirs = 0
            files = 0
                
            for tmp in listTree(path):
                if os.path.isfile(tmp):
                    files += 1
                    size += os.path.getsize(tmp)
                else:
                    dirs += 1
            
            namespace.size = size
            namespace.files = files
            namespace.dirs = dirs
    else:
        namespace.type = "None"
        return
        
    namespace.absPath = os.path.abspath(path)
    namespace.createdTime = os.path.getctime(path)
    namespace.modifiedTime = os.path.getmtime(path)
    namespace.name = os.path.basename(namespace.absPath)

    return namespace