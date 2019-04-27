'''
TO DO:
1) Investigate the Blocktypes lines further.
--There should be a way to save the name of the players like
Garrosh Hellscream, and then check in a given line in the name
of the player with their atk/health is in the line












Player1: PLAYING / Player2: PLAYING - ROUND 2 - WARRIOR Player1
Hero[P1]: 30 / Hero[P2]: 30

* Calculating solutions *** Player 1 ***
Depth: 1 --> 10/11 options! [SOLUTIONS:1]
Depth: 2 --> 45/52 options! [SOLUTIONS:8]
Depth: 3 --> 140/171 options! [SOLUTIONS:39]
Depth: 4 --> 342/454 options! [SOLUTIONS:151]
Depth: 5 --> 0/342 options! [SOLUTIONS:493]
- Player 1 - <WARRIOR Player1> ---------------------------
MinionAttackTask => [WARRIOR Player1] 'Southsea Deckhand[28]'(MINION) attack 'Garrosh Hellscream[6]'
Time: 4/3/2019 10:25:36 AM, Level: INFO, Location: Game, Blocktype: PLAY, TextMinionAttackTask => [WARRIOR Player1] 'Southsea Deckhand[28]'(MINION) attack 'Garrosh Hellscream[6]'
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Southsea Deckhand[28]' set data ATTACKING to 1
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Garrosh Hellscream[6]' set data DEFENDING to 1
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Garrosh Hellscream[6]' set data PREDAMAGE to 2
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Garrosh Hellscream[6]' set data PREDAMAGE to 0
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Garrosh Hellscream[6]' set data DAMAGE to 2
Time: 4/3/2019 10:25:36 AM, Level: INFO, Location: Character, Blocktype: ACTION, Text'Garrosh Hellscream[6]' took damage for 2(2).
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Southsea Deckhand[28]' set data ATTACKING to 0
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Garrosh Hellscream[6]' set data DEFENDING to 0
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Player[2]' set data NUM_OPTIONS_PLAYED_THIS_TURN to 1
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Player[2]' set data NUM_FRIENDLY_MINIONS_THAT_ATTACKED_THIS_TURN to 1
Time: 4/3/2019 10:25:36 AM, Level: INFO, Location: AttackPhase, Blocktype: ATTACK, Text'Southsea Deckhand[28]' is now exhausted.
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Southsea Deckhand[28]' set data EXHAUSTED to 1
Time: 4/3/2019 10:25:36 AM, Level: DEBUG, Location: Entity, Blocktype: TRIGGER, Text'Southsea Deckhand[28]' set data NUM_ATTACKS_THIS_TURN to 1
Time: 4/3/2019 10:25:36 AM, Level: INFO, Location: AttackPhase, Blocktype: ATTACK, Text[AttackPhase]'Southsea Deckhand[28]'[ATK:2/HP:1] attacked 'Garrosh Hellscream[6]'[ATK:0/HP:28].
'''


import re
import argparse

debug = False
log_file = False

def parse_options():
    parser = argparse.ArgumentParser(description="Class for parsing game data")
    parser.add_argument('data_file', help='path to the data file')
    parser.add_argument('-vb', '--verbose', action='store_true',help='set verbose logs')
    parser.add_argument('--log', action='store_true',help='choice to log to file')
    parser.add_argument('--sum', action='store_true', help='flag to print summary')
    parser.add_argument('--oth', action='store_true', help='flag to print other lines')
    parser.add_argument('--ron', action='store_true',help='flag to print health_difs')
    parser.add_argument('--end', action='store_true',help='flag to print end_turn health')
    parser.add_argument('--blk', action='store_true',help='flag to print blocktypes')
    ret_args = parser.parse_args()
    global debug
    if ret_args.verbose: debug = True
    global log_file
    if ret_args.log: log_file = open("{}.txt".format(now),"a")
    return ret_args

class Game_Filter:
    '''class to filter key info from fullgame.txt'''

    def __init__(self, infile):
        self.lines = []
        with open(infile) as f:
            for line in f:
                self.lines.append(line.strip("\n"))
        self.blocktypes = {}
        self.healths = []
        self.cur_round = []
        self.end_turns = []
        self.others = []

    def line_parser(self):
        for i in range(len(self.lines)):
            blockF, healthF, endturnF = False, False, False
            line = self.lines[i]
            prev = self.lines[i-1]
            block_query = re.search("Blocktype: [A-Z]+", line)
            if block_query != None:
                blockF = True
                #self.blocktypes[i] = block_query.group()
                self.blocktypes[i] = line

            health_query = re.search("Hero\[P1\]: [0-9]+ / Hero\[P2\]: [0-9]+", line)
            if health_query != None:
                healthF = True
                cur = health_query.group().strip('\n')
                health_list = [prev.strip('\n'), cur]
                self.healths.append(health_list)

            endturn_query = re.search(">>>Player [0-9] HEALTH", line)
            if endturn_query != None:
                endturnF = True
                end = line.strip("\n")
                self.end_turns.append(end)
                
            if not blockF and not healthF and not endturnF:
                self.others.append(line)

    def print_header(self, s):
        for i in range(45):
            print("_", end="")
        print(s, end = "")
        for i in range(45):
            print("_", end="")
        print()
        
    def print_summary(self):
        self.print_header("SUMMARY")
        print("Number of lines: {}".format(len(self.lines)))
        print("Number of blocktypes: {}".format(len(self.blocktypes)))
        print("Number of health declarations: {}".format(len(self.healths)))
        print("Number of others: {}".format(len(self.others)))
        
    def print_rounds(self):
        self.print_header("ROUNDS")
        for l in self.healths:
            #print(l[0])
            print(l[1])
        print()
        #Hero[P1]: 30 / Hero[P2]: 30

    def print_others(self):
        self.print_header("OTHERS")
        for line in self.others:
            print(line)
        print()

    def print_blocktypes(self):
        self.print_header("BLOCKTYPES")
        for key in self.blocktypes:
            print(key, self.blocktypes[key])

    def print_endturn_health(self):
        self.print_header("ENDTURN_HEALTH")
        for turn in self.end_turns:
            print(turn)

    def print_options(self, arg_list):
        if arg_list.sum:
            self.print_summary()
        if arg_list.end:
            self.print_endturn_health()
        if arg_list.ron:
            self.print_rounds()
        if arg_list.oth:
            self.print_others()
        if arg_list.blk:
            self.print_blocktypes()
            
if __name__ == "__main__":
    args = parse_options()
    #'fullgame01_040319.txt'
    game_name = args.data_file
    game_obj = Game_Filter(game_name)
    game_obj.line_parser()
    game_obj.print_options(args)
    
