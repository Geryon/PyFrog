#!/usr/bin/python

import os, sys
import pygame
from pygame.locals import *

import config, objects, media, collision

global screen

def main( ):
#	pygame.mixer.init( )
	pygame.mixer.pre_init( 44100, -16, 2, 2048 )

	pygame.init( )

	global game
	global screen
	global frog
	global gfx
	global snd
	global Global
	global col 
	col    = collision.Collision( )
	Global = config.GlobalDefs( )
	screen = pygame.display.set_mode( ( Global.Screen_width, Global.Screen_height ) )
	game   = config.mainGame( )
	frog   = objects.pyFrog( )
	gfx    = media.images( )
	snd    = media.sounds( )

	pygame.display.set_caption( Global.Title )
	pygame.mouse.set_visible( 0 )
	
	beginGame( )


def beginGame( ):
#	next_heartbeat = 0
	done = False

	if loadMedia( ) <= 0:
		print "Error: Failed to load graphics and audio!\n" 
		return

	if Global.Debug: print "D: Starting main game loop"

	clock = pygame.time.Clock( )

	while 1:
		for event in pygame.event.get( ):
			if keyEvents( event ): return 
		
#		if clock.tick( ) >= next_heartbeat:
#			next_hearbeat = clock.tick( ) + heartbeat( )

		clock.tick( heartbeat( ) )

def keyEvents( event ):
	if event.type == QUIT: return 1
	elif event.type == KEYDOWN:
		if event.key == K_ESCAPE or event.key == K_q: 
			print "D: Exiting game"
			return 1

		##
		## Artificially increase the level
		##
		elif event.key == K_l:
			game.level += 1
			print "D: Increasing level to ", game.level

		##
		## kill the frog
		##
		elif event.key == K_k:
			frog.alive  = False
			print "D: Killed the frog."

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
		if game.goDelay > 7:
			game.playing	= False
			game.lives	= 0
			game.level	= 0
			game.score	= 0
			game.freefrog	= 0
			game.drawBG	= True
#			for i = 0; i < MAX_GOALS; i++:
#				goals[i].occupied = 0
		return 500
	else:
		## Move everything
		for n in range(Global.Max_vehicles): game.vehicle[n].update( game )
		for n in range(Global.Max_logs):     game.log[n].update( game )
		for n in range(Global.Max_turtles):  game.turtle[n].update( game )
	
	drawGameScreen( )

	return 25

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
	for n in range(Global.Max_goals): pass

	## Configure logs
	for n in range(Global.Max_logs): game.log.append( objects.Logs( n ) )
 
	## Configure turtles
	for n in range(Global.Max_turtles): game.turtle.append( objects.Turtles( n ) )

	## Configure vehicles
	for n in range(Global.Max_vehicles): game.vehicle.append( objects.Vehicles( n ) )

	## Reset the fly timer

	## Reset and draw frogger for start
	frog.reset( Global )

def drawImage( srcimg, sx, sy, sw, sh, dstimg, dx, dy, alpha ):
	return 1

def drawGameScreen( ):
	if frog.direction: moveFrog( )
	if frog.riding:    ridingFrog( )

	if frog.alive and col.collisionRow( frog, game ):
		if frog.currentRow < 6 or frog.currentRow >= 12:
			snd.splat.play()
			frog.deathType = Global.Splat
			frog.alive     = False
		else:
			snd.splash.play()
			frog.deathType = Global.Splash
			frog.alive     = False

	screen.blit( gfx.background_image, ( 0, 0 ) )
	for n in range(Global.Max_vehicles): game.vehicle[n].draw( screen, gfx, game )
	for n in range(Global.Max_logs)    : game.log[n].draw( screen, gfx )
	for n in range(Global.Max_turtles) : game.turtle[n].draw( screen, gfx )

	if frog.alive == False:
		if frog.deathType == False:
			print "D: Frog died"
			game.lives -= 1
			frog.reset( Global )
		else:
			frog.deathSeq( screen, gfx )
	else:
		frog.draw( screen, gfx )

	## Draw our black side borders
	pygame.draw.rect( screen, 0, ( 0, 0, Global.Left_side, Global.Screen_height ) )
	pygame.draw.rect( screen, 0, ( Global.Right_side, 0, \
					   Global.Screen_width - Global.Right_side, \
				  	   Global.Screen_height ) )

	pygame.display.flip( )

def moveFrog( ):
	x           = Global.Frame
	frog.oldPos = frog.pos
	( X, Y )    = frog.pos
	
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

	frog.oldPos = frog.pos
	frog.pos    = ( X, Y )

	##
	## Change the image frame to display
	## 
	frog.src = ( x, 0, Global.Frame, Global.Frame )

	frog.hopCount += 1

	if frog.hopCount >= Global.Hop_speed:
		frog.hopCount  = 0
		frog.direction = False
		game.score     += Global.Score_hop

	col.checkFrogBorder( frog )

def ridingFrog( ):
	if frog.hopCount > 0: return

	if frog.ridingType == Global.Log:
		speed = game.log[frog.ridingIdx].speed 
	elif frog.ridingType == Global.Turtle:
		speed = game.turtle[frog.ridingIdx].speed
		
	( X, Y )        = frog.pos
	frog.oldPos     = ( X, Y )

	if frog.riding == Global.Left    : frog.pos = ( X - speed, Y )
	elif frog.riding == Global.Right : frog.pos = ( X + speed, Y )

	col.checkFrogBorder( frog )

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
	
	snd.hop    = loadSound( 'dp_frogger_hop.ogg' )
	snd.splash = loadSound( 'dp_frogger_plunk.ogg' )
	snd.splat  = loadSound( 'dp_frogger_squash.ogg' )
	
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
