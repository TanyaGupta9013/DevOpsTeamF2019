# DevOpsPoker
DevOps Poker bot template

### How to use

To use the DevOps Poker bot template create a fork of the git repository and clone it to your workstation.

To run the bot in a game, you need to change the configuration at the top of `dplayer.py`.

    # -----------------------------------------------------------
    # Configuration
    # You need to change the setting according to your environment
    gregister_url='http://localhost:5001'
    glocalip_adr='127.0.0.1'
    # -----------------------------------------------------------

`gregister_url` is the game server URL to register the bot for a game.
`glocalip_adr` is the ip of your workstation to be called by the game server. Make sure your firewall does not block traffic on the port you've selected for your bot.

#### Prerequisites to run `dplayer.py` on your workstation

The following prerequisites are required to run `dplayer.py`:

- Python 3.5 or better
- packages required
	- flask
	- flask_restful
	- requests
- PIP to install packages - PIP is available on Windows in `Scripts` folder after installation.

#### Install packages

    pip install flask
    pip install flask_restful
    pip install requests
    

#### run the bot

The bot requires some command line parameters:

    DevOps Poker Bot - usage instruction
    ------------------------------------
    python dplayer.py <team name> <port> <password>
    example:
    python3 dplayer bazinga 40001 x407
    
Team name and password is provided by the organizers.

#### improve your game

The bot template is configured to fold as soon as possible. This means you cannot win. To improve your game you need to deploy new versions with a modified `__get_bid` function.
The function returns an integer value with your bid in a bet round. Hand cards and community cards are provided. The data passed to `__get_bid` in the `data` parameter is described in the source code comments. 

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
    #  @param data : a dictionary containing the following values
    #                min_bid   : minimum bid to return to stay in the game
    #                max_bid   : maximum possible bid
    #                big_blind : the current value of the big blind
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

#### Hints

1. The bot registers itself automatically when it's started. It automatically removes the registration if it crashes or terminates.
2. If a bot is started with the same team name on another host/port, the registration is updated and the new bot is used in the next game.
3. Errors in return values or not reachable, registered bots are interpreted as fold by the server.


