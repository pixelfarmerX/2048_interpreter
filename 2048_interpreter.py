# -*- coding: utf-8 -*-
"""CC_Assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s1l7QDJS4edIRkctcpib8dLyov7rzpPE
"""

!pip install sly
#!pip install termcolor

import random
from termcolor import colored, cprint
import sys

#board = arr = [[0 for i in range(4)] for j in range(4)]

#for item in self.names:
#    if self.names[item] == [r,c]:
#        self.names[item] = [r,c-1]

printwoc = lambda x: cprint(x, 'blue')
printr = lambda x: cprint(x, 'red')
printc = lambda x: cprint(x, 'cyan')
printm = lambda x: cprint(x, 'magenta')
printy = lambda x: cprint(x, 'yellow')

def PrintBoard(board):
    print(" ----------------- ")
    print(" | ", end = "")
    print(board[0][0], end = " | ")
    print(board[0][1], end = " | ")
    print(board[0][2], end = " | ")
    print(board[0][3], end ="")
    print(" | ")
    print(" ----------------- ")
    print(" | ", end = "")
    print(board[1][0], end = " | ")
    print(board[1][1], end = " | ")
    print(board[1][2], end = " | ")
    print(board[1][3], end ="")
    print(" | ")
    print(" ----------------- ")
    print(" | ", end = "")
    print(board[2][0], end = " | ")
    print(board[2][1], end = " | ")
    print(board[2][2], end = " | ")
    print(board[2][3], end ="")
    print(" | ")
    print(" ----------------- ")
    print(" | ", end = "")
    print(board[3][0], end = " | ")
    print(board[3][1], end = " | ")
    print(board[3][2], end = " | ")
    print(board[3][3], end ="")
    print(" | ")
    print(" ----------------- ")

from sly import Lexer
#from main import *

class GameLexer(Lexer):
    tokens = {ADD, SUBTRACT, MULTIPLY, DIVIDE, LEFT, RIGHT, UP, DOWN, ASSIGN, TO, VAR, IS, VALUE, IN, COMMA, FULLSTOP, VARNAME, NUMBER}
    ignore = ' \t'

    # keywords
    ADD = r'ADD'
    SUBTRACT = r'SUBTRACT'
    MULTIPLY = r'MULTIPLY'
    DIVIDE = r'DIVIDE'
    LEFT = r'LEFT'
    RIGHT = r'RIGHT'
    UP = r'UP'
    DOWN = r'DOWN'
    ASSIGN = r'ASSIGN'
    TO = r'TO'
    VAR = r'VAR'
    IS = r'IS'
    VALUE = r'VALUE'
    IN = r'IN'

    # other tokens
    VARNAME = r'[a-zA-Z_][a-zA-Z0-9_]+'
    NUMBER = r'\d+'
    COMMA = r'\,'
    FULLSTOP = r'\.'

    # Ignored pattern

    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

from sly import Parser
#from main import *

