
from tkinter import *
from inner_class import *

class_client = Client(0)
class_compte = Client(0).Compte()
class_carte= Client(0).Compte().Carte()
class job:
    def __init__(self,root):


        self.root = root


        self.x=700
        self.y=400
        self.root.geometry('%sx%s'%(self.x,self.y))

        self.frame1=Frame(self.root,height=50,width=700,bg='green')
        self.frame1.grid(row=0,column=0)
        self.frame1.grid_propagate(0)

        self.frame1.grid_rowconfigure(0,weight=1)

        self.frame2 = Frame(self.root, height=50, width=700, bg='white')
        self.frame2.grid(row=1, column=0)
        self.frame2.grid_propagate(0)

        self.frame3 = Frame(self.root, height=300, width=700, bg='gray')
        self.frame3.grid(row=2, column=0)
        self.frame3.grid_propagate(0)



        self.btraitement=Button(self.frame1,text='consulter le compte',command=self.bconsulter)
        self.btraitement.grid(row=0, column=0,sticky=S)

        self.bentrainement = Button(self.frame1, text="retirer l'arget",command=self.bretirer)
        self.bentrainement.grid(row=0, column=1,sticky=S)





    # pour un mise a jour de frame 2 pour afficher les nouvelle boutton et effacer les ancians

    def update_frame3(self):
        self.frame3 = Frame(self.root, height=300, width=700, bg='gray')
        self.frame3.grid(row=2, column=0)
        self.frame3.grid_propagate(0)

    # afficher les boutton de partie de triatement les données qui déja scrapy

    def consulter(self,num_carte,code_secret):
        if class_client.consulter_pour_client(num_carte, code_secret) == None or class_carte.select_etat_carte(num_carte) == 'non active':

            if class_client.consulter_pour_client(num_carte, code_secret) == None:
                self.update_frame3()
                lmsg = Label(self.frame3, text="votre code secret ou code de carte est incorect  ")
                lmsg.grid(row=3, column=0)

            else:
                self.update_frame3()
                lmsg = Label(self.frame3, text="votre carte a été bloquer  ")
                lmsg.grid(row=3, column=0)

        else:
            self.update_frame3()
            lmsg = Label(self.frame3, text="votre solde est "+str(class_client.consulter_pour_client(num_carte,code_secret)))
            lmsg.grid(row=3, column=0)
    def solde (self,num_carte,code_secret,montant):
        if class_client.consulter_pour_client(num_carte,code_secret )==None or class_carte.select_etat_carte(num_carte)=='non active':

            if class_client.consulter_pour_client(num_carte,code_secret )==None:
                self.update_frame3()
                lmsg = Label(self.frame3, text="votre code secret ou code de carte est incorect  ")
                lmsg.grid(row=3, column=0)

            else:
                self.update_frame3()
                lmsg = Label(self.frame3, text="votre carte a été bloquer  ")
                lmsg.grid(row=3, column=0)
        else:
            if int(class_client.consulter_pour_client(num_carte, code_secret))<montant:
                self.update_frame3()
                lmsg = Label(self.frame3, text="vous avez dépassé votre solde ")
                lmsg.grid(row=4, column=0)
            else:
                self.update_frame3()
                nouvelle_solde=int(class_client.consulter_pour_client(num_carte,code_secret))-int(montant)


                class_compte.update_solde(nouvelle_solde,int(class_client.select_num_compte_client( num_carte, code_secret)))

                lmsg = Label(self.frame3, text="vous avez retirer : "+str(montant)+" votre solde maintenet est :"+str(nouvelle_solde))
                lmsg.grid(row=4, column=0)
    def  bconsulter( self):
        self.update_frame3()
        self.btraitement.configure(bg="green")

        lcode_secret=Label(self.frame3,text="entrer le code secret de votre carte")
        lcode_secret.grid(row=0,column=0)
        ecode_secret=Entry(self.frame3)
        ecode_secret.grid(row=0,column=1)

        lnum_carte = Label(self.frame3, text="entrer le numéro de votre carte de votre carte")
        lnum_carte.grid(row=1, column=0)
        enum_carte = Entry(self.frame3)
        enum_carte.grid(row=1, column=1)

        self.bvalider = Button(self.frame3, text='consulter ',command=lambda:self.consulter(int(enum_carte.get()),int(ecode_secret.get())))
        self.bvalider.grid(row=2, column=0, sticky=S)



    def bretirer(self):
        self.update_frame3()
        self.btraitement.configure(bg="green")

        lcode_secret = Label(self.frame3, text="entrer le code secret de votre carte")
        lcode_secret.grid(row=0, column=0)
        ecode_secret = Entry(self.frame3)
        ecode_secret.grid(row=0, column=1)

        lnum_carte = Label(self.frame3, text="entrer le numéro de votre carte de votre carte")
        lnum_carte.grid(row=1, column=0)
        enum_carte = Entry(self.frame3)
        enum_carte.grid(row=1, column=1)

        lmontant = Label(self.frame3, text="entrer le montant en DA")
        lmontant.grid(row=2, column=0)
        emontant = Entry(self.frame3)
        emontant.grid(row=2, column=1)



        self.bvalider = Button(self.frame3, text='retirer ',
                               command=lambda: self.solde(int(enum_carte.get()), int(ecode_secret.get()),int(emontant.get())))
        self.bvalider.grid(row=3, column=0, sticky=S)

    # pour afficher les boutton de partie de train












if __name__ == '__main__':
     root=Tk()
     job(root)
     root.mainloop()