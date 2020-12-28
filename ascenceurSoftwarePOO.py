import time
from pynput.keyboard import Key, Listener
from tkinter import *

"""---------------------------------------------------------

Pour que le code fonctionne, il faut installer les modules keyboard et pynput avec les commandes suivantes:
pip3 install keyboard 
pip install pynput
  ---------------------------------------------------------------"""


class Ascenseur:


    """ Création de la classe ascenseur"""

    def __init__(self):

        """Création du constructeur de la classe pour initialiser ses attributs """

        self.positionAscenseur=0  # attribut qui représente l'étage où se trouve l'ascenseur
        self.nombreEtage=1
        self.etages=[0]
        self.poidsMax="500 Kg"   # poids maximal autorisé
        self.porteOuverte=False  # attribut pour vérifier si la port de l'ascenseur est ouverte ou non
        self.initialiserPositionAscenseur()


        self.window = Tk()
        self.window.geometry("900x500")
        self.window.title("Ascenseur")
        self.canvas = Canvas(self.window)

        self.entree1=IntVar(self.window)#nombre d'étages
        self.entree2=IntVar(self.window)#position d'utilisateur

        '-----------------------Affichez Ascenseur------------------'
        Label(self.window, font=('Calibri', 20, 'bold'), text="Ascenseur", fg="black").grid(row=1, column=4, padx=350, pady=30)

        '-----------------------Entrer et valider le nombre d\'étage------------------'
        Label(self.window, font=('Calibri', 15, 'bold'), text="entrez le nombre d'étages", fg='black').place(relx=.07,rely=.25)
        self.entreNombreEtages=Spinbox(self.window,from_= 1, to= 100, textvariable=self.entree1, width=10,state='readonly').place(relx=.433,rely=.265)
        Button(self.window, text="Valider", command=self.getNombreEtage, width=15).place(relx=.52,rely=.26)

        '-----------------------Appel d\'asceseur à l\'étage de l\'utilisateur------------------'
        Label(self.window, font=('Calibri', 15, 'bold'), text="Vous êtes en quel étage", fg='black').place(relx=.07,rely=.3)
        self.entrePositionUtilisateur = Spinbox(self.window,from_= 0, to=100, textvariable=self.entree2, width=10,state='readonly').place(relx=.433, rely=.32)
        self.appelAscenseurButton=Button(self.window, text="Appel d'ascenseur", width=15, command=self.appelAscenseur).place(relx=.52, rely=.32)

        '----------------------Mise en place des boutons goUP et goDown---------------------'
        self.goUpButton=Button(self.window, text="goUp", width=10,command=self.goUp).place(relx=.423, rely=.39)
        self.goDownButton=Button(self.window, text="goDown", width=10, command=self.goDown).place(relx=.423, rely=.44)

        '----------------------Vous voulez partir en quelle étage---------------------'
        Label(self.window, font=('Calibri', 15, 'bold'), text="Vous voulez partir en quel étages ?", fg='black').place(relx=.07,rely=.5)
        self.entrePositionUtilisateur = Spinbox(self.window, textvariable=self.entree2, width=10,state='readonly').place(relx=.433,rely=.515)
        self.goButton=Button(self.window, text="go", width=15, command=self.go).place(relx=.52, rely=.51)


        self.can = Canvas(self.window, width=500, height =105)
        self.can.place(relx=.045, rely=.59)
        self.can.create_line(10, 37, 350, 37, width=1)  # fils
        self.can.create_line(10, 37, 10, 1, width=1)  # fils
        self.can.create_line(10, 3, 350, 3, width=1)  # fils
        self.can.create_line(350, 37, 350, 1, width=1)  # fils

        '----------------------étage où se trouve l\'ascenseur---------------------'
        self.afficher1=Label(self.window, font=('Calibri', 15, 'bold'), text="L'ascenseur est arrivé à l'étage : ", fg='black').place(relx=.07, rely=.6)
        self.afficheur2=Label(self.window, font=('Calibri', 15, 'bold'), text=self.positionAscenseur).place(relx=.38, rely=.6)

        '----------------------Arrêt d\'urgence---------------------------------'
        Button(self.window, text="Arrêt d'urgence", width=15, command=self.arretUrgence).place(relx=.52, rely=.8)

        Button(self.window, text="mettre en marche", width=15, command=self.remiseEnMarche).place(relx=.32, rely=.8)

        self.message = Label(self.window, font=('Calibri', 13, 'bold'), text="").place(relx=.17, rely=.7)

        self.panne=Label(self.window, font=('Calibri', 15, 'bold'), text="                                 ", fg='black').place(relx=.32,rely=.9)
        self.marche = Label(self.window, font=('Calibri', 15, 'bold'), text="                                 ",fg='black').place(relx=.32, rely=.9)


        self.window.resizable(width=False,height=False)
        self.window.mainloop()


    def getNombreEtage(self):
        """méthode qui permet de récuperer le nombre d'étage entré par l'utilisateur"""
        self.nombreEtage=self.entree1.get()
        Label(self.window, font=('Calibri', 15, 'bold'), text="Le nombre d'étage est : ").place(relx=.68, rely=.25)
        Label(self.window, font=('Calibri', 15, 'bold'), text=self.nombreEtage).place(relx=.92, rely=.25)
        self.entreNombreEtages=Entry(self.window, textvariable=self.entree1,state='disabled', width=10).place(relx=.433,rely=.265)
        Button(self.window, text="Valider", command=self.getNombreEtage, width=15, state='disabled').place(relx=.52,rely=.26)
        self.etages = [0] * (self.nombreEtage + 1)
        self.etages[0] = 1
        print(self.etages)

    def initialiserPositionAscenseur(self):
        """ Méthode qui initialise la liste qui représente la position de l'ascenseur"""
        self.etages = [0] * (self.nombreEtage + 1)
        self.etages[0]=1
        print("L'ascenseur est dans l'étage ",self.positionAscenseur,"\n",self.etages)

    def goUp(self):
        """Méthode pour monter d'un étage
        On fait monter l'ascenseur d'un étage"""

        for i in range(self.nombreEtage+1):
            if(self.etages[i]==1):
                if (i < self.nombreEtage):
                    self.etages[i] = 0
                    self.etages[i + 1] = 1
                    self.positionAscenseur = i + 1
                    time.sleep(1)
                    print("l\'ascenseur est arrivé à l\'étage", self.positionAscenseur)
                    Label(self.window, font=('Calibri', 15, 'bold'), text="L'ascenseur est arrivé à l'étage :  ", fg='black').place(relx=.07, rely=.6)
                    Label(self.window, font=('Calibri', 15, 'bold'), text=self.positionAscenseur).place(relx=.38, rely=.6)

                    break
                else:
                    print("l\'ascenseur est en dernière étage")
                    self.afficher1=Label(self.window, font=('Calibri', 15, 'bold'), text="l'ascenseur est en dernière étage  ").place(relx=.07,rely=.6)
                    break

    def goDown(self):
        """Méthode pour descendre d'un étage.
            On fait descendre l'ascenseur d'un étage"""

        for i in range(self.nombreEtage + 1):
            if (self.etages[i] == 1):
                if (i > 0):
                    self.etages[i] = 0
                    self.etages[i - 1] = 1
                    self.positionAscenseur = i - 1
                    time.sleep(1)
                    #print("l\'ascenseur est arrivé à l\'étage", self.positionAscenseur)
                    Label(self.window, font=('Calibri', 15, 'bold'), text="L'ascenseur est arrivé à l'étage :  ",fg='black').place(relx=.07, rely=.6)
                    Label(self.window, font=('Calibri', 15, 'bold'), text=self.positionAscenseur).place(relx=.38, rely=.6)
                    break
                else:
                    print("l'ascenseur est au rez-de-chaussée")
                    Label(self.window, font=('Calibri', 15, 'bold'), text="l'ascenseur est au rez-de-chaussée").place(relx=.07, rely=.6)
                    break

    def ouvrirPorte(self):
        """ méthode qui ouvre automatiquement la porte de l'ascenseur"""

        print("2 secondes pour l'ouverture de porte")
        self.porteOuverte = True
        time.sleep(2)  # attendre 2 secoundes pour l'ouverture de la porte de l'acsenseur

    def fermerPorte(self):
        """"" méthode qui ouvre automatiquement la porte de l'ascenseur"""

        print("2 secondes pour la fermeture de porte")
        self.porteOuverte = False
        time.sleep(2)  # attendre 2 sencondes pour la fermeture de la porte de l'acsenseur

    def appelAscenseur(self):
        """Méthode qui permet de faire un appel d'ascenseur
            pour qu'il vient à l'étage de l'utilisateur"""
        positionUtilisateur=self.entree2.get()
        if (positionUtilisateur < self.positionAscenseur):
            if(self.porteOuverte):
                self.fermerPorte()
            if(positionUtilisateur<0):
                self.message=Label(self.window, font=('Calibri', 13, 'bold'), text="Veuillez rentrer un numéro d'étage valide").place(relx=.3, rely=.7)
            else:
                while (positionUtilisateur < self.positionAscenseur):
                    self.goDown()
                    #Label(self.window, font=('Calibri', 15, 'bold'), text="L'ascenseur est arrivé à l'étage : ",fg='black').place(relx=.07, rely=.6)
                    Label(self.window, font=('Calibri', 15, 'bold'), text=self.positionAscenseur).place(relx=.38, rely=.6)
                    self.message = Label(self.window, font=('Calibri', 13, 'bold'),text="                                                                                            ").place(relx=.17, rely=.7)
            print(self.etages)
            self.ouvrirPorte()
            #Label(self.window, font=('Calibri', 14, 'bold'), text="                                           La porte est ouverte                                                                                               ").place(relx=.17, rely=.7)



        elif (positionUtilisateur > self.positionAscenseur):
            if (self.porteOuverte):
                self.fermerPorte()
            if(positionUtilisateur>self.nombreEtage):
                self.message=Label(self.window, font=('Calibri', 13, 'bold'), text="Veuillez rentrer un numéro d'étage valide").place(relx=.3, rely=.7)
            else:
                while (positionUtilisateur > self.positionAscenseur):
                    self.goUp()
                    #Label(self.window, font=('Calibri', 15, 'bold'), text="L'ascenseur est arrivé à l'étage : ",fg='black').place(relx=.07, rely=.6)
                    Label(self.window, font=('Calibri', 15, 'bold'), text=self.positionAscenseur).place(relx=.38, rely=.6)
                    self.message = Label(self.window, font=('Calibri', 13, 'bold'), text="                                                                                   ").place(relx=.3, rely=.7)
            print(self.etages)
            self.ouvrirPorte()
            #Label(self.window, font=('Calibri', 14, 'bold'),text="Veuillez rentrer un numéro d'étage différent de l'étage actuel",state='disable').place(relx=.32, rely=.7)
            #Label(self.window, font=('Calibri', 14, 'bold'),text="                                           La porte est ouverte                                                                                               ").place(relx=.17, rely=.7)
        else:
            self.ouvrirPorte()
            print("Veuillez rentrer un numéro d'étage différent de l'étage actuel")
            #  Label(self.window, font=('Calibri', 14, 'bold'), text="La porte est ouverte, veuillez entrer dans l'ascenseur").place(relx=.32,rely=.7)

    def go(self):
        """Méthode qui permet de partir directement à un étage spécifique"""
        positionUtilisateur=self.entree2.get()
        if(positionUtilisateur==self.positionAscenseur):
            self.message=Label(self.window, font=('Calibri', 14, 'bold'),text="Veuillez rentrer un numéro d'étage différent de l'étage actuel").place(relx=.17, rely=.7)
        else:
            self.message = Label(self.window, font=('Calibri', 14, 'bold'),text="                                                                                                                                          ").place(relx=.17,rely=.7)
            self.appelAscenseur()

    def arretUrgence(self):
        """Méthode qui permet d'arrêter le fonctionnement de l'ascenseur en cas d'urgence ou si l'ascenseur tombe en panne"""

        #Button(self.window, text="Valider", command=self.getNombreEtage, width=15,state='disabled').place(relx=.52, rely=.26)
        Button(self.window, text="Appel d'ascenseur", width=15, command=self.appelAscenseur, state='disabled').place(relx=.52, rely=.32)
        Button(self.window, text="goDown", width=10, command=self.goDown,  state='disabled').place(relx=.423, rely=.44)
        Button(self.window, text="goUp", width=10,command=self.goUp,  state='disabled').place(relx=.423, rely=.39)
        Button(self.window, text="go", width=15, command=self.go, state='disabled').place(relx=.52, rely=.51)
        self.marche = Label(self.window, font=('Calibri', 15, 'bold'), text="                                 ",fg='black').place(relx=.32, rely=.9)
        self.panne=Label(self.window, font=('Calibri', 15, 'bold'), text="L'ascenseur est en panne  ", fg='black').place(relx=.32,rely=.9)

    def remiseEnMarche(self):
        """Méthode qui permet de remettre l'ascenseur en marche après réparation"""
        #Button(self.window, text="Valider", command=self.getNombreEtage, width=15,state='normal').place(relx=.52, rely=.26)
        Button(self.window, text="Appel d'ascenseur", width=15, command=self.appelAscenseur, state='normal').place(relx=.52, rely=.32)
        Button(self.window, text="goDown", width=10, command=self.goDown,  state='normal').place(relx=.423, rely=.44)
        Button(self.window, text="goUp", width=10,command=self.goUp,  state='normal').place(relx=.423, rely=.39)
        Button(self.window, text="go", width=15, command=self.go, state='normal').place(relx=.52, rely=.51)
        self.panne=Label(self.window, font=('Calibri', 15, 'bold'), text="                                 ", fg='black').place(relx=.32,rely=.9)
        self.marche=Label(self.window, font=('Calibri', 15, 'bold'), text="L'ascenseur est en marche", fg='black').place(relx=.32,rely=.9)


    def lancerAscenseur(self, enPanne):
        """Méthode qui permet de simuler l'ascenseur dans la console du compilateur"""
        while (enPanne != 1):

            '------------------------------------------------------'
            """savoir l'étage de l'utilisateur"""
            while True:
                positionUtilisateur = input('\nVous etes en quel étage?\n ')
                try:
                    positionUtilisateur = int(positionUtilisateur)
                    if (positionUtilisateur > ascenseur1.nombreEtage):
                        print("Veuillez rentrer un nombre d\étage valide")
                    else:
                        break;
                except ValueError:
                    print("Veuillez rentrer un numéro")

            print("l\'ascenseur est dans l'étage", self.positionAscenseur)

            self.appelAscenseur(positionUtilisateur)


            """-------------Boucle qui va s'éxecuter tant que l'utilisateur n'est pas arrivé à sa destination ( étage souhaité) """
            while True:
                direction = input("\npour monter cliquez sur 'u' + entrer\npour descendre cliquez sur 'd' + entrer\n")

                """------------------utilisation de la commande goUp() pour monter"""
                if (direction == "u"):
                    print("Vous avez choisi de monter d'un étage")
                    self.fermerPorte()
                    self.goUp()

                    print("\nEst-ce que vous êtes arrivé à l'étage souhaité?\n")
                    destination = 'a'
                    while (destination != 'y' and destination != 'n'):
                        destination = input("si oui cliquez sur 'y'+entrer sinon clickez sur 'n'+entrer\n")

                    if destination == "y":
                        break
                    elif (destination == "n"):
                        pass


                elif (direction == "d"):
                    print("Vous avez choisi de descendre d'un étage")
                    self.fermerPorte()
                    self.goDown()

                    print("\nEst-ce que vous êtes arrivé à l'étage souhaité?\n")
                    destination = 'a'
                    while (destination != 'y' and destination != 'n'):
                        destination = input("si oui cliquez sur 'y'+entrer sinon clickez sur 'n'+entrer\n")

                    if destination == "y":
                        break
                    elif (destination == "n"):
                        pass
                    else:
                        with Listener(on_release=on_release) as listener:
                            listener.join()

            self.ouvrirPorte()
            time.sleep(5) #temps d'attente pour que l'utilisateur rentre dans l'ascenseur

            # Collect events until released
            print("En cas d'urgence cliquez sur échape sinon cliquez sur n'importe quel autre charactère\n ")
            time.sleep(2)
            with Listener(on_release=on_release) as listener:
                listener.join()

