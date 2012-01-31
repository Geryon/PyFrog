#!/usr/bin/python

import os, sys
import pygame
from pygame.locals import *

##
## Define our game initial variables
##
DEBUG		= 1
DEBUG		= 1
VERSION		= "$Id: pyfrog.py,v 1.5 2011-11-05 04:07:53 nick Exp $"
TITLE 		= "PyFrog"
SCREEN_WIDTH 	= 640
SCREEN_HEIGHT 	= 480
COLORKEY	= ( 255, 0, 255 )
TRUE		= 1
FALSE		= 0
FROG_START_X	= 306
FROG_START_Y	= 425
FRAME		= 24
HFRAME		= FRAME / 2
HOP_DISTANCE	= 30
HOP_SPEED	= 3
ROW_BASE	= 425
LEFT_SIDE	= 115
RIGHT_SIDE	= 525
SPLASH		= 1
SPLAT		= 2

##
## Baddies
##
VEHICLE		= 0
LOG		= 1
TURTLE		= 2
GATOR		= 3
SNAKE		= 4
BEAVER		= 5

##
## Goal areas
##
MAX_GOALS	= 5

##
## Logs
##
SHORT_LOG	= 4
MEDIUM_LOG	= 6
LONG_LOG	= 9
MAX_WOOD	= 7

##
## Input
##
UP		= 273
DOWN		= 274
RIGHT		= 275
LEFT		= 276

##
## Turtles
##
DIVE_START_TIME	= 50
DIVE_PHASE_TIME	= 20
MAX_TURTLES	= 9
TURTLE_ANIM_TIME= 5

##
## Vehicles
##
MAX_VEHICLES	= 40

##
## Our points table
##
SCORE_HOP	= 10
SCORE_GOAL	= 50
SCORE_LEVEL	= 1000
SCORE_FLY	= 150
SCORE_PINK	= 200
SCORE_SECONDS	= 10
HIGH_SCORE	= 4630
SCORE_FREE_FROG	= 2000
LIVES		= 3

##
## The green game timer
##
MAX_TIMER	= 350

global screen

##
## Some general game state stats
##
class mainGame( ):
	def __init__( self ):
		self.level 	= 0
		self.playing 	= FALSE
		self.goDelay	= 0
		self.score	= 0
		self.lives	= 0
		self.freefrog	= 0
		self.drawBG 	= FALSE
		self.timeLeft   = MAX_TIMER
		
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
		self.hop	= 0

class Log( pygame.sprite.Sprite ):
	def __init__( self ):
		pygame.sprite.Sprite.__init__( self )
		self.size 	= 0
		self.placement 	= [ 0, 0 ]
		self.oPlacement = [ 0, 0 ]
		self.row	= 0
		self.speed	= 0
		self.pink	= 0
		self.gator	= 0
		
	def update( self ):
		self.placement += self.speed

class Vehicles( pygame.sprite.Sprite ):
	def __init__( self ): 
		self.placement 	= [ 0, 0 ]
		self.oPlacement = [ 0, 0 ]
		self.direction	= 0
		self.row	= 0
		self.speed	= 0
		self.level	= 0
		self.image	= 0
	
	def update( self ):
		self.placement += self.speed

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
	
		self.src	= [ 0, 0, FRAME, FRAME ]
		self.dst	= [ 0, 0 ]

def main( ):
	pygame.mixer.init( )
	pygame.mixer.pre_init( 44100, -16, 2, 2048 )

	pygame.init( )

	global game
	global screen
	global frog
	global gfx
	global snd
	screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
	game   = mainGame( )
	frog   = pyFrog( )
	gfx    = images( )
	snd    = sounds( )

	pygame.display.set_caption( TITLE )
	pygame.mouse.set_visible( 0 )
	
	beginGame( )


