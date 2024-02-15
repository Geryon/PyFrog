import os, sys
import pygame
from pygame.locals import *
import config

##
## All collision detection functionality is here
##
class Collision( ):
    def __init__( self ):
        self.Global = config.GlobalDefs( )
    
    ## 
    ## Set down some boundries for our frog.
    ##
    def checkFrogBorder( self, frog ):
        ( X, Y ) = frog.pos
        ( x, y, w, h ) = frog.src
        if ( Y - 5 ) >= self.getRowPixel( 0 ):
            frog.pos = frog.oldPos
            frog.currentRow = 0
            return 0
        if X <= self.Global.Left_side or X + w >= self.Global.Right_side:
            if frog.currentRow == 0 or frog.currentRow == 6:
                frog.pos = frog.oldPos
            else:
                frog.alive = False
        return 1
    
    ##
    ## This calculates the pixel top of the requested row
    ##
    def getRowPixel( self, row ):
       return self.Global.Row_base - ( row * self.Global.Hop_distance )

    ##
    ## Check if our frog is colliding with anything
    ##
    def collideFrog( self, frog, x, y, h, w ):
        h += 1;
        w += 1;

#        if frog.pos[0] <= ( x + w ):           return 0
#        elif x <= frog.pos[0] + self.Global.Frame: return 0

        if frog.pos[1] >= ( y + h ):            return 0
        if frog.pos[0] >= ( x + w ):            return 0
        if y >= ( frog.pos[1] + self.Global.Frame ):    return 0
        if x >= ( frog.pos[0] + self.Global.Frame ):    return 0
        
        return 1

    ##
    ## This does collision detection based on the row our frog 
    ## is currently residing in.  Only one row is done to reduce overhead.
    ##
    def collisionRow( self, frog, game ):
        if frog.currentRow <= 0: return 0

        if frog.currentRow == 6: 
            ## If I add the python to the path, that'll go here.
            frog.riding = False
        if frog.currentRow < 6:
            ## Vehicles
            frog.riding = False
            for n in range( self.Global.Max_vehicles ):
                if game.vehicle[n].row != frog.currentRow: continue
                if game.level >= game.vehicle[n].level:
                    length = self.Global.Frame
                    if game.vehicle[n].row == 5: length = length * 2

                    if self.collideFrog( frog, \
                        game.vehicle[n].placement[0], \
                        game.vehicle[n].placement[1], \
                        self.Global.Frame, length ): return 1
            return 0
        if frog.currentRow == 7 or frog.currentRow == 10:
            ## Turtles
            for n in range( self.Global.Max_turtles ):
                if self.collideFrog( frog, \
                        game.turtle[n].pos[0], \
                        game.turtle[n].pos[1], \
                        self.Global.Frame, \
                        self.Global.Frame * game.turtle[n].count ):
                    frog.riding     = self.Global.Left
                    frog.ridingType = self.Global.Turtle
                    frog.ridingIdx  = n
                    return 0
            frog.riding = False
            return 1
        if frog.currentRow == 8 or frog.currentRow == 9 or frog.currentRow == 11:
            ## Logs
            for n in range( self.Global.Max_logs ):
                if self.collideFrog( frog, \
                        game.log[n].placement[0], \
                        game.log[n].placement[1], \
                        self.Global.Frame, \
                        self.Global.Frame * game.log[n].size ):
                    frog.riding    = self.Global.Right
                    frog.ridingType = self.Global.Log
                    frog.ridingIdx  = n
                    return 0
            frog.riding = False
            return 1
        if frog.currentRow == 12:
            ## Check the goals
            frog.riding = False

        return 0
