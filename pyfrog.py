#!/usr/bin/python

import screen
import pygame

##
## Define our game initial variables
##
VERSION		= "$Id: pyfrog.py,v 1.1 2011-06-14 14:23:26 nick Exp $"
TITLE 		= "Frogger"
SCREEN_WIDTH 	= 640
SCREEN_HEIGHT 	= 480
LIVES		= 3
SCORE		= 0

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

def beginGame( ):
	next_heartbeat = 0
	done = 0

	pygame.init( )
	size = width, height = SCREEN_WIDTH, SCREEN_HEIGHT
	screen = pygame.display.set_mode( size )
	if screen == NULL:
		print "ERROR"
		sys.exit( )

	print( "D: Starting main game loop" );

	while 1:
		for event in pygame.event.get( ):
			if event.type == pygame.QUIT: sys.exit( )

		
	
beginGame( )
