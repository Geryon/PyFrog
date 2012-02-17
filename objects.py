import os, sys
import pygame
from pygame.locals import *
import config, collision

class Logs( pygame.sprite.Sprite ):
	def __init__( self, log ):
		pygame.sprite.Sprite.__init__( self )
		self.Global		= config.GlobalDefs( )
		self.Collision		= collision.Collision( )
		size, speed, row, X     = self.fetchLogData( log )
		self.size 		= size
		self.placement 		= [ self.Global.Left_side + X, self.Collision.getRowPixel( row ) ]
		self.oPlacement 	= self.placement
		self.row		= row
		self.speed		= speed
		self.pink		= 0
		self.gator		= 0
		pixelSrc		= 0
		if self.size == self.Global.Medium:
			pixelSrc	= self.Global.Frame * self.Global.Long 
		elif self.size == self.Global.Short:
			pixelSrc	= self.Global.Frame * ( self.Global.Long + self.Global.Medium ) 
		self.src		= [ 
						pixelSrc,
						self.Global.Frame,
						self.Global.Frame * self.size,
						self.Global.Frame
					  ]
		
	def update( self, game ):
		if self.placement[0] > self.Global.Right_side + 5:
			self.placement[0] = self.Global.Left_side - self.src[2] - 5
		self.placement[0] += self.speed

	def draw( self, screen, gfx ):
		screen.blit( gfx.frogger_image, self.placement, self.src )

	def fetchLogData( self, log ):
		Log = [
			## Log_Size, Speed, Row, X_Pos
			[ self.Global.Long,   3, 9,  0   ],
			[ self.Global.Long,   3, 9,  305 ],
			[ self.Global.Short,  2, 8,  25  ],
			[ self.Global.Short,  2, 8,  160 ],
			[ self.Global.Short,  2, 8,  380 ],
			[ self.Global.Medium, 4, 11, 140 ],
			[ self.Global.Medium, 4, 11, 440 ],
		      ]
		return Log[log]

class Vehicles( pygame.sprite.Sprite ):
	def __init__( self, vehicle ):
		self.Global 		= config.GlobalDefs( )
		self.Collision		= collision.Collision( )
		row, X, speed, level    = self.fetchVehicleData( vehicle )
		self.placement		= [ self.Global.Left_side + X, self.Collision.getRowPixel( row ) ]
		self.oPlacement		= self.placement
		self.direction		= self.Global.Left if row % 2 > 0 else self.Global.Right 
		self.row		= row
		self.speed		= speed
		self.level		= level
		self.src		= [ 
				   	    self.Global.Frame * ( 4 + row ),
			   		    self.Global.Frame * 2,
				   	    self.Global.Frame * 2 if row == 5 else self.Global.Frame,
				   	    self.Global.Frame
					  ]
		self.image		= 0

	def update( self, game ):
		if self.direction == self.Global.Right:
			if self.placement[0] > self.Global.Right_side + 5:
				self.placement[0] = self.Global.Left_side - self.src[2] - 5
			self.placement[0] += self.speed + game.level * .25
		else:
			if self.placement[0] < self.Global.Left_side - 5:
				self.placement[0] = self.Global.Right_side - self.src[2] + 5
			self.placement[0] -= self.speed + game.level * .25

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

class Turtles( pygame.sprite.Sprite ):
	def __init__( self, turtle ):
		self.canDive, self.diveTime, self.speed, self.row, self.X, self.count = self.fetchTurtleData(turtle)
		self.Global	= config.GlobalDefs()
		self.Collision	= collision.Collision( )
		self.diveStep	= 0
		self.animStep	= 0
		self.animDelay	= 0
		self.animFrame  = 0
		self.pos	= [ self.Global.Left_side + self.X, self.Collision.getRowPixel( self.row ) ]
		self.oPos	= self.pos
		self.src	= [ 0, self.Global.Frame * 2, self.Global.Frame, self.Global.Frame ]

	def draw( self, screen, gfx ):
		tsrc     = self.src
		tsrc[0]  = self.Global.Frame * self.animStep
		for n in range(self.count):	
			X  = self.pos[0]
			X += ( self.Global.Frame + 3 ) * n
			screen.blit( gfx.frogger_image, [ X, self.pos[1] ], tsrc )

	def update( self, game ):
		## move the turtles and wrap as necessary
		self.pos[0] -= self.speed		
		if self.pos[0] <= self.Global.Left_side - ( self.count * self.Global.Frame ) + 10:
			self.pos[0] = self.Global.Right_side + 10;

		## Set animation for the tail
		if self.animDelay >= self.Global.Turtle_anim_time:
			self.animDelay  = 0
			self.animStep  += 1
			if self.animStep > 2: self.animStep = 0
		else:
			self.animDelay += 1

	def fetchTurtleData( self, turtle ):
		Turtles = [
				## DIVE, DIVE_TIME, SPEED, ROW, STARTX, COUNT
				[ False, 0, 1, 7,  0,   3 ],
				[ True,  0, 1, 7,  125, 3 ],
				[ False, 0, 1, 7,  250, 3 ],
				[ True, 30, 1, 7,  375, 3 ],
				[ False, 0, 2, 10, 100, 2 ],
				[ True, 50, 2, 10, 200, 2 ],
				[ False, 0, 2, 10, 300, 2 ],
				[ True, 10, 2, 10, 400, 2 ],
				[ False, 0, 2, 10, 500, 2 ]
			  ]
		return Turtles[ turtle ]

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
		self.ridingIdx  = 0
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

