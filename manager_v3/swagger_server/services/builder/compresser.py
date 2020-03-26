import tarfile

'''
function to compresse agent befor send it

'''

def compresse(name):
    fp = tarfile.open(name+".tar.gz", "w:gz")
    fp.add(name)
    fp.close()
