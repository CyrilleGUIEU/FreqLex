"""Interface graphique pour une étude d'énoncé à l'aide d'un lexique fréquentiel
"""
# On importe Tkinter
from tkinter import font,Tk,END,LabelFrame,GROOVE,VERTICAL,WORD,S,N,Frame,Scrollbar,Text,Listbox
import pickle


#Récupération des données
with open ('freqlex.dat', 'rb') as fp:
    lexique = pickle.load(fp)

taille_lexique=len(lexique)

def rang_mot(mot):
    """#ette fonction renvoie la position du mot dans la liste"""
    if mot in lexique:
        return(lexique.index(mot))
    else:
        return(None)
    
def texte_liste(t1):
    """Cette fonction transforme un texte en liste de mots"""
    liste_mots=[]
    i=0
    mot=""
    t=t1+"."
    while t!="":        
        if t[0:i+1].isalpha():
            mot=t[0:i+1]
            i=i+1
        else:
            t=t[i+1:]
            if mot!="":
                liste_mots.append(mot)
            mot=""
            i=0
    return liste_mots


print("Démarrage de l'interface graphique...")



# On crée une fenêtre, racine de notre interface
fenetre = Tk()

#On crée les  polices
police_mots=font.Font(fenetre, size=16, family='Courier')
police_enonce=font.Font(fenetre, size=12, family='Courier')


#Fonctions qui gèrent les évènements
def recupere_texte(la_zone):
    t=la_zone.get("1.0",END)
    return(t)

def ecoute_clavier(event):
    touche = event.keysym
    if touche=="Return":
        #Extraction du texte à partir du cadre
        texte_brut=recupere_texte(texte_enonce)
        #Génération de la liste de mots à partir du texte brut
        les_mots=texte_liste(texte_brut)
        #Ce dictionnaire contiendra les mots avec la casse
        #du texte en fonction de leur rang
        dict_mots={}
        indices_mots=[]
        mots_absents=[]
        for mot in les_mots:
            mot_init=mot
            mot=mot.lower()
            r=rang_mot(mot)
            #Si le mot n'est pas dans le lexique ...
            if r==None:
                #...on le met dans les mots absents si il n'y est pas déjà
                if mot_init not in mots_absents:
                    mots_absents.append(mot_init)
            else:
            #Sinon on l'ajoute au dictionnaire si il n'y est pas déjà
                if not r in dict_mots:
                    dict_mots[r]=mot_init
                    #On conserve une liste d'indices pour le classement
                    indices_mots.append(r)
        #Classement par niveau de rareté décroissant
        indices_mots.sort(reverse=True)
        #On efface l'affichage du classement
        liste_mots.delete(0,END)
        #On insère les nouveaux mots dans le classement
        for i in indices_mots:
            liste_mots.insert(END, dict_mots[i]+"->"+str(int(100*i/taille_lexique)))
        #On efface la liste des mots absents pour la reconstruire à partir des
        #données actualisées
        liste_mots_absents.delete(0,END)
        for mot in mots_absents:
            liste_mots_absents.insert(END, mot)
        
        
#Definition de l'interface graphique
            
#Ce cadre contient le texte à analyser
cadre_enonce = LabelFrame(fenetre, width=200, height=600, borderwidth=2,
                        relief=GROOVE,text="Enoncé")
asc_enonce=Scrollbar(cadre_enonce,orient=VERTICAL)

#La variable globale texte_enonce est utilisée par la fonction recupere_texte
texte_enonce = Text(cadre_enonce, wrap=WORD,font=police_enonce)
texte_enonce.bind("<Key>", ecoute_clavier)
## association du déplacement de la glissière des scrollbar avec la position visible dans  
## le widget Text et inversement.  
asc_enonce.config(command = texte_enonce.yview) 
texte_enonce.config(yscrollcommand = asc_enonce.set)
## Placement du widget Text et des Scrollbar associés 
texte_enonce.grid(column=0, row=0) 
asc_enonce.grid(column=1, row=0, sticky=S+N)
cadre_enonce.grid(column=0,row=0)

   



#Ce cadre contient les deux cadres de listes de mots
cadre_listes=Frame(fenetre, width=200, height=600, borderwidth=2,
                        relief=GROOVE)
cadre_listes.grid(column=1,row=0)

#Ce cadre contient les mots du lexique classés
cadre_mots = LabelFrame(cadre_listes, width=200, height=400, borderwidth=2,
                        relief=GROOVE,text="Classement par difficulté lexicale \n 0->très fréquent 100->très rare")
asc_mots=Scrollbar(cadre_mots,orient=VERTICAL)

#La variable globale liste_mots est utilisée par la fonction ecoute_clavier
liste_mots=Listbox(cadre_mots, font=police_mots, yscrollcommand = asc_mots.set )

liste_mots.grid(column=0,row=0)
asc_mots.grid(column=1,row=0,sticky=S+N)
asc_mots.config( command = liste_mots.yview )
cadre_mots.grid(column=1,row=0)


#Ce cadre contient les mots absents du lexique
cadre_absents = LabelFrame(cadre_listes, width=200, height=200, borderwidth=2,
                        relief=GROOVE,text="Mots absents du lexique")
asc_mots_absents=Scrollbar(cadre_absents,orient=VERTICAL)

#La variable globale liste_mots_absents est utilisée par la fonction ecoute_clavier
liste_mots_absents=Listbox(cadre_absents, font=police_mots, yscrollcommand = asc_mots_absents.set )

liste_mots_absents.grid(column=0,row=0)
asc_mots_absents.grid(column=1,row=0,sticky=S+N)
asc_mots_absents.config( command = liste_mots_absents.yview )
cadre_absents.grid(column=1,row=1)

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
