from zipfile import ZipFile



archive=ZipFile("../FreqLeq.zip","w")
archive.write("Scripts/FreqLex_core.py")
archive.write("Scripts/base_lexique.py")
archive.write("Scripts/gui_freqlex.py")
archive.write("Scripts/licence_freqlex.py")
archive.write("Scripts/gestion_couleurs.py")
archive.write("Data/freqlex.dat")
archive.write("Data/icon.ico")
archive.write("FreqLex.py")
archive.write("Licence")
archive.close()