def beginGame( ):
	next_heartbeat = 0
	done = FALSE

	if loadMedia( ) <= 0:
		print "Error: Failed to load graphics and audio!\n" 
		return

	if DEBUG: print "D: Starting main game loop"

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
					game.playing = FALSE
				else:
					game.playing = TRUE
				print "D: Pausing Game"
				
		##
		## Key actions at the main menu
		##
		elif event.key == K_1:
			if not game.level and not game.playing:
				game.level   = 1
				game.playing = TRUE
				game.lives   = LIVES
				game.drawBG  = TRUE
				print "D: Starting Game"

		##
		## Key actions while playing a game
		##
		if game.level and game.playing and frog.alive:
			if event.key == K_LEFT:
				if not frog.direction:
					snd.hop.play()
					frog.hopCount = 0
					frog.direction = LEFT
			if event.key == K_RIGHT:
				if not frog.direction:
					snd.hop.play()
					frog.hopCount = 0
					frog.direction = RIGHT
			if event.key == K_UP:
				if not frog.direction:
					snd.hop.play()
					frog.hopCount = 0
					frog.direction = UP
					frog.currentRow += 1
			if event.key == K_DOWN:
				if not frog.direction:
					snd.hop.play()
					frog.hopCount = 0
					frog.direction = DOWN
					frog.currentRow -= 1

def updateGameState( ):
	if game.drawBG == TRUE:
		game.drawBG = FALSE
		configGameScreen( )

	if game.lives <= 0:
		print "GAME OVER"
		game.goDelay += 1
		drawGameOver( )
		if goDelay > 7:
			game.playing	= FALSE
			game.lives	= 0
			game.level	= 0
			game.score	= 0
			game.freefrog	= 0
			game.drawBG	= TRUE
#			for i = 0; i < MAX_GOALS; i++:
#				goals[i].occupied = 0
		return 500
	
	drawGameScreen( )

	return 50

##
## This configures a new game
##
def configGameScreen( ):
	game.drawBG = FALSE

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

	## Configure wood

	## Configure turtles

	## Configure vehicles

	## Reset the fly timer

	## Reset and draw frogger for start
	froggerReset( )

def froggerReset( ):
	game.timeLeft = MAX_TIMER

	frog.pos        = [ FROG_START_X, FROG_START_Y ]
	frog.oldPos     = frog.pos
	frog.hopCount   = 0
	frog.direction  = 0
	frog.currentRow = 0
	frog.alive	= TRUE
	frog.riding	= FALSE
	frog.deathType	= 0  # Death type SPLAT or SPLASH
	frog.deathCount = 0  # Death animation timer

	frog.src	= [ 0, 0, FRAME, FRAME ]
	frog.dst	= frog.pos

def drawImage( srcimg, sx, sy, sw, sh, dstimg, dx, dy, alpha ):
	return 1

def drawGameScreen( ):
	if frog.direction: 
		moveFrog( )

	screen.blit( gfx.background_image, ( 0, 0 ) )
	screen.blit( gfx.frogger_image, ( frog.pos ), ( frog.src ) )

	pygame.display.flip( )

def moveFrog( ):
	x = FRAME

	frog.oldPos = frog.pos
	( X, Y ) = frog.pos
	
	##
	## Time to actually move frogger
	##
	if frog.direction == UP:
		Y -= ( HOP_DISTANCE / HOP_SPEED )
	elif frog.direction == DOWN:
		x = ( 5 * FRAME )
		Y += ( HOP_DISTANCE / HOP_SPEED )
	elif frog.direction == LEFT:
		x = ( 7 * FRAME )
		X -= ( HOP_DISTANCE / HOP_SPEED )
	elif frog.direction == RIGHT:
		x = ( 3 * FRAME )
		X += ( HOP_DISTANCE / HOP_SPEED )

	frog.pos   = ( X, Y )
	##
	## Change the image frame to display
	## 
	frog.src = ( x, 0, FRAME, FRAME )

	frog.hopCount += 1

	if frog.hopCount >= HOP_SPEED:
		frog.hopCount  = 0
		frog.direction = FALSE
		game.score     += SCORE_HOP
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
