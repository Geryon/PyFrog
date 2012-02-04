import os, sys
import pygame
from pygame.locals import *

import objects, media

class GlobalDefs( ):
	##
	## Define our game initial variables
	##
	def __init__( self ):
		self.Debug		= 1
		self.Version		= "$Id: pyfrog.py,v 1.5 2011-11-05 04:07:53 nick Exp $"
		self.Title 		= "PyFrog"
		self.Screen_width 	= 640
		self.Screen_height 	= 480
		self.Colorkey		= ( 255, 0, 255 )
		self.Frog_start_x	= 306
		self.Frog_start_y	= 425
		self.Frame		= 24
		self.Hframe		= self.Frame / 2
		self.Hop_distance	= 30
		self.Hop_speed		= 3
		self.Row_base		= 425
		self.Left_side		= 115
		self.Right_side		= 525
		self.Splash		= 1
		self.Splat		= 2
		
		##
		## Baddies
		##
		self.Vehicle		= 0
		self.Log		= 1
		self.Turtle		= 2
		self.Gator		= 3
		self.Snake		= 4
		self.Beaver		= 5
		
		##
		## Goal areas
		##
		self.Max_goals		= 5
		
		##
		## Logs
		##
		self.Long		= 9
		self.Medium		= 6
		self.Short		= 4
		self.Max_wood		= 7
		
		##
		## Input
		##
		self.Up			= 273
		self.Down		= 274
		self.Right		= 275
		self.Left		= 276
		
		##
		## Turtles
		##
		self.Dive_start_time	= 50
		self.Dive_phase_time	= 20
		self.Max_turtles	= 9
		self.Turtle_anim_time	= 5
		
		##
		## Vehicles
		##
		self.Max_vehicles	= 40
		
		##
		## Our points table
		##
		self.Score_hop		= 10
		self.Score_goal		= 50
		self.Score_level	= 1000
		self.Score_fly		= 150
		self.Score_pink		= 200
		self.Score_seconds	= 10
		self.High_score		= 4630
		self.Score_free_frog	= 2000
		self.Lives		= 3
		
		##
		## The green game timer
		##
		self.Max_timer		= 350

##
## Some general game state stats
##
class mainGame( ):
	def __init__( self ):
		self.level 		= 0
		self.playing 		= False
		self.goDelay		= 0
		self.score		= 0
		self.lives		= 0
		self.freefrog		= 0
		self.drawBG 		= False
		self.timeLeft  		= 0
		self.vehicle		= [ ]
		self.log		= [ ]
