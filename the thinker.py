from game import *

import matplotlib.pyplot as plt
from IPython import display
import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet , QTrainer
MAX_MEMOREY = 200000
BATCH_SIZE = 10000
LEARNING_RATE = 0.001
the_difficulty = 2

number_of_random_rounds = 500

class the_thinker():
    def __init__(self):
        self.game = connect_4_game()
        self.number_of_rounds_played = 1
        self.epsilon = 0 # randomness
        self.gama = 0.2  # discount rate
        self.memorey = deque(maxlen = MAX_MEMOREY)

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


    def choose_move(self , state):
        # randomness to start
        self.epsilon = number_of_random_rounds - self.number_of_rounds_played

        move = []
        for i in self.game.slots:
            move.append(0)

        random_chooser = random.randint(0, number_of_random_rounds)
        if random_chooser < self.epsilon: ## if just random
            proven_that_there_is_room_here = False
            while proven_that_there_is_room_here == False:
                choice = random.randint(0, len(move)-1)
                move[choice] = 1
                proven_that_there_is_room_here = self.game.find_lowest_avaialable_y_at_this_x(choice)
        else:

            state0 = torch.tensor(state, dtype = torch.float)
            predicition = self.model(state0)
            choice = torch.argmax(predicition).item()
            move[choice] = 1;

            
        index = -1
        index_found = False
        for m in move:
            index+=1
            if m == 1:
                index_found = True
                break
        if not index_found:
            raise Exception("  no thinker x index chosen ")
        return move , index;

    def remember(self, state, action, reward, next_state , done):
        self.memorey.append((state, action, reward, next_state , done))

    def train_long_term_memorey(self , state_old, action, reward, state_new,game_over):
        if len(self.memorey) > BATCH_SIZE:
            mini_sample = random.sample(self.memorey, BATCH_SIZE)
        else:
            mini_sample = self.memorey
        state_old, action, reward, state_new,game_over = zip(*mini_sample)
        self.trainer.train_step(state_old, action, reward, state_new,game_over)

                                #state_old, move_decided, reward, state_new,game_over
    def train_short_term_memorey(self , state_old, action, reward, state_new,game_over):
        self.trainer.train_step(state_old, action, reward, state_new,game_over)

plt.ion()

def plot(scores, mean_scores , proc):
    display.clear_output(wait = True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score ratio')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    try:
        plt.savefig(str(the_difficulty)+" = difficulty    training graph    proc = "+str(proc)+".png")
    except:
        plt.savefig(str(the_difficulty)+" = difficulty spare    =    training graph    proc = "+str(proc)+".png")
    plt.show(block=False)
#    plt.pause(.1)

def train(proc = "naa"):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    best_score = 0
    agent = the_thinker()
    display , clock = agent.game.initialize_screen()
    while True:
    #    for i in range(1000):
    #        print('77777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777')
        old_game_state = agent.get_simple_state()
        move_decided , move_decided_index = agent.choose_move(old_game_state)
        reward, game_over , score = agent.game.play_thinker_step(move_decided_index)

        agent.game.computer_plays_turn( difficulty = the_difficulty)

        new_game_state = agent.get_simple_state()


        agent.train_short_term_memorey(old_game_state, move_decided, reward, new_game_state ,game_over )
        agent.remember(old_game_state, move_decided , reward, new_game_state ,game_over)

     #   agent.game.draw(display)
    #    clock.tick(2)

        if game_over:
            agent.game.check_for_win()
            agent.number_of_rounds_played += 1
            agent.train_long_term_memorey(old_game_state, move_decided, reward, new_game_state ,game_over)
            if score > best_score:
                best_score = score
            print(str(proc)+" = ROUND PLAYER = "+str(agent.number_of_rounds_played)+ "   ,    score ratio = "+ str(score) + "       reward = "+str(reward))
            plot_scores.append(score)
            total_score+= score
            average_score = total_score/agent.number_of_rounds_played
            plot_mean_scores.append(average_score)#
            if agent.number_of_rounds_played % 10 == 0:
                plot(plot_scores, plot_mean_scores , proc)
            game_over = False
train(proc = "naa")


