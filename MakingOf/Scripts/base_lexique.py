# coding: utf8
import sqlite3
import pickle

#Nombre de classements pondérés
NCP=20
#Fichier de sauvegarde des données
FICHIER_SAUVEGARDE="Data/freqlex.dat"
FICHIER_BASE="Scripts/Lexique382.txt"


#Cette fonction renvoie la position du mot dans la liste
def rang_mot(mot,numlexique,lexiquep):
    if mot in lexiquep[numlexique]:
        return(lexiquep[numlexique].index(mot))
    else:
        return(None)

    ###Fonctions de test

def test_base(lexiquep):
    taille_lexique=len(lexiquep[0])
    print("Ce lexique contient :",taille_lexique,"mots.")
    print("test:")
    for n in range(NCP+1):
        pdle=round(n/NCP,2)
        print("pdle="+str(pdle))
        for i in range(100):
            print(str(i)+"->"+lexiquep[n][i])
    while True:
        mot=input("Entrer un mot:")
        for n in range(NCP+1):
            r=rang_mot(mot,n,lexiquep)
            if r!=None:
                print(r)
            else:
                print("Le mot "+mot+" n'est pas dans le lexique.")

def test_base_enrgistree():
    #Récupération des données
    with open (FICHIER_SAUVEGARDE, 'rb') as fp:
        #La variable "lexique" est la liste des graphème ordonnée par fréquence décroissante
        lexiquep = pickle.load(fp)
    test_base(lexiquep)

###Fin des fonctions de test

def genere_base():   
    n=0
    lexiquep=[]
    while n<=NCP:
        #pdle:poids du lexique écrit
        pdle=n/NCP
        print("Génération du lexique pour pdle="+str(pdle))
        #Ouverture du fichier au format utf8 et chargement des entrées -> lecture
        print("Lecture du fichier de lexique.")
        lexique_complet=open(FICHIER_BASE,encoding='utf8')
        lecture=lexique_complet.readlines()

        #Sélection des entrées pertinentes -> entrees
        graphemes=[]
        dernier_grapheme=""
        premier=True
        for ligne in lecture:
            ligne=ligne.split("\t")
            if not premier:
                #0->graphemes
                #8->freq livres
                #9->freq films
                #une_entree=[ligne[0],ligne[9]+ligne[8]]
                #entrees.append(une_entree)
                g,freq=ligne[0],float(ligne[8])*pdle+float(ligne[9])*(1-pdle)
                if g==dernier_grapheme:
                    graphemes[-1][1]=graphemes[-1][1]+freq
                else:
                    graphemes=graphemes+[[g,freq]]
                    dernier_grapheme=g
                if len(graphemes)%10000==0:
                    print(str(len(graphemes)/1400)+"%")
            else:
                premier=False
        #On ferme le fichier
        lexique_complet.close()

        print("Traitement des données.")
        #Création d'une base de données en mémoire
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        #Création de la table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lexique(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             ortho TEXT,
             freq REAL
        )
        """)
        #La table est remplie avec les "entrees"
        cursor.executemany("""
        INSERT INTO lexique(ortho,freq) VALUES(?, ?)""", graphemes)
        #On trie par fréquence décroissante
        lexique_classe=cursor.execute('SELECT * FROM lexique ORDER BY freq DESC')
        conn.commit()
        #On récupère les données -> lexique
        lexique=[]
        for row in lexique_classe:
            lexique.append(row[1])
        lexiquep.append(lexique)
        #Fermeture de la base
        conn.close()

        #Calcul du nombre d'entrées
        taille_lexique=len(lexique)
        print("Lexique généré avec le poids ",str(round(n/NCP,2)), "pour le lexique écrit.")
        print("Il y a "+str(taille_lexique)+" mots dans ce lexique.")
        n=n+1

    #Sauvegarde de la liste
    with open(FICHIER_SAUVEGARDE, 'wb') as fp:
        pickle.dump(lexiquep, fp)
    return lexiquep
   
if __name__=="__main__":
    lexiquep=genere_base()
    test_base(lexiquep)


