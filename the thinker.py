from game import *

import matplotlib.pyplot as plt
from IPython import display
import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet , QTrainer , Linear_QNet_extra_layers
import time as tim



##### controls
show_game = False
show_plot = False
save_plot = True

MAX_MEMOREY = 200000
BATCH_SIZE = 10000
LEARNING_RATE = 0.001
the_difficulty = 3

extra_layers = True


############
monitor_failed_attempts_to_place_coins = True
if show_plot:
    plt.ion()

number_of_random_rounds = 900

class the_thinker():
    def __init__(self):
        self.game = connect_4_game()
        self.number_of_rounds_played = 1
        self.epsilon = 0 # randomness
        self.gama = 0.2  # discount rate
        self.memorey = deque(maxlen = MAX_MEMOREY)
        if extra_layers:
            self.model = Linear_QNet_extra_layers(3 * self.game.y_rows * self.game.x_rows, 6 * self.game.y_rows * self.game.x_rows,self.game.x_rows)
        else:
            self.model = Linear_QNet(3 * self.game.y_rows * self.game.x_rows, 6 * self.game.y_rows * self.game.x_rows,self.game.x_rows)#### input len = area of game board x 3

        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gama=self.gama)


    def get_simple_state(self):
        state = []
        positions_of_thinkers_tiles = []
        positions_of_enemy_tiles = []
        empty_tiles = []
        for x in range(len(self.game.slots)):
            for y ,  y_ind in zip(self.game.slots[x] , range(len(self.game.slots[x]))):
                if y.occupied_by_player and y.occupied_by_computer:
                    raise Execption("bugger, this should never happen")
                if y.occupied_by_player:
                    positions_of_thinkers_tiles.append(True)
                    positions_of_enemy_tiles.append(False)
                elif y.occupied_by_computer:
                    positions_of_thinkers_tiles.append(False)
                    positions_of_enemy_tiles.append(True)
                else:
                    positions_of_thinkers_tiles.append(False)
                    positions_of_enemy_tiles.append(False)
                if y.empty():
                    empty_tiles.append(True)
                else:
                    empty_tiles.append(False)

        for enemy in positions_of_enemy_tiles:
            state.append(enemy)
        for our in positions_of_thinkers_tiles:
            state.append(our)
        for empty in empty_tiles:
            state.append(empty)

        return state


    def choose_move(self , state , unplayable , times_tried_to_choose_a_move):

        # randomness to start
        self.epsilon = number_of_random_rounds - self.number_of_rounds_played
        move = []
        draw_found = False
        all_failed = False
        for i in self.game.slots:
            move.append(0)
        random_chooser = random.randint(0, number_of_random_rounds)
        if random_chooser < self.epsilon: ## if just random
            proven_that_there_is_room_here = False
            while proven_that_there_is_room_here == False:
                choice = random.randint(0, len(move)-1)
                move[choice] = 1
                proven_that_there_is_room_here = self.game.find_lowest_avaialable_y_at_this_x(choice)
                all_failed = self.game.completletley_full_check()
                if all_failed == True:
                    print("this all failed failed choice")
                    break;
                else:
                    pass
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            predicition = self.model(state0)
            for i in range(len(predicition)):
                for r in unplayable:
                    if i == r:
                        predicition[i] = - 99999
            choice = torch.argmax(predicition).item()

            move[choice] = 1;
        if all_failed == False:
            index = -1
            index_found = False
            for m in move:
                index+=1
                if m == 1:
                    index_found = True
                    break
            if not index_found:
                raise Exception("  no thinker x index chosen ")
            return move , index , all_failed;
        else:
            print("returnig this all failed thing")
            #### how to pass back move decided if none decided, just push it back in the usual old way but in game over when stuff chosen , add the draw check jusat before return
            return 9999 , 9999 , all_failed

        print("yoo hoooo ")
    def remember(self, state, action, reward, next_state , done):
        self.memorey.append((state, action, reward, next_state , done))

    def train_long_term_memorey(self , state_old, action, reward, state_new,game_over):
        if len(self.memorey) > BATCH_SIZE:
            mini_sample = random.sample(self.memorey, BATCH_SIZE)
        else:
            mini_sample = self.memorey
        state_old, action, reward, state_new,game_over = zip(*mini_sample)
        self.trainer.train_step(state_old, action, reward, state_new,game_over , False)

                                #state_old, move_decided, reward, state_new,game_over
    def train_short_term_memorey(self , state_old, action, reward, state_new,game_over):
        self.trainer.train_step(state_old, action, reward, state_new,game_over ,self.game.completletley_full_check())


#str(the_difficulty)+" = difficulty    training graph    proc = "+str(proc)+".png"
def plot(scores, mean_scores , proc  , show_plot , save_plot, title , xlbl, ylbl, filename):
    if show_plot:

        display.clear_output(wait = True)
        display.display(plt.gcf())

    plt.clf()
    plt.title(title)
    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    if save_plot:
        try:
            plt.savefig(filename)
        except:
            plt.savefig("spare "+str(filename))
    if show_plot:
        plt.show(block=False)
        plt.pause(.1)

