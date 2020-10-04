import sqlite3
import random
import pandas as pandas
import datetime
#ouvrir la base de données chinook
connection=sqlite3.connect('chinook.db')

cur=connection.cursor()

cur.execute("PRAGMA foreign_keys = ON")


class Client:
    def __init__(self,v):
        if v==1:
            self.num_compte_default = "{:04d}".format(random.randint(0, 9999))
            self.num_carte_default = "{:04d}".format(random.randint(1, 9999))


            self.create_table_client()
            self.create_table_compte()
            self.create_table_carte()
            self.default_num()
            self.depart()

        else:



          pass

    def create_table_client(self):

        cur.execute('create table if not exists Client_table (code_client integer  primary key   AUTOINCREMENT, nom VARCHAR (25) ,'
                    'prenom varchar(25),code_agence varchar (20),tel  int(11) )')


    def create_table_compte(self):


        cur.execute('create table if not exists Compte_table (num_compte varchar(25)   primary key  ,code_client integer , solde int(11), FOREIGN KEY(code_client) REFERENCES Client_table(code_client) ON DELETE CASCADE)')
        connection.commit()
    def create_table_carte(self):

        cur.execute('create table if not exists Carte_table (num_carte varchar(25)   primary key ,num_compte varchar(25)  ,'
                    'code_secret varchar(25),date_expiration varchar(20),etat_carte varchar(25), FOREIGN KEY(num_compte ) REFERENCES Compte_table (num_compte ) ON DELETE CASCADE)')
        connection.commit()


    def ajouter_client (self,nom,prenom,code_agence,tel):


        cur.execute('insert into Client_table (nom,prenom,code_agence,tel)values(?,?,?,?)',
                    (nom,prenom,code_agence,tel))

        connection.commit()

    def ajouter_carte(self, num_carte,num_compte,code_secret,date_expiration,etat_carte):
        cur.execute(
            'insert into Carte_table (num_carte,num_compte ,code_secret,date_expiration,etat_carte)values(?,?,?,?,?)',
            ( num_carte,num_compte,code_secret,date_expiration,etat_carte))

        connection.commit()

    def bloquer_carte (self,num_carte):
        if self.select_etat_carte(num_carte)=="active":
            cur.execute('UPDATE Carte_table SET etat_carte = "non active"  where num_carte = (?);''',(num_carte,))

            connection.commit()
            print("la carte a été bloquer avec succés")
        else:
           print("cette carte a été déja bloqué")

    def debloquer_carte (self,num_carte):
        if self.select_etat_carte(num_carte)=="non active":
            cur.execute('UPDATE Carte_table SET etat_carte = "active"  where num_carte = (?);''',(num_carte,))

            connection.commit()
            print("la carte a été debloquer avec succés")
        else:
           print("cette carte a été déja debloqué")

    def modifier_code_secret (self,code_secret,num_carte):
        cur.execute('UPDATE Carte_table SET code_secret = (?)  where num_carte = (?);''', (code_secret,num_carte,))

        connection.commit()
        print("la code sectrer de carte a été changé avec succés")


    def update_solde (self,solde,num_compte):
        cur.execute('UPDATE Compte_table SET solde = (?)  where num_compte = (?)', (solde,num_compte,))

        connection.commit()
        print("la code sectrer de carte a été changé avec succés")
    def ajouter_compte(self, num_compte,code_client,solde):
        cur.execute(
            'insert into Compte_table (num_compte,code_client,solde)values(?,?,?)',
            (num_compte,code_client,solde))

        connection.commit()

    def supprimer_compte(self, num_compte):

        if int(num_compte) in self.select_num_compte():
            cur.execute('DELETE FROM Compte_table WHERE num_compte=?', (int(num_compte),))
            connection.commit()
            print("le compte a été supprimé")
        else:
          print("ce numéro n'existe pas ")



    def debiter(self):
        pass
    def crediter(self):
        pass
    def consulter(self,num_compte):

        cur.execute("SELECT solde  FROM Compte_table where num_compte=(?) ", (num_compte,))
        rows = cur.fetchall()
        if len(rows) == 0:
            r = rows
        else:
            r = list(rows[0])[0]
        return r

    def select_num_compte_client(self,num_carte,code_secret):
        try:
            cur.execute("SELECT num_compte  FROM Carte_table where num_carte=(?) and code_secret=(?) ", (num_carte,code_secret,))
            rows = cur.fetchall()
            if len(rows) == 0:
                r = rows
            else:
                r = list(rows[0])[0]
            return r
        except :
               r=None
               print("nooooooo")
               return r
    def consulter_pour_client(self,num_carte,code_secret):
        try:

            cur.execute("SELECT solde  FROM Compte_table where num_compte=(?) ", (self.select_num_compte_client(num_carte,code_secret),))
            rows = cur.fetchall()
            if len(rows) == 0:
                r = rows
            else:
                r = list(rows[0])[0]
            return r
        except:
          print("okkk")
          r=None
          return r
    def select_num_compte(self):
        cur.execute("SELECT num_compte  FROM Compte_table ")
        rows = cur.fetchall()
        if len(rows)==0:
            r=rows
        else:
            r=list(rows[0])
        return r

    def select_num_carte(self):
        cur.execute("SELECT num_carte  FROM Carte_table ")
        rows = cur.fetchall()
        if len(rows) == 0:
            r = rows
        else:
            r = list(rows[0])
        return r

    def select_etat_carte(self,num_carte):
        cur.execute("SELECT etat_carte  FROM Carte_table where num_carte=(?) ",(num_carte,))
        rows = cur.fetchall()
        if len(rows) == 0:
            r = rows
        else:
            r = list(rows[0])[0]
        return r
    def default_num(self):
        self.r1 = True
        while self.r1==True:

            if self.num_carte_default in self.select_num_carte() :
                self.num_carte_default = self.random.randint(0, 10)
            else:
                self.r1 = False

            if len(self.select_num_carte()) == 10:
                print('toutes les numéros des carte sont utilisé ')
                break
        self.r2 = True
        while self.r2 == True:

            if self.num_compte_default in self.select_num_compte()  :
                self.num_compte_default = random.randint(0, 10)
            else:
                self.r2 = False

            if len(self.select_num_compte()) == 10:
                print('toutes les numéros des comptes sont utilisé ')
                break


    def depart(self):
            print(self.select_etat_carte(2))
            a = True
            while a == True:
                reponse = input("#####################################\n"
                                "pour ajouter un client repondre par 1 \n "
                                "pour ajouter un compte repondre par 2 \n"
                                "pour ajouter un carte repondre par 3 \n"
                                "pour supprimer un comte repondre  4 \n"
                                "pour bloquer carte repondre  5 \n"
                                "pour debloquer carte repondre  6 \n"
                                "pour change code secret de carte  repondre  7 \n"
                                "pour consulter un compte repondre  8 \n"
                                "pour anuuler repondre 0")

                if reponse == "0":
                    a = False
                if reponse == "1":
                    self.default_num()
                    nom = input("entrer le nom de client: ")
                    prenom = input("entrer le prenom de client: ")
                    code_agence = input("entrer le code de agence de client: ")
                    tel = input("entrer le numéro de téléphone de client: ")
                    self.ajouter_client(nom, prenom, code_agence, tel)
                    print("votre client a été cree")
                if reponse == "2":
                    self.default_num()
                    code_client = input("entrer le code client: ")
                    print('le numéro de compte disponible est :',self.num_compte_default)

                    solde = input("entrer le solde client: ")
                    self.ajouter_compte(self.num_compte_default, code_client, solde)
                    print('votre compte a été creer')

                if reponse == "3":

                    num_compte = input("entrer le numéro de compte corespondant à cette carte : ")
                    print('le numéro de carte disponible est :', self.num_carte_default)

                    code_secret = input("entrer le code secret pour  cette carte : ")

                    date_expiration = input("entrer date d'expiration de client: ")
                    etat_carte = input("etat carte : ")
                    self.ajouter_carte(self.num_carte_default, num_compte, code_secret, date_expiration, etat_carte)
                    print('votre carte  a été creer')

                if reponse == "4":
                    num_compte = input("entrer le numéro de compte que vous voullez supprimer : ")
                    self.supprimer_compte(num_compte)

                if reponse == "5":
                    num_compte = input("entrer le numéro de carte que vous voullez bloquer : ")
                    self.bloquer_carte(num_compte)
                if reponse == "6":
                    num_compte = input("entrer le numéro de carte que vous voullez debloquer : ")
                    self.debloquer_carte(num_compte)
                if reponse == "7":
                    num_carte = input("entrer le numéro de carte que vous voullez changé sa code secret  : ")
                    nouvelle_code_secret = input("entrer le nouvelle code secret  : ")
                    self.modifier_code_secret(nouvelle_code_secret,num_carte)
                if reponse == "8":
                    num_compte = input("entrer le numéro de compte  que vous voullez consulter : ")
                    if int(num_compte) in self.select_num_compte():

                        print("le sode de compte ",num_compte," est : ",self.consulter(num_compte))
                    else:
                        print("ce compte ne existe pas ")

if __name__ == '__main__':
   Client(1)



