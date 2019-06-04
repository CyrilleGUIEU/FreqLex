from tkinter import font,LabelFrame,Scrollbar,Listbox,Tk,GROOVE,VERTICAL,S,N 

#Paramètres de l'interface graphique
LARGEUR_CADRE_ENONCE=50
LARGEUR_LISTE_MOTS=25

class liste_mots:
    """Définit un cadre contenant une liste de mot avec un ascenseur"""
    def __init__(self,parent,titre):
        police_mots=font.Font(parent, size=12, family='Courier')
        self.cadre = LabelFrame(parent, borderwidth=2,
                                relief=GROOVE,text=titre)
        self.ascenseur=Scrollbar(self.cadre,orient=VERTICAL)
        self.mots=Listbox(self.cadre, font=police_mots, width=LARGEUR_LISTE_MOTS,yscrollcommand = self.ascenseur.set )
        self.mots.grid(column=0,row=0)
        self.ascenseur.grid(column=1,row=0,sticky=S+N)
        self.ascenseur.config( command = self.mots.yview )
def fenetre_freqlex():
    fenetre=Tk()
    fenetre.title('FreqLex')
    fenetre.wm_iconbitmap('DATA/icon.ico')
    return(fenetre)

