#!/usr/bin/python

import os, sys
import pygame
from pygame.locals import *

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
		self.Short_log		= 4
		self.Medium_log		= 6
		self.Long_log		= 9
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
	
global screen

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
		self.timeLeft  		= Global.Max_timer
		
class images( ):
	def __init__( self ):
		self.title_image	= 0
		self.title_rect		= 0
		self.frogger_image	= 0
		self.frogger_rect	= 0
		self.background_image	= 0
		self.background_rect	= 0

class sounds( ):
	def __init__( self ):
		self.hop		= 0

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
		self.pos	= [ 0, 0 ]
		self.oldPos	= [ 0, 0 ]	
		self.direction	= 0
		self.location	= 0
		self.hopCount	= 0
		self.currentRow	= 0
		self.alive	= 1
		self.riding	= 0
		self.ridingType	= 0
		self.deathType	= 0
		self.deathCount	= 0
	
		self.src	= [ 0, 0, Global.Frame, Global.Frame ]
		self.dst	= [ 0, 0 ]

	def draw( self ):
		screen.blit( gfx.frogger_image, self.pos, self.src )

	def reset( self ):
		game.timeLeft = Global.Max_timer

		self.pos        = [ Global.Frog_start_x, Global.Frog_start_y ]
		self.oldPos     = self.pos
		self.hopCount   = 0
		self.direction  = 0
		self.currentRow = 0
		self.alive	= True
		self.riding	= False
		self.deathType	= 0  # Death type SPLAT or SPLASH
		self.deathCount = 0  # Death animation timer
	
		self.src	= [ 0, 0, Global.Frame, Global.Frame ]
		self.dst	= self.pos


def main( ):
	pygame.mixer.init( )
	pygame.mixer.pre_init( 44100, -16, 2, 2048 )

	pygame.init( )

	global game
	global screen
	global frog
	global gfx
	global snd
	global Global
	Global = GlobalDefs( )
	screen = pygame.display.set_mode( ( Global.Screen_width, Global.Screen_height ) )
	game   = mainGame( )
	frog   = pyFrog( )
	gfx    = images( )
	snd    = sounds( )

	pygame.display.set_caption( Global.Title )
	pygame.mouse.set_visible( 0 )
	
	beginGame( )


def beginGame( ):
	next_heartbeat = 0
	done = False

	if loadMedia( ) <= 0:
		print "Error: Failed to load graphics and audio!\n" 
		return

	if Global.Debug: print "D: Starting main game loop"

	clock = pygame.time.Clock( )

	while 1:
		for event in pygame.event.get( ):
			if keyEvents( event ): return 
		
#		if pygame.GetTicks( ) >= next_heartbeat:
#			next_hearbeat = pygame.GetTicks( ) + heartbeat( )

		clock.tick( heartbeat( ) )

def keyEvents( event ):
	if event.type == QUIT: return 1
	elif event.type == KEYDOWN:
		print "D: Key Event Type: ", event.key

		if event.key == K_ESCAPE or event.key == K_q: 
			print "D: Exiting game"
			return 1

		##
		## Key actions if paused
		##
		elif event.key == K_p: 
			if game.level:
				if game.playing:
					game.playing = False
				else:
					game.playing = True
				print "D: Pausing Game"
				
		##
		## Key actions at the main menu
		##
		elif event.key == K_1:
			if not game.level and not game.playing:
				game.level   = 1
				game.playing = True
				game.lives   = Global.Lives
				game.drawBG  = True
				print "D: Starting Game"

		##
		## Key actions while playing a game
		##
		if game.level and game.playing and frog.alive:
			if event.key == K_LEFT:
				if not frog.direction:
					snd.hop.play()
					frog.hopCount = 0
					frog.direction = Global.Left 
			elif event.key == K_RIGHT:
				if not frog.direction:
					snd.hop.play()
					frog.hopCount = 0
					frog.direction = Global.Right 
			elif event.key == K_UP:
				if not frog.direction:
					snd.hop.play()
					frog.hopCount = 0
					frog.direction = Global.Up
					frog.currentRow += 1
			elif event.key == K_DOWN:
				if not frog.direction:
					snd.hop.play()
					frog.hopCount = 0
					frog.direction = Global.Down
					frog.currentRow -= 1

def updateGameState( ):
	if game.drawBG == True:
		game.drawBG = False
		configGameScreen( )

	if game.lives <= 0:
		print "GAME OVER"
		game.goDelay += 1
		drawGameOver( )
		if goDelay > 7:
			game.playing	= False
			game.lives	= 0
			game.level	= 0
			game.score	= 0
			game.freefrog	= 0
			game.drawBG	= True
