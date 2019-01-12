#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#  dodPoker:  a poker server to run automated texas hold'em
#  poker rounds with bots
#  Copyright (C) 2017 wobe-systems GmbH
# -----------------------------------------------------------
# -----------------------------------------------------------
# Configuration
# You need to change the setting according to your environment
gregister_url='http://192.168.8.135:5001'
glocalip_adr='192.168.8.169'	#Mavis Laptop IP

# -----------------------------------------------------------

from flask import Flask, request
from flask_restful import Resource, Api
import sys

from requests import put
import json

app = Flask(__name__)
api = Api(app)

# Web API to be called from the poker manager
class PokerPlayerAPI(Resource):

    ## return bid to caller
    #
    #  Depending on the cards passed to this function in the data parameter,
    #  this function has to return the next bid.
    #  The following rules are applied:
    #   -- fold --
    #   bid < min_bid
    #   bid > max_bid -> ** error **
    #   (bid > min_bid) and (bid < (min_bid+big_blind)) -> ** error **
    #
    #   -- check --
    #   (bid == 0) and (min_bid == 0) -> check
    #
    #   -- call --
    #   (bid == min_bid) and (min_bid > 0)
    #
    #   -- raise --
    #   min_bid + big_blind + x
    #   x is any value to increase on top of the Big blind
    #
    #   -- all in --
    #   bid == max_bid -> all in
    #
    #  @param data : a dictionary containing the following values - example: data['pot']
    #                min_bid   : minimum bid to return to stay in the game
    #                max_bid   : maximum possible bid
    #                big_blind : the current value of the big blind
    #                pot       : the total value of the current pot
    #                board     : a list of board cards on the table as string '<rank><suit>'
    #                hand      : a list of individual hand cards as string '<rank><suit>'
    #
    #                            <rank> : 23456789TJQKA
    #                            <suit> : 's' : spades
    #                                     'h' : hearts
    #                                     'd' : diamonds
    #                                     'c' : clubs
    #
    # @return a dictionary containing the following values
    #         bid  : a number between 0 and max_bid
    def __get_bid(self, data):
		
		x = 0
		bid = data['min_bid']

		##data['max_bid'] - (data['min_bid'] + data['big_blind'])

		two = 0
		three = 0
		four = 0
		five = 0
		six = 0
		seven = 0
		eight = 0
		nine = 0
		ten = 0
		Joker = 0
		Queen = 0
		King = 0
		As = 0

		spades = 0
		hearts = 0
		diamnond = 0
		clubs = 0

		mylist = []

		for i in data['board']:

			if data['borad'][i][0] == '2':
				two ++
			if data['board'][i][0] == '3':
				three ++
			if data['board'][i][0] == '4':
				four ++
			if data['board'][i][0] == '5':
				fife ++
			if data['board'][i][0] == '6':
				six ++
			if data['board'][i][0] == '7':
				seven ++
			if data['board'][i][0] == '8':
				eight ++
			if data['board'][i][0] == '9':
				nine ++
			if data['board'][i][0] == 'T':
				ten ++
			if data['board'][i][0] == 'J':
				Joker ++
			if data['board'][i][0] == 'K':
				King ++
			if data['board'][i][0] == 'Q':
				Queen ++
			if data['board'][i][0] == 'A':
				As ++

			if data['board'][i][1] == 's':
				spades ++
			if data['board'][i][1] == 'd':
				diamonds ++
			if data['board'][i][1] == 'h':
				hearts ++
			if data['board'][i][1] == 'c':
				clubs ++


		for i in data['hand']:

			if data['hand'][i][0] == '2':
				two ++
			if data['hand'][i][0] == '3':
				three ++
			if data['hand'][i][0] == '4':
				four ++
			if data['hand'][i][0] == '5':
				fife ++
			if data['hand'][i][0] == '6':
				six ++
			if data['hand'][i][0] == '7':
				seven ++
			if data['hand'][i][0] == '8':
				eight ++
			if data['hand'][i][0] == '9':
				nine ++
			if data['hand'][i][0] == 'T':
				ten ++
			if data['hand'][i][0] == 'J':
				Joker ++
			if data['hand'][i][0] == 'K':
				King ++
			if data['hand'][i][0] == 'Q':
				Queen ++
			if data['hand'][i][0] == 'A':
				As ++

			if data['hand'][i][1] == 's':
				spades ++
			if data['hand'][i][1] == 'd':
				diamonds ++
			if data['hand'][i][1] == 'h':
				hearts ++
			if data['hand'][i][1] == 'c':
				clubs ++

		if(two < 1 || three < 1 || four < 1 || fife < 1 || six < 1 || seven < 1 || eight < 1 || nine < 1 || ten < 1 || Joker < 1 || King < 1 || Queen < 1  || As < 1):
			##rais 
			bid = data['max_bid'] - 1
			print(bid)

		elif(clubs < 4 || hearts < 4 || diamonds < 4 || spades < 4)
			#raise more but less then max-bid
			bid = data['max_bid'] - 1
			print(bid)

        return bid
    
    # -------------------------------------------------------------- do not change behind this line
    # dispatch incoming get commands
    def get(self, command_id):

        data = request.form['data']
        data = json.loads(data)

        if command_id == 'get_bid':
            return {'bid': self.__get_bid(data)}
        else:
            return {}, 201

    # dispatch incoming put commands (if any)
    def put(self, command_id):
        return 201


api.add_resource(PokerPlayerAPI, '/dpoker/player/v1/<string:command_id>')

# main function
def main():

    # run the player bot with parameters
    if len(sys.argv) == 4:
        team_name = sys.argv[1]
        api_port = int(sys.argv[2])
        api_url = 'http://%s:%s' % (glocalip_adr, api_port)
        api_pass = sys.argv[3]
    else:
        print("""
DevOps Poker Bot - usage instruction
------------------------------------
python3 dplayer.py <team name> <port> <password>
example:
    python3 dplayer bazinga 40001 x407
        """)
        return 0


    # register player
    r = put("%s/dpoker/v1/enter_game"%gregister_url, data={'team': team_name, \
                                                           'url': api_url,\
                                                           'pass':api_pass}).json()
    if r != 201:
        raise Exception('registration failed: probably wrong team name or password')

    else:
        print('registration successful')

    try:
        app.run(host='0.0.0.0', port=api_port, debug=False)
    finally:
        put("%s/dpoker/v1/leave_game"%gregister_url, data={'team': team_name, \
                                                           'url': api_url,\
                                                           'pass': api_pass}).json()
# run the main function
if __name__ == '__main__':
    main()


