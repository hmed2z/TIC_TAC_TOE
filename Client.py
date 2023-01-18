import socket
import os
import time
from tkinter import *
from tkinter import messagebox

# meme chose que dans le fichier Server.py
PORT = 8888
SERVER = 'localhost' #'10.3.141.1'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

# verifie que le coup soit bien dans la bonne range
def correctInput(i):
    return i == 0 or i == 1 or i == 2


# Code du jeu
class Morpion:
    #label = label(fenetre, text="TicTacToe")
    #label.pack()

    #def TicTacToeGUI():
        #global t
        #t = Tk()
        #t.title("TIC TAC TOE")
        #t.configure(bg="white")
        ## Making the background of the window as white#Displaying the player
        #l1 = Label(t, text="PLAYER: 1(X)", height=3, font=("COMIC SANS MS", 10, "bold"), bg="white")
        #l1.grid(row=0, column=0)  # Quit button
        #exitButton = Button(t, text="Quit", command=Quit, font=("COMIC SANS MS", 10, "bold"))
        #exitButton.grid(row=0, column=2)  # Grid buttons
        #b1 = Button(t, text="", height=4, width=8, bg="black", activebackground="white", fg="white",
        #            font="Times 15 bold", command=lambda: changeVal(b1, 0, 0))
        #b2 = Button(t, text="", height=4, width=8, bg="black", activebackground="white", fg="white",
        #            font="Times 15 bold", command=lambda: changeVal(b2, 0, 1))
        #b3 = Button(t, text="", height=4, width=8, bg="black", activebackground="white", fg="white",
        #            font="Times 15 bold", command=lambda: changeVal(b3, 0, 2))
        #b4 = Button(t, text="", height=4, width=8, bg="black", activebackground="white", fg="white",
        #            font="Times 15 bold", command=lambda: changeVal(b4, 1, 0))
        #b5 = Button(t, text="", height=4, width=8, bg="black", activebackground="white", fg="white",
        #            font="Times 15 bold", command=lambda: changeVal(b5, 1, 1))
        #b6 = Button(t, text="", height=4, width=8, bg="black", activebackground="white", fg="white",
        #            font="Times 15 bold", command=lambda: changeVal(b6, 1, 2))
        #b7 = Button(t, text="", height=4, width=8, bg="black", activebackground="white", fg="white",
        #            font="Times 15 bold", command=lambda: changeVal(b7, 2, 0))
        #b8 = Button(t, text="", height=4, width=8, bg="black", activebackground="white", fg="white",
        #            font="Times 15 bold", command=lambda: changeVal(b8, 2, 1))
        #b9 = Button(t, text="", height=4, width=8, bg="black", activebackground="white", fg="white",
        #            font="Times 15 bold", command=lambda: changeVal(b9, 2, 2))
        #b1.grid(row=2, column=0)

    #b2.grid(row=2, column=1)
    #b3.grid(row=2, column=2)
    #b4.grid(row=3, column=0)
    #b5.grid(row=3, column=1)
    #b6.grid(row=3, column=2)
    #b7.grid(row=4, column=0)
    #b8.grid(row=4, column=1)
    #b9.grid(row=4, column=2)

    def __init__(self):
        self.board = []
        self.player = None
        self.currentPlayer = None

    def initializeBoard(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append("-")
            self.board.append(row)

    def printBoard(self):
        print(f' {self.board[0][0]} | {self.board[0][1]} | {self.board[0][2]} \n+--+---+--+')
        print(f' {self.board[1][0]} | {self.board[1][1]} | {self.board[1][2]} \n+--+---+--+')
        print(f' {self.board[2][0]} | {self.board[2][1]} | {self.board[2][2]} \n')

    # renvoie True si le coup est valide
    def isValidMove(self, row, col):
        return correctInput(row) and correctInput(col) and self.board[row][col] == "-"

    # Joue le coup
    def play(self, row, col):
        self.board[row][col] = self.currentPlayer

    # set le role du player
    def setPlayer(self, player):
        self.player = player

    # change le joueur dont c'est le tour
    def changeCurrentPlayer(self):
        self.currentPlayer = opposite(self.currentPlayer)

    # set le joueur dont s'est le tour -> pour le premier tour
    def setCurrentPlayer(self, currentPlayer):
        self.currentPlayer = currentPlayer

# renvoie le role du joueur adverse
def opposite(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'

# print un affichage en boite avec le message au centre
def box(message):
    leng = len(message) + 3
    boxx = "+"
    for i in range(leng - 1):
        boxx = boxx + "-"
    boxx = boxx + "+"
    print(f'{boxx}\n| {message} |\n{boxx}\n')

# debut du client
def start():
    # creation du jeu
    morpion = Morpion()
    # initialise le board
    morpion.initializeBoard()

    #fenetre = Tk()
    #fenetre.title("TicTacToe By Ahmed, Dalia and Dyhia")
    #fenetre.mainloop()

    # temoin de connection
    connected = True
    while connected:
        # message recu par le client
        message = client.recv(1024).decode(FORMAT)

        # la suite du code est composee de verification des messages
        # deconnecte le client si le server est complet
        if message == '[SERVER FULL]':
            print(message + '\n[DECONNECTION]')
            connected = False
        # interpretation du message donnant le role du joueur
        elif len(message) == 1:
            morpion.setPlayer(message)
            text = f'You are the player {morpion.player}'
            box(text)
        # lorsqu'il s'agit du tour du joueur
        elif message == f'Player {morpion.player} turn':
            # defini le joueur comme le joueur dont c'est le tour
            morpion.setCurrentPlayer(morpion.player)
            print(message)
            # demande au joueur de rentrer une ligne et une colone indicant la case dans la grille
            row, col = list(map(int, input("Enter row and column numbers to fix spot: ").split()))
            # si le coup est valide on l'envoie au server
            if morpion.isValidMove(row, col):
                client.send(f'{row} {col}'.encode(FORMAT))
            else:
                # tant que le coup n'est pas valide, on demande au joueur de re-donner un autre couple
                while not morpion.isValidMove(row, col):
                    row, col = list(map(int, input("Wrong spot, try again: ").split()))
                client.send(f'{row} {col}'.encode(FORMAT))
        # s'il s'agit d'un message de victoire ou d'egalite, on affiche le message dans une box et
        # on termine la session
        elif message.__contains__('wins the game') or message.__contains__('Match Draw'):
            box(message)
            print('[END OF THE GAME]\nClosing the session...')
            time.sleep(2)
            # termine la connection en changeant la valeur du temoin
            connected = False
        # message disant qu'il s'agit du tour de l'adversaire
        elif message == f'Player {opposite(morpion.player)} turn':
            morpion.setCurrentPlayer(opposite(morpion.player))
            print(message)
        # message contenant un coup a jouer
        elif len(message) == 3:
            # reccupere les valeurs de la ligne et de la colone dans 2 variables
            split = message.split()
            row = int(split[0])
            col = int(split[1])
            # joue le jeu dans la grille
            morpion.play(row, col)
            # affiche le board
            morpion.printBoard()
            # indique la fin du tour en changeant le joueur dont s'est le tour
            morpion.changeCurrentPlayer()
# debut du client
start()
# fermeture du scrip
os._exit(0)