class GameParser(Parser):
    tokens = GameLexer.tokens

    def __init__(self):
        self.names = {}
        self.vars = []

    # TILE VARIABLE QUERY

    @_('VALUE IN VARNAME FULLSTOP')
    def statement(self, p):
        #try:
        if p.VARNAME not in self.vars:
            printc("2048 > Sorry, no such tile exists.")
            return 0
        else:
            print("2048 >", end = " ")
            print(p.VARNAME, end = " ") 
            print("is the tile at position :", end = " ")
            print(self.names[p.VARNAME], end = " ")
            print("with Value :", end =" ")
            print(board[self.names[p.VARNAME][0]][self.names[p.VARNAME][1]])
        #except LookupError:
            #print(f'Undefined name {p.VARNAME!r}')
            #print("2048 > Sorry, no such tile exists.")
            #return 0

    @_('VALUE IN VARNAME')
    def statement(self, p):
          printy("2048 > You need to end a command with a full-stop.")
          return 0

    # SYNTAX ERROR CASES

    @_('VARNAME')
    def statement(self, p):
        printr("2048 > Syntax Error.")
        return 0

    @_('NUMBER')
    def statement(self, p):
        printm("2048 > Sorry, I don’t understand that.")
        return 0

    # NAMING

    @_('VAR VARNAME IS NUMBER COMMA NUMBER FULLSTOP')
    def statement(self, p):
        if p.VARNAME in GameLexer.tokens:
          printc("2048 > No, a keyword cannot be a variable name.")
          return -1
        elif p.VARNAME in self.vars:
          printc("2048 > Variable name already assigned.")
          return -1
        elif (int(p.NUMBER0)>3 or int(p.NUMBER0)<0 or int(p.NUMBER1)>3 or int(p.NUMBER1)<0):
          printm("2048 > There is no tile like that. The tile co-ordinates must be in the range 0,1,2,3.")
          return 0
        else:
          printwoc("2048 > Thanks, naming done.")
          self.names[p.VARNAME] = [int(p.NUMBER0), int(p.NUMBER1)]
          self.vars.append(p.VARNAME)
          return 0

    @_('VAR VARNAME IS NUMBER COMMA NUMBER')
    def statement(self, p):
          printy("2048 > You need to end a command with a full-stop.")
          return 0

    # ASSIGNMENT (WITHOUT NESTED COMMANDS)

    @_('ASSIGN NUMBER TO NUMBER COMMA NUMBER FULLSTOP')
    def statement(self, p):
        if (int(p.NUMBER2)>3 or int(p.NUMBER2)<0 or int(p.NUMBER1)>3 or int(p.NUMBER1)<0):
          printm("2048 > There is no tile like that. The tile co-ordinates must be in the range 0,1,2,3.")
          return 0
        else:
          board[int(p.NUMBER1)][int(p.NUMBER2)] = int(p.NUMBER0)
          printwoc("2048 > Thanks, assignment done.")
          printwoc("2048 > The current state is:")
          #for row in board:
          #   print(row)
          PrintBoard(board)
          return 0

    @_('ASSIGN NUMBER TO NUMBER COMMA NUMBER')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    # ASSIGNMENT (WITH NESTED COMMANDS) (1)

    @_('ASSIGN NUMBER TO VARNAME FULLSTOP')
    def statement(self, p):
        if p.VARNAME not in self.vars:
          printc("2048 > There is no such Tile with this name.")
          return 0
        else:
          board[self.names[p.VARNAME][0]][self.names[p.VARNAME][1]] = int(p.NUMBER)
          printwoc("2048 > Thanks, assignment done.")
          printwoc("2048 > The current state is:")
          #for row in board:
          #   print(row)
          PrintBoard(board)
          return 0

    @_('ASSIGN NUMBER TO VARNAME')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    # QUERY (WITHOUT NESTED COMMANDS)

    @_('VALUE IN NUMBER COMMA NUMBER FULLSTOP')
    def statement(self, p):
        if (int(p.NUMBER0)>3 or int(p.NUMBER0)<0 or int(p.NUMBER1)>3 or int(p.NUMBER1)<0):
          printm("2048 > There is no tile like that. The tile co-ordinates must be in the range 0,1,2,3.")
          return 0
        else:
          print("2048 > ", end = "")
          print(board[int(p.NUMBER0)][int(p.NUMBER1)])
          return 0

    @_('VALUE IN NUMBER COMMA NUMBER')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    # ASSIGNMENT (WITH NESTED COMMANDS) (2)

    @_('ASSIGN VALUE IN NUMBER COMMA NUMBER TO NUMBER COMMA NUMBER FULLSTOP')
    def statement(self, p):
        if (int(p.NUMBER2)>3 or int(p.NUMBER2)<0 or int(p.NUMBER1)>3 or int(p.NUMBER1)<0):
          printm("2048 > There is no tile like that. The tile co-ordinates must be in the range 0,1,2,3.")
          return 0
        else:
          board[int(p.NUMBER2)][int(p.NUMBER3)] = board[int(p.NUMBER0)][int(p.NUMBER1)]
          printwoc("2048 > Thanks, assignment done.")
          printwoc("2048 > The current state is:")
          #for row in board:
          #   print(row)
          PrintBoard(board)
          return 0

    @_('ASSIGN VALUE IN NUMBER COMMA NUMBER FULLSTOP TO NUMBER COMMA NUMBER FULLSTOP')
    def statement(self, p):
        printy("2048 > You do not need to put a full-stop in between.")
        return 0

    @_('ASSIGN VALUE IN NUMBER COMMA NUMBER TO NUMBER COMMA NUMBER')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    # MOVES

    @_('ADD LEFT FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(1,4):
                if (board[r][c-1] == board[r][c]) and (board[r][c] != 0):
                      board[r][c-1] = 2*board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c-1]
                      c = c+1
                elif (board[r][c-1] == 0) and (board[r][c] != 0):
                      board[r][c-1] = board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c-1]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, left move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)  

    @_('ADD LEFT')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('ADD RIGHT FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(3):
                if (board[r][c+1] == board[r][c]) and (board[r][c] is not 0):
                      board[r][c+1] = 2*board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c+1]
                      c = c+1
                elif (board[r][c+1] == 0) and (board[r][c] is not 0):
                      board[r][c+1] = board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c+1]
                      c = c+1
        
        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, right move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('ADD RIGHT')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('ADD UP FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(1,4):
                if (board[c-1][r] == board[c][r]) and (board[c][r] is not 0):
                      board[c-1][r] = 2*board[c][r]
                      board[c][r] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c-1,r]
                      c = c+1
                elif (board[c-1][r] == 0) and (board[c][r] is not 0):
                      board[c-1][r] = board[c][r]
                      board[c][r] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c-1,r]
                      c = c+1

        count = 0
        while 1:
          ri = random.randint(0,3)
          ci = random.randint(0,3)
          if board[ri][ci] == 0:
              idx = random.randint(1,8)
              board[ri][ci] = idx
              break
          elif count>=15:
              break
          else:
              count=count+1

        printwoc("2048 > Thanks, up move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('ADD UP')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('ADD DOWN FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(3):
                if (board[c+1][r] == board[c][r]) and (board[c][r] is not 0):
                      board[c+1][r] = 2*board[c][r]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c+1,r]
                      c = c+1
                elif (board[r][c+1] == 0) and (board[r][c] is not 0):
                      board[c+1][r] = board[c][r]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c+1,r]
                      c = c+1

        count = 0
        while 1:
          ri = random.randint(0,3)
          ci = random.randint(0,3)
          if board[ri][ci] == 0:
              idx = random.randint(1,8)
              board[ri][ci] = idx
              break
          elif count>=15:
              break
          else:
              count=count+1

        printwoc("2048 > Thanks, down move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('ADD DOWN')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('SUBTRACT LEFT FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(1,4):
                if (board[r][c-1] == board[r][c]) and (board[r][c] != 0):
                      board[r][c-1] = 0
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c-1]
                      c = c+1
                elif (board[r][c-1] == 0) and (board[r][c] != 0):
                      board[r][c-1] = board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c-1]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, left move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('SUBTRACT LEFT')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('SUBTRACT RIGHT FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(3):
                if (board[r][c+1] == board[r][c]) and (board[r][c] != 0):
                      board[r][c+1] = 0
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c+1]
                      c = c+1
                elif (board[r][c+1] == 0) and (board[r][c] is not 0):
                      board[r][c+1] = board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c+1]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, right move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('SUBTRACT RIGHT')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('SUBTRACT UP FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(1,4):
                if (board[c-1][r] == board[c][r]) and (board[c][r] is not 0):
                      board[c-1][r] = 0
                      board[c][r] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c-1,r]
                      c = c+1
                elif (board[c-1][r] == 0) and (board[c][r] is not 0):
                      board[c-1][r] = board[c][r]
                      board[c][r] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c-1,r]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, up move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('SUBTRACT UP')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('SUBTRACT DOWN FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(3):
                if (board[c+1][r] == board[c][r]) and (board[c][r] is not 0):
                      board[c+1][r] = 0
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c+1,r]
                      c = c+1
                elif (board[r][c+1] == 0) and (board[r][c] is not 0):
                      board[c+1][r] = board[c][r]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c+1,r]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break  
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, down move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)                

    @_('SUBTRACT DOWN')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('MULTIPLY LEFT FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(1,4):
                if (board[r][c-1] == board[r][c]) and (board[r][c] != 0):
                      board[r][c-1] = board[r][c]*board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c-1]
                      c = c+1
                elif (board[r][c-1] == 0) and (board[r][c] != 0):
                      board[r][c-1] = board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c-1]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, left move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('MULTIPLY LEFT')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('MULTIPLY RIGHT FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(3):
                if (board[r][c+1] == board[r][c]) and (board[r][c] != 0):
                      board[r][c+1] = board[r][c]*board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c+1]
                      c = c+1
                elif (board[r][c+1] == 0) and (board[r][c] is not 0):
                      board[r][c+1] = board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c+1]
                      c = c+1
        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, right move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)
              

    @_('MULTIPLY RIGHT')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('MULTIPLY UP FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(1,4):
                if (board[c-1][r] == board[c][r]) and (board[c][r] is not 0):
                      board[c-1][r] = board[c][r]*board[c][r]
                      board[c][r] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c-1,r]
                      c = c+1
                elif (board[c-1][r] == 0) and (board[c][r] is not 0):
                      board[c-1][r] = board[c][r]
                      board[c][r] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c-1,r]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, up move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('MULTIPLY UP')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('MULTIPLY DOWN FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(3):
                if (board[c+1][r] == board[c][r]) and (board[c][r] is not 0):
                      board[c+1][r] = board[c][r]*board[c][r]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c+1,r]
                      c = c+1
                elif (board[r][c+1] == 0) and (board[r][c] is not 0):
                      board[c+1][r] = board[c][r]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c+1,r]
                      c = c+1
        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, down move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)
    

    @_('MULTIPLY DOWN')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('DIVIDE LEFT FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(1,4):
                if (board[r][c-1] == board[r][c]) and (board[r][c] != 0):
                      board[r][c-1] = 1
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c-1]
                      c = c+1
                elif (board[r][c-1] == 0) and (board[r][c] != 0):
                      board[r][c-1] = board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c-1]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, left move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)    

    @_('DIVIDE LEFT')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('DIVIDE RIGHT FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(3):
                if (board[r][c+1] == board[r][c]) and (board[r][c] is not 0):
                      board[r][c+1] = 1
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c+1]
                      c = c+1
                elif (board[r][c+1] == 0) and (board[r][c] is not 0):
                      board[r][c+1] = board[r][c]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [r,c]:
                                  self.names[item] = [r,c+1]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1

        printwoc("2048 > Thanks, right move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('DIVIDE RIGHT')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('DIVIDE UP FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(1,4):
                if (board[c-1][r] == board[c][r]) and (board[c][r] is not 0):
                      board[c-1][r] = 1
                      board[c][r] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c-1,r]
                      c = c+1
                elif (board[c-1][r] == 0) and (board[c][r] is not 0):
                      board[c-1][r] = board[c][r]
                      board[c][r] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c-1,r]
                      c = c+1

        count = 0
        while 1:
          ri = random.randint(0,3)
          ci = random.randint(0,3)
          if board[ri][ci] == 0:
              idx = random.randint(1,8)
              board[ri][ci] = idx
              break
          elif count>=15:
              break
          else:
              count=count+1

        printwoc("2048 > Thanks, up move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)

    @_('DIVIDE UP')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

    @_('DIVIDE DOWN FULLSTOP')
    def statement(self, p):
        for r in range(4):
            for c in range(3):
                if (board[c+1][r] == board[c][r]) and (board[c][r] is not 0):
                      board[c+1][r] = 1
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c+1,r]
                      c = c+1
                elif (board[r][c+1] == 0) and (board[r][c] is not 0):
                      board[c+1][r] = board[c][r]
                      board[r][c] = 0
                      for item in self.names:
                          if self.names[item] == [c,r]:
                                  self.names[item] = [c+1,r]
                      c = c+1

        count = 0
        while 1:
              ri = random.randint(0,3)
              ci = random.randint(0,3)
              if board[ri][ci] == 0:
                  idx = random.randint(1,8)
                  board[ri][ci] = idx
                  break
              elif count>=15:
                  break
              else:
                  count=count+1     

        printwoc("2048 > Thanks, down move done, random tile added.")
        printwoc("2048 > The current state is:")
        #for row in board:
        #      print(row)
        PrintBoard(board)         

    @_('DIVIDE DOWN')
    def statement(self, p):
        printy("2048 > You need to end a command with a full-stop.")
        return 0

board = arr = [[0 for i in range(4)] for j in range(4)]

if __name__ == '__main__':
      lexer = GameLexer()
      parser = GameParser()
      idx = random.randint(1,8)
      r = random.randint(0,3)
      c = random.randint(0,3)
      board[r][c] = idx
      printc("2048 > Hi, I am the 2048-game Engine.")
      printc("2048 > The start state is:")
      #for row in board:
      #      print(row)
      PrintBoard(board)
      while True:
          try:
              #for row in board:
                    #print(row)
              printc("2048 > Please Type a Command")
              text = input('---- > ')
              if text == "EXIT PROGRAM" or text == "EXIT PROGRAM." or text == "Exit Program" or text == "EXIT" or text == "Exit" or text == "exit":
                    break
          except EOFError:
              break
          if text:
              #print("2048 > ", end ="")
              parser.parse(lexer.tokenize(text))
              print(*board, file = sys.stderr)       

      print("2048 > Thank You. See You Again!")