def train(proc = "naa"):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    best_score = 0
    agent = the_thinker()
    number_of_failed_attempts_to_place_coins = 0
    times_of_failed_attempts_to_place_coins = []
    y_for_times_of_failed_attempts_to_place_coins = []
    if show_game:
        display , clock = agent.game.initialize_screen()
    while True:
    #    for i in range(1000):
    #        print('77777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777')


        move_playable = False
        moves_unplayable = []

        times_tried_to_choose_a_move = 0
        draw_found = False
  #      print(" bread crum 0.1 ")
        while move_playable == False:
   #         print(" bread crum 0.2 ")
            old_game_state = agent.get_simple_state()
            move_decided , move_decided_index, draw_found = agent.choose_move(old_game_state , moves_unplayable , times_tried_to_choose_a_move)
            if draw_found == False:
    #            print("draw  not found")
                reward, game_over , score , move_playable = agent.game.play_thinker_step(move_decided_index)
                times_tried_to_choose_a_move+= 1
                if move_playable == False:
                #    print("this move unplayablle ")
                    if monitor_failed_attempts_to_place_coins:
                        number_of_failed_attempts_to_place_coins+= 1
                        times_of_failed_attempts_to_place_coins.append(number_of_failed_attempts_to_place_coins)
                        y_for_times_of_failed_attempts_to_place_coins.append(times_tried_to_choose_a_move)
                    moves_unplayable.append(move_decided_index)
                    new_game_state = agent.get_simple_state()
                    agent.train_short_term_memorey(old_game_state, move_decided, reward, new_game_state ,game_over )
                else:
                    if monitor_failed_attempts_to_place_coins:
                        times_of_failed_attempts_to_place_coins.append(number_of_failed_attempts_to_place_coins)
                        y_for_times_of_failed_attempts_to_place_coins.append(times_tried_to_choose_a_move)
            else:
       #         print("draw found so setting move playable")
                move_playable = True
#        print(" bread crum 1 ")
        if draw_found == False:
            agent.game.computer_plays_turn( difficulty = the_difficulty)


        new_game_state = agent.get_simple_state()
        if draw_found == False:
 #           print(" bread crum 2 ")
            agent.train_short_term_memorey(old_game_state, move_decided, reward, new_game_state ,game_over )
  #          print(" bread crum  3 ")
            agent.remember(old_game_state, move_decided , reward, new_game_state ,game_over)
   #         print(" bread crum  4 ")
    #    print(" bread crum  4.5 ")


        if show_game:
            agent.game.draw(display)
     #   print(" bread crum  5 ")
        if game_over or draw_found:
            agent.game.check_for_win()
            agent.number_of_rounds_played += 1
            agent.train_long_term_memorey(old_game_state, move_decided, reward, new_game_state ,game_over)
            if score > best_score:
                best_score = score
            if extra_layers:
                print(str(proc)+" = ROUND PLAYER = "+str(agent.number_of_rounds_played)+ "   ,    score ratio = "+ str(score) + "       reward = "+str(reward)+ "   with extra layers ")
            else:
                print(str(proc)+" = ROUND PLAYER = "+str(agent.number_of_rounds_played)+ "   ,    score ratio = "+ str(score) + "       reward = "+str(reward))
            plot_scores.append(score)
            total_score+= score
            average_score = total_score/agent.number_of_rounds_played
            plot_mean_scores.append(average_score)#
            if show_plot or save_plot:
                if agent.number_of_rounds_played % 40 == 0:
                    if extra_layers:
                        file_name = str(the_difficulty)+" = difficulty   extra layerrs    score ratio    proc = "+str(proc)+".png"
                    else:
                        file_name  = str(the_difficulty)+" = difficulty   no  extra layerrs  ,   score ratio    proc = "+str(proc)+".png"
                    plot(plot_scores, plot_mean_scores , proc , show_plot , save_plot, "score ratio over time", "number of games" , "score ratio" , file_name )

            if monitor_failed_attempts_to_place_coins:
                if agent.number_of_rounds_played % 40 == 0:
                    y = times_of_failed_attempts_to_place_coins
# y_for_times_of_failed_attempts_to_place_coins.append(times_tried_to_choose_a_move)
                    x = y_for_times_of_failed_attempts_to_place_coins
                    if extra_layers:
                        file_name =  str(the_difficulty)+" = difficulty  extra layerr  times failed    proc = "+str(proc)+".png"
                    else:
                        file_name  =  str(the_difficulty)+" = difficulty   no  extra layerrs    times failed    proc = "+str(proc)+".png"
                    plot(x , y , proc , show_plot , save_plot, "times failed to place coin", "number of total attempts" , "number of fails" ,file_name )

            game_over = False
            if draw_found:
       #         agent.game.draw(display)
      #          print("weve drawn")
                agent.game.draw_reset()

