"""Interface graphique pour une étude d'énoncé à l'aide d'un lexique fréquentiel
"""


# On importe Tkinter pour construire l'interface graphique
from tkinter import Scale,DISABLED,font,Tk,END,LabelFrame,Button,GROOVE,VERTICAL,WORD,S,N,Frame,Scrollbar,Text,Listbox
#Le module pickle sert à importer les données
import pickle
import webbrowser

#Ces modules sont des modules du projet freqlex
from Scripts.base_lexique import NCP,FICHIER_SAUVEGARDE,rang_mot
from Scripts.gui_freqlex import liste_mots,fenetre_freqlex,LARGEUR_CADRE_ENONCE
from Scripts.licence_freqlex import Licence,cree_cadre_credits,FICHIER_LICENCE
from Scripts.gestion_texte import ensemble_mots
from Scripts.gestion_couleurs import colore_mots,convertit_indice_couleur,COULEUR_ABSENT

#Récupération des données
with open (FICHIER_SAUVEGARDE, 'rb') as fp:
    #La variable "lexique" est la liste des formes orthographiques ordonnées
    #par fréquence décroissante
    lexiquep = pickle.load(fp)

taille_lexique=len(lexiquep[0])
  

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

        #Les données liées à l'énoncé seront stockées dans cette variable
        self.enonce=ensemble_mots(lexiquep)

        # On démarre la boucle Tkinter qui s'interrompt quand on ferme la fenêtre
        fenetre.mainloop()
    #Fonction qui gère le traitement de l'énoncé
    def affiche_liste_mots(self,pdle,zone_mots_lexique,zone_mots_absents):
        #On efface l'affichage des mots absents
        zone_mots_absents.mots.delete(0,END)
        #On génère la liste des mots absents du lexique
        self.enonce.creer_liste_absents(pdle)
        #On insère les mots absents dans la zone des mots absents
        mots_affiches=[] #Ce tableau évite d'afficher les doublons
        for mot in self.enonce.liste_absents:
            if mot.minuscule not in mots_affiches:
                zone_mots_absents.ajoute_mot_couleur(mot.original,COULEUR_ABSENT)
                mots_affiches.append(mot.minuscule)
        #On efface l'affichage des mots du lexique
        zone_mots_lexique.mots.delete(0,END)
        #On génère la liste des mots du lexique
        self.enonce.creer_liste_lexique(pdle)
        #On insère les mots du lexique dans la zone des mots du lexique
        mots_affiches=[] #Ce tableau évite d'afficher les doublons
        for mot in self.enonce.liste_lexique:
            if mot.minuscule not in mots_affiches:
                r=mot.rangs[pdle]
                p=self.enonce.convertit_rang_pourcent(r,pdle)
                chaine=mot.original+"->"+str(p)+"%"
                couleur=convertit_indice_couleur(r,pdle,self.enonce)
                zone_mots_lexique.ajoute_mot_couleur(chaine,couleur)
                mots_affiches.append(mot.minuscule)
                
    
    
        
    def ecoute_clavier(self,event):
        touche = event.keysym
        if touche=="Return":
            self.analyse(event)
            
        
    def analyse(self,event):
        #On efface les éventuelles données
        self.enonce.efface_liste_mots()
        #Extraction du texte à partir du cadre
        self.enonce.ajoute_mots_fenetre(self.texte_enonce,lexiquep[0])
        #Actualisation des affichages des listes de droite
        self.affiche_liste_mots(0,self.mots_lexique_pdle0,self.mots_absents_pdle0)
        self.affiche_liste_mots(NCP,self.mots_lexique_pdle1,self.mots_absents_pdle1)
        pdle=int(self.curseur_pdle.get()/100*NCP)
        self.affiche_liste_mots(pdle,self.mots_lexique_pdle,self.mots_absents_pdle)
        #Coloration des mots de la zone d'énoncé
        colore_mots(self.texte_enonce,pdle,self.enonce)
        
                
             
            



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

