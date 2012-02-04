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
	## This calculates the pixel top of the requested row
	##
	def getRowPixel( self, row ):
		return self.Global.Row_base - ( row * self.Global.Hop_distance )		

class Log( pygame.sprite.Sprite ):
	def __init__( self ):
		pygame.sprite.Sprite.__init__( self )
		self.size 		= 0
		self.placement 		= [ 0, 0 ]
		self.oPlacement 	= [ 0, 0 ]
		self.row		= 0
		self.speed		= 0
		self.pink		= 0
		self.gator		= 0
		
	def update( self ):
		self.placement += self.speed

class Vehicles( pygame.sprite.Sprite ):
	def __init__( self, vehicle ):
		self.Global 		= config.GlobalDefs( )
		self.Collision		= Collision( )
		row, X, speed, level    = self.fetchVehicleData( vehicle )
		self.placement 		= [ 0, 0 ]
		self.placement[0]       = self.Global.Left_side + X
                self.placement[1]       = self.Collision.getRowPixel( row )
		self.oPlacement		= self.placement
		self.direction		= self.Global.Left if row % 2 > 0 else self.Global.Right 
		self.row		= row
		self.speed		= speed
		self.level		= level
		self.src		= [ 0, 0, 0, 0 ]
		self.src[0]		= self.Global.Frame * ( 4 + row )
		self.src[1]		= self.Global.Frame * 2
		self.src[2]		= self.Global.Frame * 2 if row == 5 else self.Global.Frame
		self.src[3]		= self.Global.Frame
		self.image		= 0

	def update( self ):
		if self.direction == self.Global.Right:
			if self.placement[0] > self.Global.Right_side + 5:
				self.placement[0] = self.Global.Left_side - self.src[2] - 5
			self.placement[0] += self.speed
		else:
			if self.placement[0] < self.Global.Left_side - 5:
				self.placement[0] = self.Global.Right_side - self.src[2] + 5
			self.placement[0] -= self.speed

	def draw( self, screen, gfx, game ):
		if game.level >= self.level: screen.blit( gfx.frogger_image, self.placement, self.src )
			

	def fetchVehicleData( self, vehicle ):
		Vehicles = [
				   ## [ ROW, X_CORD, SPEED, LEVEL ]
				   ## Row 1 -- yellow car
				   [ 1, 0,   1, 1 ],
				   [ 1, 100, 1, 3 ],
				   [ 1, 200, 1, 1 ],
				   [ 1, 300, 1, 1 ],
				   ### Row 2 -- tractor
				   [ 2, 0,   3, 1 ],
				   [ 2, 100, 3, 2 ],
				   [ 2, 200, 3, 1 ],
				   [ 2, 300, 3, 3 ],
				   ### Row 3 -- pink car
				   [ 3, 75,  2, 1 ],
				   [ 3, 150, 2, 3 ],
				   [ 3, 225, 2, 1 ],
				   [ 3, 375, 2, 2 ],
				   ### Row 4 -- white car
				   [ 4, 75,  5, 1 ],
				   [ 4, 150, 5, 3 ],
				   [ 4, 225, 5, 2 ],
				   [ 4, 375, 5, 3 ],
				   ### Row 5 -- Trucks 
				   [ 5, 30,  3, 1 ],
				   [ 5, 150, 3, 1 ],
				   [ 5, 250, 3, 1 ],
				   [ 5, 350, 3, 3 ]
			   ]
		return Vehicles[vehicle]

class Goals( pygame.sprite.Sprite ):
	def __init__( self ):
		pygame.sprite.Sprite.__init__( self )
		self.x, self.y, self.w, self.h = 0
		self.occupied 	= 0
		self.fly	= 0
		self.gator	= 0

class pyFrog( ):
	def __init__( self ):
	#	pygame.sprite.Sprite.__init( self )
		self.config     = config.GlobalDefs( )
		self.pos	= [ 0, 0 ]
		self.oldPos	= [ 0, 0 ]	
		self.direction	= 0
		self.location	= 0
		self.hopCount	= 0
		self.currentRow	= 0
		self.alive	= True
		self.riding	= False
		self.ridingType	= 0
		self.deathType	= 0
		self.deathCount	= 0
	
		self.src	= [ 0, 0, self.config.Frame, self.config.Frame ]
		self.dst	= [ 0, 0 ]

	def draw( self, screen, gfx ):
		screen.blit( gfx.frogger_image, self.pos, self.src )

	def reset( self, config ):
		self.pos        = [ self.config.Frog_start_x, self.config.Frog_start_y ]
		self.oldPos     = self.pos
		self.hopCount   = 0
		self.direction  = 0
		self.currentRow = 0
		self.alive	= True
		self.riding	= False
		self.deathType	= 0  # Death type SPLAT or SPLASH
		self.deathCount = 0  # Death animation timer
	
		self.src	= [ 0, 0, self.config.Frame, self.config.Frame ]
		self.dst	= self.pos