#			for i = 0; i < MAX_GOALS; i++:
#				goals[i].occupied = 0
		return 500
	
	drawGameScreen( )

	return 50

##
## This configures a new game
##
def configGameScreen( ):
	game.drawBG = False

	print "Configing game screen"

	screen.blit( gfx.background_image, ( 0, 0 ) )

	##
	## Cars drive on rows 1 - 5
	## Logs are on rows 8, 9 and 11, 8 = short, 9 long, 11 medium
	## Turtles are on rows 7, 10
	## Frogger starts on Row 0, 
	## Sidewalk is row 6
	## and the goal is row 12
	##

	## Configure goals

	## Configure logs

	## Configure turtles

	## Configure vehicles

	## Reset the fly timer

	## Reset and draw frogger for start
	frog.reset( )

def drawImage( srcimg, sx, sy, sw, sh, dstimg, dx, dy, alpha ):
	return 1

def drawGameScreen( ):
	if frog.direction: 
		moveFrog( )

	screen.blit( gfx.background_image, ( 0, 0 ) )
	frog.draw( )

	pygame.display.flip( )

def moveFrog( ):
	x = Global.Frame

	frog.oldPos = frog.pos
	( X, Y ) = frog.pos
	
	##
	## Time to actually move frogger
	##
	if frog.direction == Global.Up:
		Y -= ( Global.Hop_distance / Global.Hop_speed )
	elif frog.direction == Global.Down:
		x = ( 5 * Global.Frame )
		Y += ( Global.Hop_distance / Global.Hop_speed )
	elif frog.direction == Global.Left:
		x = ( 7 * Global.Frame )
		X -= ( Global.Hop_distance / Global.Hop_speed )
	elif frog.direction == Global.Right:
		x = ( 3 * Global.Frame )
		X += ( Global.Hop_distance / Global.Hop_speed )

	frog.pos   = ( X, Y )
	##
	## Change the image frame to display
	## 
	frog.src = ( x, 0, Global.Frame, Global.Frame )

	frog.hopCount += 1

	if frog.hopCount >= Global.Hop_speed:
		frog.hopCount  = 1
		frog.direction = False
		game.score     += Global.Score_hop
#		frog.src       -= ( FRAME )

	checkFroggerBorder( )

def checkFroggerBorder( ):
	pass

def heartbeat( ):
	ticks = 0;
	if game.level:
		if game.playing:
			ticks = updateGameState( )
			if ticks <= 0: ticks = 50
			return ticks
		else:
			drawPauseScreen( )
			return 500
	else:
		drawTitleScreen( )
		return 500

def drawGameOver( ):
	print "D: Game Over man!  Game Over!"

def drawPauseScreen( ):
	print "D: Game Paused"

def drawTitleScreen( ):
	screen.blit( gfx.background_image, ( 0, 0 ) )
	screen.blit( gfx.title_image, ( 35, 92 ) )
	pygame.display.flip( )
	
def loadMedia( ):
	print "D: Loading media"
	gfx.background_image, gfx.background_rect = loadImage( 'gameboard.png' )
	gfx.frogger_image, gfx.frogger_rect = loadImage( 'frogger.png', -1 )
	gfx.title_image, gfx.title_rect = loadImage( 'pyfrog-title.png', -1 )
	
	snd.hop = loadSound( 'dp_frogger_hop.ogg' )
	
	return 1

def loadImage( filename, colorKey = None ):
	fullname = os.path.join( 'images', filename )

	try:
		image = pygame.image.load( fullname ).convert( )
	except pygame.error, message:
		print "ERROR: Failed to load image: " + fullname
		raise SystemExit, message
	
	if colorKey is not None:
		if colorKey is -1:
			colorKey = image.get_at( ( 0, 0 ) )
		image.set_colorkey( colorKey, RLEACCEL )

	return image, image.get_rect( )

def loadSound( name ):
	class noSound:
		def play( self ): pass

	if not pygame.mixer or not pygame.mixer.get_init( ):
		return noSound( )

	fullname = os.path.join( 'sounds', name )
	try:
		sound = pygame.mixer.Sound( fullname )
	except pygame.error, message:
		print "ERROR: Audio file missing: " + fullname
		return noSound

	return sound

################################################################################
## Begin Here
################################################################################

if __name__ == '__main__': main()
