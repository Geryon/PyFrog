import os, sys
import pygame
from pygame.locals import *

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
	def __init__( self ): 
		self.placement 		= [ 0, 0 ]
		self.oPlacement		= [ 0, 0 ]
		self.direction		= 0
		self.row		= 0
		self.speed		= 0
		self.level		= 0
		self.image		= 0
	
	def update( self ):
		self.placement 		+= self.speed

	def draw( self ):
		print "D: Display Vehicle"		
	def Set( self, row, X, speed, level ):
		pass

class Goals( pygame.sprite.Sprite ):
	def __init__( self ):
		pygame.sprite.Sprite.__init__( self )
		self.x, self.y, self.w, self.h = 0
		self.occupied 	= 0
		self.fly	= 0
		self.gator	= 0

class pyFrog( ):
	def __init__( self, config ):
	#	pygame.sprite.Sprite.__init( self )
#		self.parent     = parent
#		self.config	= parent.config
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
	
		self.src	= [ 0, 0, config.Frame, config.Frame ]
		self.dst	= [ 0, 0 ]

	def draw( self, screen, gfx ):
		screen.blit( gfx.frogger_image, self.pos, self.src )

	def reset( self, config ):
		self.pos        = [ config.Frog_start_x, config.Frog_start_y ]
		self.oldPos     = self.pos
		self.hopCount   = 0
		self.direction  = 0
		self.currentRow = 0
		self.alive	= True
		self.riding	= False
		self.deathType	= 0  # Death type SPLAT or SPLASH
		self.deathCount = 0  # Death animation timer
	
		self.src	= [ 0, 0, config.Frame, config.Frame ]
		self.dst	= self.pos

