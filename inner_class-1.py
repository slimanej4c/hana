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

            self.class_compte = Client.Compte()
            self.class_carte = Client.Compte().Carte()
            self.create_table_client()
            self.class_compte.create_table_compte()
            self.class_carte.create_table_carte()

            self.default_num()
            self.depart()

        else:
            pass

    def create_table_client(self):

        cur.execute(
            'CREATE TABLE if NOT EXISTS Client_table (code_client INTEGER PRIMARY KEY AUTOINCREMENT, Nom VARCHAR (25) ,'
            'Prenom VARCHAR(25),code_agence VARCHAR (20),Tel  INT(11), Email VARCHAR(25))')

    def ajouter_client(self,code_client, Nom, Prenom, code_agence, Tel, Email):

        cur.execute('INSERT INTO Client_table (code_client,Nom,Prenom,code_agence,Tel,Email)values(?,?,?,?,?,?)',
                    (code_client,Nom,Prenom,code_agence,Tel,Email))

        connection.commit()
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


    class Compte:
        def __init__(self):
            pass

        def create_table_compte(self):
            cur.execute(
                'CREATE TABLE if NOT EXISTS Compte_table (num_compte VARCHAR (25)  PRIMARY KEY ,code_client INTEGER , solde INT(11), FOREIGN KEY(code_client) REFERENCES Client_table(code_client) ON DELETE CASCADE)')
            connection.commit()

        def select_solde(self, num_compte):
            try:
                cur.execute("SELECT solde  FROM Compte_table where num_compte=(?) ",
                            (num_compte,))
                rows = cur.fetchall()
                if len(rows) == 0:
                    r = rows
                else:
                    r = list(rows[0])[0]
                return r
            except:
                print("okkk")
                r = None
                return r

        def debiter_solde(self, solde, num_compte):
            solde=int(str(self.select_solde(num_compte)))-int(solde)
            cur.execute('UPDATE Compte_table SET solde=(?)  WHERE num_compte =(?)', (solde, num_compte,))

            connection.commit()
            print("le solde de la carte a été changé avec succés")

        def crediter_solde(self, solde, num_compte):
                cur.execute('UPDATE Compte_table SET solde=(?)  where num_compte =(?)', (solde, num_compte,))

                connection.commit()
                print("le solde de la carte a été changé avec succés")


        def ajouter_compte(self, num_compte, code_client, solde):
            cur.execute(
                'INSERT INTO Compte_table (num_compte,code_client,solde) VALUES(?,?,?)',
                (num_compte, code_client, solde))

            connection.commit()

        def supprimer_compte(self, num_compte):

            if int(num_compte) in self.select_num_compte():
                cur.execute('DELETE FROM Compte_table WHERE num_compte=?', (int(num_compte),))
                connection.commit()
                print("le compte a été supprimé")
            else:
                print("ce numéro n'existe pas ")

        def consulter(self, num_compte):

            cur.execute("SELECT solde  FROM Compte_table where num_compte=(?) ", (num_compte,))
            rows = cur.fetchall()
            if len(rows) == 0:
                r = rows
            else:
                r = list(rows[0])[0]
            return r

        def select_num_compte(self):
            cur.execute("SELECT num_compte  FROM Compte_table ")
            rows = cur.fetchall()
            if len(rows) == 0:
                r = rows
            else:
                r=[]
                for i in list(rows):
                    r.append(i[0])
            return r

        class Carte:
            def __init__(self):
                pass

            def create_table_carte(self):

                cur.execute('CREATE TABLE if NOT EXISTS Carte_table (num_carte VARCHAR (25)  PRIMARY KEY,num_compte VARCHAR (25)  ,'
                            'code_secret VARCHAR (25),date_expiration VARCHAR (20),etat_carte VARCHAR (25), FOREIGN KEY(num_compte ) REFERENCES Compte_table (num_compte ) ON DELETE CASCADE)')
                connection.commit()


            def ajouter_carte(self, num_carte,num_compte,code_secret,date_expiration,etat_carte):
                cur.execute(
                    'insert into Carte_table (num_carte,num_compte ,code_secret,date_expiration,etat_carte)values(?,?,?,?,?)',
                    ( num_carte,num_compte,code_secret,date_expiration,etat_carte))

                connection.commit()

            def bloquer_carte (self,num_carte):
                if self.select_etat_carte(num_carte)=="active":
                    cur.execute('UPDATE Carte_table SET etat_carte = "non active" WHERE num_carte = (?);''',(num_carte,))

                    connection.commit()
                    print("la carte a été bloquer avec succés")
                else:
                    print("cette carte a été déja bloqué")

            def debloquer_carte (self,num_carte):
                if self.select_etat_carte(num_carte)=="non active":
                    cur.execute('UPDATE Carte_table SET etat_carte = "active"  where num_carte = (?);''',(num_carte,))

                    connection.commit()
                    print("La carte a été débloquer avec succés")
                else:
                    print("Cette carte a été déja débloqué")

            def modifier_code_secret (self,code_secret,num_carte):
                cur.execute('UPDATE Carte_table SET code_secret = (?)  WHERE num_carte = (?);''', (code_secret,num_carte,))

                connection.commit()
                print("Le code secret de la carte a été changé avec succés")

            def supprimer_carte(self, num_carte):

                if int(num_carte) in self.select_num_carte():
                    cur.execute('DELETE FROM Carte_table WHERE num_carte=?', (int(num_carte),))
                    connection.commit()
                    print("La carte a été supprimée")
                else:
                    print("Cette carte n'existe pas ")


            def select_num_carte(self):
                cur.execute("SELECT num_carte  FROM Carte_table ")
                rows = cur.fetchall()
                if len(rows) == 0:
                    r = rows
                else:
                    r=[]
                    for i in list(rows):
                        r.append(i[0])

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

            if self.num_carte_default in self.class_carte.select_num_carte() :


                self.num_carte_default = "{:04d}".format(random.randint(1, 9999))
            else:
                self.r1 = False

            if len(self.class_carte.select_num_carte()) == 10:
                print('toutes les numéros des carte sont utilisé ')
                break
        self.r2 = True
        while self.r2 == True:

            if self.num_compte_default in self.class_compte.select_num_compte()  :

                self.num_compte_default = "{:04d}".format(random.randint(0, 9999))
            else:
                self.r2 = False

            if len(self.class_compte.select_num_compte()) == 10:
                print('toutes les numéros des comptes sont utilisé ')
                break


    def depart(self):
            print(self.class_carte.select_etat_carte(2))
            a = True
            while a == True:
                reponse = input("#####################################\n"
                                "Pour ajouter un client répondre par 1 \n"
                                "------------------------------------------ \n"
                                "Pour ajouter un compte répondre par 2 \n"
                                "------------------------------------------ \n"
                                 "Pour ajouter une carte répondre par 3 \n"
                                "------------------------------------------ \n"
                                "Pour débiter le montant du compte répondre par 4 \n"
                                "------------------------------------------ \n"
                                "Pour créditer le montant du compte répondre par 5 \n"
                                "------------------------------------------ \n"
                                "Pour consulter un compte répondre par 6 \n"
                                "------------------------------------------ \n"
                                "Pour supprimer un compte repondre par 7 \n"
                                "------------------------------------------ \n"
                                "Pour bloquer une carte répondre par 8 \n"
                                "------------------------------------------ \n"
                                "Pour débloquer une carte répondre par 9 \n"
                                "------------------------------------------ \n"
                                "Pour modifier le code secret de la carte  répondre par 10 \n"
                                "------------------------------------------ \n"
                                "Pour anuuler répondre par 0: \n")

                if reponse == "0":
                    a = False

                if reponse == "1":
                    self.default_num()
                    code_client=input("entrer le code de client: ")
                    Nom = input("entrer le nom du client: ")
                    Prenom = input("entrer le prenom du client: ")
                    code_agence = input("entrer le code d'agence de client: ")
                    Tel = input("entrer le numéro de téléphone de client: ")
                    Email=input("entrer l'adresse email: ")
                    self.ajouter_client(code_client, Nom, Prenom, code_agence, Tel, Email)
                    print("votre client a été ajouter \n")

                if reponse == "2":
                    self.default_num()
                    code_client = input("entrer le code de client: ")
                    print('le numéro de compte disponible est :',self.num_compte_default)

                    solde = input("entrer le solde de client: ")
                    self.class_compte.ajouter_compte(self.num_compte_default, code_client, solde)
                    print('votre compte a été ajouter \n')

                if reponse == "3":

                    num_compte = input("entrer le numéro de compte correspondant à cette carte : ")
                    print('le numéro de carte disponible est :', self.num_carte_default)

                    code_secret = input("entrer le code secret pour  cette carte : ")

                    date_expiration = input("entrer la date d'expiration de client: ")
                    etat_carte = input("entrer l'état de la carte : ")
                    self.class_carte.ajouter_carte(self.num_carte_default, num_compte, code_secret, date_expiration, etat_carte)
                    print('votre carte a été ajouter \n')

                if reponse=="4":
                    solde=input("entrer le montant que vous voulez enlever: ")
                    num_compte=input("entrer le numéro de compte que vous vouler modifier: ")
                    self.class_compte.debiter_solde(solde, num_compte)
                    print("votre solde a été débiter \n")

                if reponse=="5":
                    solde = input("entrer le montant que vous voulez ajouter: ")
                    num_compte = input("entrer le numéro de compte que vous voulez supprimer: ")
                    self.class_compte.crediter_solde(solde, num_compte)
                    print("votre montant a été créditer \n")

                if reponse == "6":
                    num_compte = input("entrer le numéro de compte  que vous voulez consulter: ")

                    if num_compte in self.class_compte.select_num_compte():

                        print("le solde de compte ",num_compte," est : ",self.class_compte.consulter(num_compte))
                    else:
                        print("ce compte n'existe pas ")

                if reponse == "7":
                    num_compte = input("entrer le numéro de compte que vous voulez supprimer: ")
                    self.class_compte.supprimer_compte(num_compte)
                    print("votre compte a été supprimer \n")

                if reponse == "8":
                    num_compte = input("entrer le numéro de carte que vous voulez bloquer: ")
                    self.class_carte.bloquer_carte(num_compte)
                    print("votre carte a été bloquer \n")

                if reponse == "9":
                    num_compte = input("entrer le numéro de carte que vous voulez débloquer: ")
                    self.class_carte.debloquer_carte(num_compte)
                    print("votre compte a été débloquer \n")

                if reponse == "10":
                    num_carte = input("entrer le numéro de carte que vous voulez changer son code secret: ")
                    nouvelle_code_secret = input("entrer le nouvel code secret: ")
                    self.class_carte.modifier_code_secret(nouvelle_code_secret,num_carte)
                    print("votre code secret a été changer avec succée \n")



if __name__ == '__main__':
   Client(1)



