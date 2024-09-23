#!/usr/bin/env python2
OUTPUTNAME_IGNORE_NUMBER=3

def InputDir(argv):
    if len(argv) != 2: raise IOError("input a directory")
    output=argv[1]
    return output[:-1] if output[-1]=='/' else output

import commands
import os
class folder(object):
    def __init__(self, currentDir):
        self._cDir=currentDir
        self._motherId=0
        self.blocked=False
        self.IsEndPoint=False
    def daugidx(self, idx):
        return self._daughters[idx]
    def GetDaughter(self,dIdx=0):
        self.browsedaughters()
        if dIdx >= len(self._daughters):
            self.blocked=True
            return None
        if not GetFromPool(self.daugidx(dIdx)).blocked:
            return GetFromPool(self.daugidx(dIdx))
        return self.GetDaughter(dIdx+1)
    def GetMother(self):
        return GetFromPool(self._motherId)
    def fullpath(self, d):
        return '/'.join( [self._cDir,d] )

    def browsedaughters(self):
        if not hasattr(self, '_daughters'):
            daugs=os.listdir(self._cDir)
            self._daughters=[ SetToPool(self.fullpath(dname)) for dname in daugs if os.path.isdir(self.fullpath(dname)) ]
    def containingrootfile(self):
        for content in os.listdir(self._cDir):
            if '.root' == content[-5:]: return True
        return False
    def nodaughter(self):
        if self.GetDaughter() == None: return True
        return False
    def ended(self):
        self.blocked=True
        return True
    def IsGoalFolder(self):
        #if self.containingrootfile()         : return self.ended()
        self.browsedaughters()
        if len(self._daughters)==0:
            self.blocked=True
            self.IsEndPoint=True
        #if self.GetDaughter() == None : self.IsEndPoint=True
        return self.IsEndPoint

def RecordRes(finalFolder):
    pathfreg=finalFolder._cDir.split('/')
    oPath=pathfreg[1]+'.txt' if len(pathfreg)>1 else pathfreg[0]+'.txt'
    print 'output text : ' + oPath
    rootfiles=[ os.path.abspath(finalFolder._cDir+'/'+rootfile)
                for rootfile in os.listdir(finalFolder._cDir) if '.root' == rootfile[-5:] ]
    f=open(oPath,'a')
    for l in rootfiles:
        f.write(l + '\n')
    f.close()


def FolderPool():
    fnull=folder('')
    fnull.blocked=True
    return [fnull]
def NullFolder():
    return pool[0]
def SetToPool(foldname):
    pool.append(folder(foldname))
    return len(pool)-1
def GetFromPool(idx):
    return pool[idx]

# return depth
def RecursivelyBrowsingFolder(foldobj):
    if foldobj.IsGoalFolder():
        return 1
    daugobj=foldobj.GetDaughter()
    if daugobj:
        return RecursivelyBrowsingFolder(daugobj)+1
    return -100
def findall(startpoint):
    res=[]
    SetToPool(startpoint)
    startfolder=GetFromPool(1)
    while startfolder.blocked==False:
        depth=RecursivelyBrowsingFolder(startfolder)


if __name__ == '__main__':
    import sys
    import os
    startdir=InputDir(sys.argv)

    printchecker = True if len([ 1 for v in os.listdir('.') if '.txt' in v ]) > 0 else False

    pool=FolderPool()
    #findall('/home/ltsai/TMP')
    findall(startdir)

    for a in pool:
        if a.IsEndPoint:
            print a._cDir
            RecordRes(a)

    if printchecker: print '''
    ================================================================================
    Warning : The file is opened at "append mode". Originally there exists text file
    originally, output files might contain old content. Check before use.
    ================================================================================

    '''



