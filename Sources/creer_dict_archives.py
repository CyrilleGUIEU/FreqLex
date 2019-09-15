import pickle

#Récupération des données
fichier=open("../Data/base_lexicale.pickle","rb")
bl=pickle.load(fichier)
fichier.close()
#Création de la base
fichier=open("../Data/dict_archive.pickle","wb")
taille=1000
dict_archive={}
fcc=[0 for k in bl.bddl_brute]
for mot in dict_archive.keys():
    k=0
    for f in freq:
        fcc[k]=fcc[k]+f/10**6
        k=k+1

n=0
for mot in bl.bddl_brute[0].forme[:taille]:
    if mot not in dict_archive.keys():
        freq=bl.liste_freq2forme(mot)
        dict_archive[mot]=freq
        k=0
        for f in freq:
            fcc[k]=fcc[k]+f/10**6
            k=k+1
    if n%10==0:
        print(fcc)
    n=n+1
        
print(fcc)
    
    
    
pickle.dump(dict_archive,fichier)
fichier.close()
