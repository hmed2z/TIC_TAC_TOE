import socket
import os
import random
import threading
import time
from tkinter import *
from tkinter import messagebox

# Port > 1024
PORT = 8888
# IP ou on se connecte
SERVER = 'localhost' #"10.3.141.1"
ADDRESS = (SERVER, PORT)
# Format d'encodage des messages
FORMAT = 'utf-8'
# Cree le socket pour le server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

# Dictionnaire ou on va stocker les connections
# et les roles des joueurs
clients = dict()

# Envoie le message à tous les clients
def sendAll(message):
    for client in clients:
        client.send(message)


# Code du Morpion
class Morpion:

    def __init__(self):
        self.board = []
        self.currentPlayer = None
        self.startGame = False
        self.changement = False

    # rempli le board de case vide "-"
    def initializeBoard(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append("-")
            self.board.append(row)

    # Renvoie un role aleatoire
    def randRole(self):
        if random.randint(0, 1) == 0:
            return "X"
        else:
            return "O"


    # Affiche le board
    def printBoard(self):
        print(f' {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]} \n+--+---+--+')
        print(f' {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]} \n+--+---+--+')
        print(f' {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]} \n')

    # a l'aide d'un random, defini qui
    # commence entre X et O
    def whosStarting(self):
        who = random.randint(0, 1)
        if who == 1:
            self.currentPlayer = "X"
        else:
            self.currentPlayer = "O"

    # return True si le coup est
    # Possible
    def isValidMove(self, row, col):
        if self.board[row][col] == "-":
            return True
        return False

    # joue le coup dans le board
    def play(self, row, col):
        self.board[row][col] = self.currentPlayer

    # Change le currentPlayer du morpion
    # et set le changement a True
    def changecurrentPlayer(self):
        if self.currentPlayer == "X":
            self.currentPlayer = "O"
        else:
            self.currentPlayer = "X"
        self.changement = True

    # regarde si le board est gagnant en regardant toutes les possibilites
    # renvoie True si vrai
    def isWinning(self):
        # rows
        row1 = self.board[0][0] == self.board[0][1] and self.board[0][1] == self.board[0][2] and self.board[0][0] == self.currentPlayer
        row2 = self.board[1][0] == self.board[1][1] and self.board[1][1] == self.board[1][2] and self.board[1][0] == self.currentPlayer
        row3 = self.board[2][0] == self.board[2][1] and self.board[2][1] == self.board[2][2] and self.board[2][0] == self.currentPlayer
        rows = row1 or row2 or row3

        # columns
        col1 = self.board[0][0] == self.board[1][0] and self.board[1][0] == self.board[2][0] and self.board[0][0] == self.currentPlayer
        col2 = self.board[0][1] == self.board[1][1] and self.board[1][1] == self.board[2][1] and self.board[0][1] == self.currentPlayer
        col3 = self.board[0][2] == self.board[1][2] and self.board[1][2] == self.board[2][2] and self.board[0][2] == self.currentPlayer
        cols = col1 or col2 or col3

        # diagonals
        diag1 = self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] == self.currentPlayer
        diag2 = self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2] and self.board[2][0] == self.currentPlayer
        diags = diag1 or diag2

        return rows or cols or diags

    # Renvoie True si le board est complet mais non gagnant
    def isDraw(self):
        for i in self.board:
            for j in i:
                if j == "-":
                    return False
        return True

# Code du server
# ecoute des messages et agit en fonctions de ces derniers
def start(connection, address):
    # attend que les deux joueurs soient presents
    while not morpion.startGame:
        if len(clients) == 2:
            morpion.startGame = True

    # ecoute des messages
    while morpion.startGame:
        # afin de faire attendre le joueur qui ne joue pas
        morpion.changement = False
        # si la connection appartient au joueur dont s'est le tour
        if clients[connection] == morpion.currentPlayer:
            # attend pour laisser le temps aux informations
            # d'aller aux joueurs -> meme chose pour tous les
            # time.sleep, permet d'eviter les erreurs
            time.sleep(1)
            print('Current player : ' + morpion.currentPlayer)
            # envoie a qui de jouer a tous les joueurs
            sendAll(f'Player {morpion.currentPlayer} turn'.encode(FORMAT))
            # message contenant le coup joue par le joueur
            message = connection.recv(1024).decode(FORMAT)
            # coup de la forme "int int"
            # split le message au niveau de l'espace pour reccuperer les deux valeurs
            # et les stock dans des variables
            split = message.split()
            row = int(split[0])
            col = int(split[1])
            # joue le coup du joueur
            morpion.play(row, col)
            time.sleep(1)
            # envoie a tous les joueurs le coup a jouer
            sendAll(f'{row} {col}'.encode(FORMAT))

            # envoie un message a tous les joueurs en cas de victoire apres le coup joue
            if morpion.isWinning():
                sendAll(f"Player {morpion.currentPlayer} wins the game".encode(FORMAT))
                time.sleep(1)
                # termine le script
                os._exit(0)
            # envoie un message a tous les joueurs si match nul
            if morpion.isDraw():
                sendAll("Match Draw".encode(FORMAT))
                time.sleep(1)
                # termine le script
                os._exit(0)
            morpion.changecurrentPlayer()
        else:
            # gere l'attente du second dont ce n'est pas le tour
            while not morpion.changement:
                time.sleep(1)

        time.sleep(1)

# Fonction initialisant le server et attribuant le role de chaque joueur
def begin(morpion):
    print(f'Démarrage du serveur sur [{SERVER}]')
    # Le server "ecoute" les nouvelles entrees
    server.listen()
    # Remplie le board de cases vides
    morpion.initializeBoard()
    # Defini qui commence
    morpion.whosStarting()
    while True:
        # Reccupere le socket de connection et l'adresse du nouveau client
        connection, address = server.accept()
        # creation d'un role pour l'attribution aleatoire
        role = None
        # si 0 client dans le dictionnaire
        if len(clients) == 0:
            # premièr role attribue de facon aleatoire
            role = morpion.randRole()
            # envoie du role au client
            connection.send(f'{role}'.encode(FORMAT))
            # print dans le chat du server le role, l'adresse et indique qu'il est connecte
            print(f'[{address}] {role} - Connected')
            # associe le role et la connection dans le dicitonnaire
            clients[connection] = role
            # creation du thread pour gerer le client
            thread = threading.Thread(target=start, args=(connection, address))
            thread.start()
        # si il y a deja un premier client
        elif len(clients) == 1:
            # meme chose que pour le code au dessus
            # on attribut le role en fonction
            # du role du premier connecte
            if role == 'X':
                connection.send('O'.encode(FORMAT))
                print(f'[{address}] O - Connected')
                clients[connection] = "O"
            else:
                connection.send('X'.encode(FORMAT))
                print(f'[{address}] X - Connected')
                clients[connection] = "X"
            thread = threading.Thread(target=start, args=(connection, address))
            thread.start()
        # si deux clients sont deja connectes, on rejette les autres
        else:
            connection.send('[SERVER FULL]'.encode(FORMAT))
            connection.close()

# creation du jeu
morpion = Morpion()
# debut du jeu
begin(morpion)
# termine le script quand le jeu est fini
os._exit(0)