def on_release(key):
    """Fonction qui met l'ascenseur à l'arrêt en cas d'urgence pour la partie de simulation dans la console si
        l'utilisateur appuie sur la touche échape du clavier"""

    if key == Key.esc:
        print("l'ascenseur est en panne, arrêt d'urgence")
        global enPanne
        enPanne = 1
        return False
    else:
        return False



def entrezDansAscenseur():
    """fonction qui met un temps d'attente pour que l'utilisateur rentre dans l'ascenseur """
    print("10 secondes d'attente pour que l\'utilisateur rentre dans l\'ascenseur")
    time.sleep(10)  # attendre 10 sencondes pour que l'utilisateur entre dans l'acsenseur


def sortezAscenseur():
    """fonction qui met un temps d'attente pour que l'utilisateur rentre dans l'ascenseur """
    print("10 secondes d'attente pour que l\'utilisateur sort de l\'ascenseur")
    time.sleep(10)  # attendre 10 sencondes pour que l'utilisateur sort de l'acsenseur


"""Création d'un objet ascenseur """
ascenseur1=Ascenseur()
print("le poids maximal supporté est : ",ascenseur1.poidsMax)

"""Mettre l'ascenseur en marche"""
global enPanne
enPanne = 0  # bon fonctionnement
global positionUtilisateur

print("\nEn cas durgence appuyez sur la touche échape sinon appuyez sur n'importe quel autre touche du clavier\n ")

time.sleep(2)
with Listener(on_release=on_release) as listener:
    listener.join()



ascenseur1.lancerAscenseur(enPanne)





#ProgName= Label(window,font=('Calibri', 15,'bold'), text="ascenseur",fg="blue")
#ProgName.grid(row=1,column=3, padx=200,pady=30)


#ligne_texte=Label(window,font=('Calibri',15,'bold'), text="entrez le nombre d'étage",fg='black')
#ligne_texte.place(relx=.03,rely=.25)
#nombreEtage=IntVar()
#nbrEtage=Spinbox(window,from_=1,to=100, variable=nombreEtage)
#nbrEtage.place(relx=.31,rely=.265)

#"monter=Button(window,text="goUp")
#monter.place(relx=.31,rely=.33)


#descendre=Button(window,text="goDown")
#descendre.place(relx=.39,rely=.33)

#positionAscenseur=Text(window, height=1, width=8)
#positionAscenseur.place(relx=.35,rely=.9)

#window.mainloop()
