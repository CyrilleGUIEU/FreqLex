from zipfile import ZipFile



archive=ZipFile("../FreqLeq.zip","w")
archive.write("FreqLex.py")
archive.write("Data/freqlex.dat")
archive.close()


