"""Interface graphique pour une étude d'énoncé à l'aide d'un lexique fréquentiel
"""
# On importe Tkinter pour construire l'interface graphique
from tkinter import Scale,DISABLED,font,Tk,END,LabelFrame,Button,GROOVE,VERTICAL,WORD,S,N,Frame,Scrollbar,Text,Listbox
#Le module pickle sert à importer les données
import pickle
import webbrowser

#Ce module est un module du projet freqlex
from Scripts.base_lexique import NCP,FICHIER_SAUVEGARDE,rang_mot
from Scripts.gui_freqlex import liste_mots,fenetre_freqlex,LARGEUR_CADRE_ENONCE
from Scripts.licence_freqlex import Licence,cree_cadre_credits,FICHIER_LICENCE




#Récupération des données
with open (FICHIER_SAUVEGARDE, 'rb') as fp:
    #La variable "lexique" est la liste des graphème ordonnée par fréquence décroissante
    lexiquep = pickle.load(fp)

taille_lexique=len(lexiquep[0])


    
def texte_liste(t1):
    """Cette fonction transforme un texte en liste de mots"""
    liste_mots=[]
    i=0
    mot=""
    t=t1+"."
    exceptions=["'","-"]
    while t!="":        
        if t[i].isalpha() or t[i] in exceptions :
            mot=t[0:i+1]
            i=i+1
        else:
            t=t[i+1:]
            if mot!="":
                if mot in lexiquep[0]:
                    if mot not in liste_mots:
                        liste_mots.append(mot)
                else:
                    for e in exceptions:
                        mots=mot.split(e)
                        for m in mots:
                            if mot not in liste_mots:
                                liste_mots.append(m)
                        
            mot=""
            i=0
    return liste_mots

class GUI():
    def __init__(self):
        fenetre=fenetre_freqlex()
        #On crée les  polices
        police_mots=font.Font(fenetre, size=16, family='Courier')
        police_enonce=font.Font(fenetre, size=12, family='Courier')  
        #Definition de l'interface graphique
        #Ce cadre contient le texte à analyser
        cadre_enonce = LabelFrame(fenetre, borderwidth=2,
                                relief=GROOVE,text="Enoncé")
        asc_enonce=Scrollbar(cadre_enonce,orient=VERTICAL)
        #L'attribut texte_enonce est utilisé par la méthode recupere_texte
        self.texte_enonce = Text(cadre_enonce, wrap=WORD,font=police_enonce,width=LARGEUR_CADRE_ENONCE)
        self.texte_enonce.bind("<Key>", self.ecoute_clavier)
        ## association du déplacement de la glissière des scrollbar avec la position visible dans  
        ## le widget Text et inversement.  
        asc_enonce.config(command = self.texte_enonce.yview) 
        self.texte_enonce.config(yscrollcommand = asc_enonce.set)
        ## Placement du widget Text et des Scrollbar associés 
        self.texte_enonce.grid(column=0, row=0) 
        asc_enonce.grid(column=1, row=0, sticky=S+N)
        
        #Ce cadre contient les deux cadres de listes de mots
        cadre_listes=LabelFrame(fenetre, text="Analyse fréquentielle \n 0->très fréquent 100->très rare",width=200, height=600, borderwidth=2,
                                relief=GROOVE)
        
        #Ce cadre contient les mots du lexique classés -pdle=0
        self.mots_lexique_pdle0=liste_mots(cadre_listes,"Classement par difficulté lexicale \n Poids de l'écrit = 0%")
        self.mots_lexique_pdle0.cadre.grid(column=0,row=0)

        #Ce cadre contient les mots absents du lexique
        self.mots_absents_pdle0 = liste_mots(cadre_listes,"Mots absents du lexique")
        self.mots_absents_pdle0.cadre.grid(column=0,row=1)

        #Ce cadre contient les mots du lexique classés -pdle=1
        self.mots_lexique_pdle1=liste_mots(cadre_listes,"Classement par difficulté lexicale \n Poids de l'écrit = 100%")
        self.mots_lexique_pdle1.cadre.grid(column=2,row=0)

        #Ce cadre contient les mots absents du lexique
        self.mots_absents_pdle1 = liste_mots(cadre_listes,"Mots absents du lexique")
        self.mots_absents_pdle1.cadre.grid(column=2,row=1)

        #Ce cadre contient les mots du lexique classés -pdle
        self.mots_lexique_pdle=liste_mots(cadre_listes,"Classement par difficulté lexicale \n Poids variable")
        self.mots_lexique_pdle.cadre.grid(column=1,row=0)

        #Ce cadre contient les mots absents du lexique
        self.mots_absents_pdle = liste_mots(cadre_listes,"Mots absents du lexique")
        #self.mots_absents_pdle.cadre.grid(column=2,row=1)
        #Curseur
        self.curseur_pdle=Scale(cadre_listes, orient='horizontal',
                                from_=0, to=100,
                                resolution=100/NCP, tickinterval=2,
                                label="Poids de l'écrit(%) ",
                                command=self.analyse)
        self.curseur_pdle.set(50)
        self.curseur_pdle.grid(column=1,row=1)

        
        #Ce cadre contient le texte des crédits
        cadre_credits = cree_cadre_credits(fenetre)

        #On place les cadres de premier niveau
        cadre_listes.grid(column=1,row=0,rowspan=2)
        cadre_enonce.grid(column=0,row=0)
        cadre_credits.grid(column=0,row=1)            

        # On démarre la boucle Tkinter qui s'interrompt quand on ferme la fenêtre
        fenetre.mainloop()
    #Fonction qui gère le traitement de l'énoncé
    def affiche_liste_mots(self,pdle,les_mots,zone_mots_lexique,zone_mots_absents):
        dict_mots={}
        indices_mots=[]
        mots_absents=[]
        for mot in les_mots:
            mot_init=mot
            mot=mot.lower()
            r=rang_mot(mot,pdle,lexiquep)
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
        zone_mots_lexique.mots.delete(0,END)
        #On insère les nouveaux mots dans le classement
        for i in indices_mots:
            zone_mots_lexique.mots.insert(END, dict_mots[i]+"->"+str(int(100*i/taille_lexique)))
        #On efface la liste des mots absents pour la reconstruire à partir des
        #données actualisées
        zone_mots_absents.mots.delete(0,END)
        for mot in mots_absents:
            zone_mots_absents.mots.insert(END, mot)        
    def ecoute_clavier(self,event):
        touche = event.keysym
        if touche=="Return":
            self.analyse(event)
        
    def analyse(self,event):       
        #Extraction du texte à partir du cadre
        texte_brut=self.texte_enonce.get("1.0",END)
        #Génération de la liste de mots à partir du texte brut
        les_mots=texte_liste(texte_brut)
        #Ce dictionnaire contiendra les mots avec la casse
        #du texte en fonction de leur rang
        self.affiche_liste_mots(0,les_mots,self.mots_lexique_pdle0,self.mots_absents_pdle0)
        self.affiche_liste_mots(NCP,les_mots,self.mots_lexique_pdle1,self.mots_absents_pdle1)
        pdle=int(self.curseur_pdle.get()/100*NCP)
        self.affiche_liste_mots(pdle,les_mots,self.mots_lexique_pdle,self.mots_absents_pdle)
        



print("Démarrage de l'interface graphique...")
# On teste si la licence a été acceptée
fichier_ouvert=False
try:
    open(FICHIER_LICENCE,"r")
    #Lancement de l'application
    fichier_ouvert=True
    GUI()
except FileNotFoundError:
    #Fenêtre d'acceptation de la licence
    if fichier_ouvert==False:
        Licence(GUI)

