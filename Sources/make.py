from zipfile import ZipFile
from os import listdir

print("Création de l'archive...")

archive=ZipFile("../FreqLex.zip","w")
archive.write("dist/FreqLex.exe",arcname = "FreqLex.exe")
archive.write("Licence")
for f in listdir("DATA"):
    if f!="LicenceOK":
        archive.write("DATA/"+f)
for f in listdir("Bases_sql"):
    archive.write("Bases_sql/"+f)

archive.close()
input()

