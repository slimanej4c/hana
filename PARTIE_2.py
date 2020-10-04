
from tkinter import *
from PARTIE_1 import *

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


        self.bretirer = Button(self.frame1, text="retirer l'arget",command=self.bretirer)
        self.bretirer .grid(row=0, column=1,sticky=S)


        self.repite_solde=0





    # pour un mise a jour de frame 2 pour afficher les nouvelle boutton et effacer les ancians

    def update_frame3(self):
        self.frame3 = Frame(self.root, height=300, width=700, bg='gray')
        self.frame3.grid(row=2, column=0)
        self.frame3.grid_propagate(0)

    # afficher les boutton de partie de triatement les données qui déja scrapy


    def solde (self,num_carte,code_secret,montant):
        self.repite_solde+=1

        if self.repite_solde==3:
            self.update_frame3()
            lmsg = Label(self.frame3, text="code invalide  ")
            lmsg.grid(row=3, column=0)
        else:
                if class_client.consulter_pour_client(num_carte,code_secret )==None or class_carte.select_etat_carte(num_carte)=='non active':

                    if class_client.consulter_pour_client(num_carte,code_secret )==None:
                        self.ecode_secret.delete(0,"end")
                        self.enum_carte.delete(0,"end")
                        self.emontant.delete(0,"end")

                        lmsg = Label(self.frame3, text="votre code secret ou le code de la carte est incorrect veuillez ressayer ")
                        lmsg.grid(row=0, column=0 , pady=20)

                    else:
                        self.update_frame3()
                        lmsg = Label(self.frame3, text="votre carte a été bloquer  ")
                        lmsg.grid(row=3, column=0)
                else:
                    if int(class_client.consulter_pour_client(num_carte, code_secret))<montant:
                        self.update_frame3()
                        lmsg = Label(self.frame3, text="vous avez dépassez votre solde ")
                        lmsg.grid(row=4, column=0)
                    else:
                        self.update_frame3()
                        nouvelle_solde=int(class_client.consulter_pour_client(num_carte,code_secret))-int(montant)
                        num_compte = class_client.select_num_compte_client(num_carte, code_secret)


                        class_compte.debiter_solde(montant,num_compte)

                        lmsg = Label(self.frame3, text="vous avez retirer: "+str(montant)+" votre solde maintenant est: "+str(nouvelle_solde))
                        lmsg.grid(row=4, column=0)






    def bretirer(self):
        self.update_frame3()
        self.bretirer.configure(bg="green")



        lcode_secret = Label(self.frame3, text="entrer le code secret de votre carte ")
        lcode_secret.grid(row=1, column=0)
        self.ecode_secret = Entry(self.frame3)
        self.ecode_secret.grid(row=1, column=1)

        lnum_carte = Label(self.frame3, text="entrer le numéro de votre carte")
        lnum_carte.grid(row=2, column=0)
        self.enum_carte = Entry(self.frame3)
        self.enum_carte.grid(row=2, column=1)

        lmontant = Label(self.frame3, text="entrer le montant en DA")
        lmontant.grid(row=3, column=0)
        self.emontant = Entry(self.frame3)
        self.emontant.grid(row=3, column=1)


        self.bvalider = Button(self.frame3, text='retirer ', command=lambda: self.solde(int(self.enum_carte.get()), int(self.ecode_secret.get()),int(self.emontant.get())))
        self.bvalider.grid(row=4, column=0, sticky=S)













if __name__ == '__main__':
     root=Tk()
     job(root)
     root.mainloop()