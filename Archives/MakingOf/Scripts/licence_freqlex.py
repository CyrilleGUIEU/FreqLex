from tkinter import font,LabelFrame,Scrollbar,Listbox,Tk,Text,Button
from tkinter import GROOVE,VERTICAL,WORD,END,DISABLED,S,N 
import webbrowser

from Scripts.gui_freqlex import fenetre_freqlex,LARGEUR_CADRE_ENONCE

FICHIER_LICENCE='Data/LicenceOK'

class Licence:
    def __init__(self,appli):
        self.appli=appli
        fenetre=fenetre_freqlex()
        #On crée les  polices
        police_licence=font.Font(fenetre, size=16, family='Courier')  
        #Ce cadre contient le texte de la licence
        cadre_licence = LabelFrame(fenetre, width=200, height=600, borderwidth=2,
                                relief=GROOVE,text="Licence utilisateur")
        asc_licence=Scrollbar(cadre_licence,orient=VERTICAL)
        texte_licence = Text(cadre_licence, wrap=WORD,font=police_licence)
        fichier_licence=open('Licence')
        texte_licence.insert(END,fichier_licence.read())
        texte_licence.config(state=DISABLED)
        ## association du déplacement de la glissière des scrollbar avec la position visible dans  
        ## le widget Text et inversement.  
        asc_licence.config(command = texte_licence.yview) 
        texte_licence.config(yscrollcommand = asc_licence.set)
        ##Boutons
        bouton_refuse=Button(text="Je refuse cette licence.",command=quit)
        bouton_accepte=Button(text="J'accepte cette licence.",command=self.accepter)
        bouton_questionnaire=Button(text="J'accepte cette licence et je soutiens ce projet en remplissant un questionnaire.",command=self.questionnaire)
        ## Placement du widget Text et des Scrollbar associés 
        texte_licence.grid(column=0, row=0) 
        asc_licence.grid(column=1, row=0, sticky=S+N)
        cadre_licence.grid(column=0,row=0,columnspan=3)
        bouton_refuse.grid(column=0,row=1)
        bouton_accepte.grid(column=1,row=1)
        bouton_questionnaire.grid(column=2,row=1)
        self.fenetre=fenetre
        fenetre.mainloop()
    def accepter(self):
        file=open(FICHIER_LICENCE,'w')
        self.fenetre.destroy()
        self.appli()
    def questionnaire(self):
        page=webbrowser.open_new(r"https://docs.google.com/forms/d/e/1FAIpQLScQAhYsyC77wiTOgC5FnWrms9MMC5n73kj-OdPBgn0IkaoQfA/viewform?usp=sf_link")
        self.accepter()
def cree_cadre_credits(fenetre):
        cadre_credits = LabelFrame(fenetre, height=2, borderwidth=2,
                                relief=GROOVE,text="Crédits:")
        texte_credits = Text(cadre_credits,bg="grey",height=2,width=LARGEUR_CADRE_ENONCE)
        texte_credits.insert(END,"Code source sur: github.com/CyrilleGUIEU/FreqLex \nLa base  lexicale provient de lexique.org")
        texte_credits.grid(column=0,row=0)
        return(cadre_credits)
        