train(proc = "naa")

scrap = '''
def get_game_state(self):
state = []
positions_of_thinkers_tiles = []
positions_of_enemy_tiles = []
positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line = []
positions_of_thinkers_pairs_of_tiles_with_room_for_1_more_to_make_horizontal_line = []
positions_of_enemies_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line = []
positions_of_enemies_pairs_of_tiles_with_room_for_1_more_to_make_horizontal_line = []
positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_box = []
positions_of_thinkers_pairs_of_tiles_with_room_for_1_more_to_make_box = []
positions_of_enemies_pairs_of_tiles_with_room_for_2_more_to_make_box = []
positions_of_enemies_pairs_of_tiles_with_room_for_1_more_to_make_box = []
for x in range(len(self.game.slots)-1):
for y ,  y_ind in zip(self.game.slots[x] , range(len(self.game.slots[x])-1)):
    if y.occupied_by_player and y.occupied_by_computer:
        raise Execption("bugger, this should never happen")
    if y.occupied_by_player:
        positions_of_thinkers_tiles.append(True)
        positions_of_enemy_tiles.append(False)
    elif y.occupied_by_computer:
        positions_of_thinkers_tiles.append(False)
        positions_of_enemy_tiles.append(True)
    else:
        positions_of_thinkers_tiles.append(False)
        positions_of_enemy_tiles.append(False)

    ## if 2 needed (horizontal)
    ## if 2 slots occupied
    if (self.game.slots[x][y].occupied_by_player and self.game.slots[x+1][y].occupied_by_player) or :## if 2 slots occupied
        ## and 2 slots are empty
        if (self.game.slots[x-1][y].empty() and self.game.slots[x+2][y].empty()) or (self.game.slots[x-1][y].empty() and self.game.slots[x-2][y].empty() ) or (self.game.slots[x+2][y].empty() and self.game.slots[x+3][y].empty() ):
            positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line.append(True)
        else:
            positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line.append(False)
   ## if 2 slots occupied (other tile)
    elif (self.game.slots[x][y].occupied_by_player and self.game.slots[x-1][y].occupied_by_player):
        ## and 2 slots are empty
        if (self.game.slots[x+1][y].empty() and self.game.slots[x+2][y].empty()) or (self.game.slots[x+1][y].empty() and self.game.slots[x-2][y].empty() ) or (self.game.slots[x-2][y].empty() and self.game.slots[x-3][y].empty() ):
            positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line.append(True)
        else:
            positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line.append(False)
    ## no 2 slots here
    else:
        positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line.append(False)



    ## if 1 needed   (left tile)(horizontal)
    if (self.game.slots[x][y].occupied_by_player and self.game.slots[x+1][y].occupied_by_player and self.game.slots[x+2][y].occupied_by_player):
        if (self.game.slots[x-1][y].empty()) or (self.game.slots[x+3][y].empty()):
            positions_of_thinkers_pairs_of_tiles_with_room_for_1_more_to_make_horizontal_line.append(True)
        else:
            positions_of_thinkers_pairs_of_tiles_with_room_for_1_more_to_make_horizontal_line.append(False)
    #        (middle tile )
    elif (self.game.slots[x][y].occupied_by_player and self.game.slots[x+1][y].occupied_by_player and self.game.slots[x-1][y].occupied_by_player):
        if (self.game.slots[x-2][y].empty()) or (self.game.slots[x+2][y].empty()):
                positions_of_thinkers_pairs_of_tiles_with_room_for_1_more_to_make_horizontal_line.append(True)
            else:
                positions_of_thinkers_pairs_of_tiles_with_room_for_1_more_to_make_horizontal_line.append(False)
    ##   right tile
elif (self.game.slots[x][y].occupied_by_player and self.game.slots[x-1][y].occupied_by_player and self.game.slots[x-2][y].occupied_by_player):
        if (self.game.slots[x+1][y].empty()) or (self.game.slots[x=3][y].empty()):
            positions_of_thinkers_pairs_of_tiles_with_room_for_1_more_to_make_horizontal_line.append(True)
        else:
            positions_of_thinkers_pairs_of_tiles_with_room_for_1_more_to_make_horizontal_line.append(False)



     and self.game.slots[x+2][y].occupied_by_player)  or (self.game.slots[x-1][y].occupied_by_player and self.game.slots[x][y].occupied_by_player and self.game.slots[x+1][y].occupied_by_player and ) or (self.game.slots[x-2][y].occupied_by_player and self.game.slots[x-1][y].occupied_by_player and self.game.slots[x][y].occupied_by_player):## if 3 slots occupied
        if (self.game.slots[x-1][y].occupied_by_player == False
            positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line.append(True)
        else:
            positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line.append(False)
    else:
        positions_of_thinkers_pairs_of_tiles_with_room_for_2_more_to_make_horizontal_line.append(False)
        '''
