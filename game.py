import pygame
from pygame import *
import math
import numpy as np
import random
import copy
import time as tim

rows = 6
cols = 6

## i built this game specifically to teach a machine through RL how to platy it
mi_turns = [0,1,1,2,4,5,6,7,8, 8 , 9 , 1 , 5, 6,6,8,6,5,5,3,4,9,6, 1]


pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,255)
grey=(169,169,169)
yellow = (246, 240, 55)



class slot():
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.occupied_by_computer = False
        self.occupied_by_player = False
    def empty(self):
        if (self.occupied_by_computer == False and self.occupied_by_player == False):
            return True
        else:
            return False

class connect_4_game():
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.draw_count = 0
        self.game_over = False
        self.x_rows = rows
        self.y_rows = cols
        self.slots = []
        self.turn_counter = 0
        self.reward  = 0
        self.score = 0

        for x in range(self.x_rows):
            ys = []
            for y in range(self.y_rows):
                ys.append(slot(x , y))
            self.slots.append(ys)

    def completletley_full_check(self):
        all_failed = True
        for x in range(len(self.slots)):
            check = self.find_lowest_avaialable_y_at_this_x(x)
            if type(check) == type(True):
                if check == False:
                    pass
                else:
                    all_failed = False
            else:
                all_failed = False
        if all_failed:
            pass
    #        tim.sleep(9)
        return all_failed;



    def new_game(self):

        self.game_over = False

        self.slots = []
        self.turn_counter = 0

        for x in range(self.x_rows):
            ys = []
            for y in range(self.y_rows):
                ys.append(slot(x , y))
            self.slots.append(ys)
    def end_round_with_no_winner(self):
        self.game_over = True
        self.reward += -0.1
        self.new_game()

    def computer_win(self):
        self.game_over = True
        self.computer_score+= 1
        self.reward += -1
        self.new_game()
        print("comp win")
    #    tim.sleep(9)
    #    print(5/0)
    def player_win(self):
        self.game_over = True
        self.player_score+= 1
        self.reward += 1
        self.new_game()
        print("player win")
    #    tim.sleep(9)
    #    print(9/0)
    def check_for_line_of_4(self , ret=False):

        ## horizontal check
#        for i in range(2):
#            print("################################")
        for x in range(len(self.slots)):
            for y in range(len(self.slots[x])):

                slot = self.slots[x][y]
                if slot.occupied_by_computer == True or slot.occupied_by_player == True:
                    try:
                        slot_right = self.slots[x+1][y]
                        slot_2right = self.slots[x+2][y]
                #        print(x+3)
                        slot_3right = self.slots[x+3][y]
                        if slot.occupied_by_computer == True:
                            if slot_right.occupied_by_computer == True:
                                if slot_2right.occupied_by_computer == True:
                                    if slot_3right.occupied_by_computer == True:
                                        if ret:
                                            return True
        #                                print("horiz line of 4 comp   starting with "+str(slot.x)+" , "+str(slot.y) +" then "+ str(slot_right.x)+ " , "+str(slot_right.y)+" then "+ str(slot_2right.x)+ " , "+str(slot_2right.y)+" then "+ str(slot_3right.x)+ " , "+str(slot_3right.y))
                                        self.computer_win()
                        if slot.occupied_by_player == True:
                            if slot_right.occupied_by_player == True:
                                if slot_2right.occupied_by_player == True:
                                    if slot_3right.occupied_by_player == True:
                                        if ret:
                                            return True
        #                                    print("horizontal line of 4 player   starting with "+str(slot.x)+" , "+str(slot.y) +" then "+ str(slot_right.x)+ " , "+str(slot_right.y)+" then "+ str(slot_2right.x)+ " , "+str(slot_2right.y)+" then "+ str(slot_3right.x)+ " , "+str(slot_3right.y) )
                    #                    print("vert line of 4 player")
                                        self.player_win()
                    except IndexError:
                        pass
        ## vertical check

        for x in range(len(self.slots)):
            for y in range(len(self.slots[x])):
                slot = self.slots[x][y]
        #        if x == 0 and y > 5:
        #            print(str(x)+ " , " + str(y))
                if slot.occupied_by_computer == True or slot.occupied_by_player == True:
                    try:
        #                print("good one = "+str(x)+ " , " + str(y))
                        slot_up = self.slots[x][y-1]
                        slot_2up = self.slots[x][y-2]
                        slot_3up = self.slots[x][y-3]
                        if slot.occupied_by_computer == True:
#                            print("vert line of 4   comp    aaaa    x, y = "+str(x)+ " , "+str(y))
                            if slot_up.occupied_by_computer == True:
#                                print("vert line of 4   comp  bbbbbb   ")
                                if slot_2up.occupied_by_computer == True:
#                                    print("vert line of 4   comp     ccccc   ")
                                    if slot_3up.occupied_by_computer == True:
        #                                print("vert line of 4 comp   starting with "+str(slot.x)+" , "+str(slot.y)  +" then "+ str(slot_up.x)+ " , "+str(slot_up.y)+" then "+ str(slot_2up.x)+ " , "+str(slot_2up.y)+" then "+ str(slot_3up.x)+ " , "+str(slot_3up.y) )
                                        if ret:
                                            return True

#                                        print("vert line of 4   comp  ")
                                        self.computer_win()
                        if slot.occupied_by_player == True:
#                            print("vert line of 4  p    aaaa  x, y = "+str(x)+ " , "+str(y))
                            if slot_up.occupied_by_player == True:
#                                print("vert line of 4   p    bbbb ")
                                if slot_2up.occupied_by_player == True:
#                                    print("vert line of 4   p    ccccc ")
                                    if slot_3up.occupied_by_player == True:
        #                                print("vert line of 4 player   starting with "+str(slot.x)+" , "+str(slot.y)  +" then "+ str(slot_up.x)+ " , "+str(slot_up.y)+" then "+ str(slot_2up.x)+ " , "+str(slot_2up.y)+" then "+ str(slot_3up.x)+ " , "+str(slot_3up.y) )
                                        if ret:
                                            return True
#                                        print("vert line of 4 player")
                                        self.player_win()
                    except IndexError:
                        pass

            ## diagonal up
        for x in range(len(self.slots)):
            for y in range(len(self.slots[x])):
                slot = self.slots[x][y]
        #        if x == 0 and y > 5:
        #            print(str(x)+ " , " + str(y))
                if slot.occupied_by_computer == True or slot.occupied_by_player == True:
                    try:
        #                print("good one = "+str(x)+ " , " + str(y))
                        if y-3 < len(self.slots[x])-1:
                            slot_up = self.slots[x+1][y-1]
                            slot_2up = self.slots[x+2][y-2]
                            slot_3up = self.slots[x+3][y-3]
                            if slot.occupied_by_computer == True:
    #                            print("diag line of 4   comp    aaaa    x, y = "+str(x)+ " , "+str(y))
                                if slot_up.occupied_by_computer == True:
    #                                print("diag line of 4   comp  bbbbbb   ")
                                    if slot_2up.occupied_by_computer == True:
    #                                    print("diag line of 4   comp     ccccc   ")
                                        if slot_3up.occupied_by_computer == True:
        #                                    print("diag line of 4 comp   starting with "+str(slot.x)+" , "+str(slot.y)  +" then "+ str(slot_up.x)+ " , "+str(slot_up.y)+" then "+ str(slot_2up.x)+ " , "+str(slot_2up.y)+" then "+ str(slot_3up.x)+ " , "+str(slot_3up.y) )
                                            if ret:
                                                return True
    #                                        print("diag line of 4   comp  ")
                                            self.computer_win()
                            if slot.occupied_by_player == True:
    #                            print("diag line of 4  p    aaaa  x, y = "+str(x)+ " , "+str(y))
                                if slot_up.occupied_by_player == True:
    #                                print("diag line of 4   p    bbbb ")
                                    if slot_2up.occupied_by_player == True:
    #                                    print("diag line of 4   p    ccccc ")
                                        if slot_3up.occupied_by_player == True:
        #                                    print(" diag line of 4 player   starting with "+str(slot.x)+" , "+str(slot.y) +" then "+ str(slot_up.x)+ " , "+str(slot_up.y)+" then "+ str(slot_2up.x)+ " , "+str(slot_2up.y)+" then "+ str(slot_3up.x)+ " , "+str(slot_3up.y)  )
                                            if ret:
                                                return True
    #                                        print("diag line of 4 player")
                                            self.player_win()

                                            diag = True
                    except IndexError:
                        pass


            ## diagonal down
        for x in range(len(self.slots)-1):
            for y in range(len(self.slots[x])):
                slot = self.slots[x][y]
        #        if x == 0 and y > 5:
        #            print(str(x)+ " , " + str(y))
                if slot.occupied_by_computer == True or slot.occupied_by_player == True:
                    try:
        #                print(y)
                        if y-3 < len(self.slots[x])-1:
        #                    print("good one = "+str(x)+ " , " + str(y))
                            slot_up = self.slots[x+1][y+1]
                            slot_2up = self.slots[x+2][y+2]
                            slot_3up = self.slots[x+3][y+3]
                            if slot.occupied_by_computer == True:
    #                            print("diag line of 4   comp    aaaa    x, y = "+str(x)+ " , "+str(y))
                                if slot_up.occupied_by_computer == True:
    #                                print("diag line of 4   comp  bbbbbb   ")
                                    if slot_2up.occupied_by_computer == True:
    #                                    print("diag line of 4   comp     ccccc   ")
                                        if slot_3up.occupied_by_computer == True:
        #                                    print(" other diag line of 4 comp   starting with "+str(slot.x)+" , "+str(slot.y)  +" then "+ str(slot_up.x)+ " , "+str(slot_up.y)+" then "+ str(slot_2up.x)+ " , "+str(slot_2up.y)+" then "+ str(slot_3up.x)+ " , "+str(slot_3up.y) )
                                            if ret:
                                                return True
    #                                        print("diag line of 4   comp  ")
                                            self.computer_win()

                            if slot.occupied_by_player == True:
    #                            print("diag line of 4  p    aaaa  x, y = "+str(x)+ " , "+str(y))
                                if slot_up.occupied_by_player == True:
    #                                print("diag line of 4   p    bbbb ")
                                    if slot_2up.occupied_by_player == True:
    #                                    print("diag line of 4   p    ccccc ")
                                        if slot_3up.occupied_by_player == True:
        #                                    print("other   diag line of 4 player   starting with "+str(slot.x)+" , "+str(slot.y)  +" then "+ str(slot_up.x)+ " , "+str(slot_up.y)+" then "+ str(slot_2up.x)+ " , "+str(slot_2up.y)+" then "+ str(slot_3up.x)+ " , "+str(slot_3up.y) )
                                            if ret:
                                                return True
    #                                        print("diag line of 4 player")
                                            self.player_win()

                    except IndexError:
                        pass
        return False

    def check_for_box_of_4(self , ret=False):
        for x in range(len(self.slots)-1):
            for y in range(len(self.slots[x])-1):
                slot = self.slots[x][y]
                slot_right = self.slots[x+1][y]
                slot_up = self.slots[x][y+1]
                slot_top_right = self.slots[x+1][y+1]

                if slot.occupied_by_computer == True:
                    if slot_right.occupied_by_computer == True:
                        if slot_up.occupied_by_computer == True:
                            if slot_top_right.occupied_by_computer == True:
                                if ret:
                                    return True
                                self.computer_win()

                if slot.occupied_by_player == True:
                    if slot_right.occupied_by_player == True:
                        if slot_up.occupied_by_player == True:
                            if slot_top_right.occupied_by_player == True:
                                if ret:
                                    return True
                                self.player_win()
        if ret:
            return False

    def find_xy_which_wins_the_game(self):
        og_copy = copy.deepcopy(self.slots)
        for x in range(len(self.slots)):
            y = self.find_lowest_avaialable_y_at_this_x(x)
            if type(y) != type(True):
                y.occupied_by_computer = True
                m1 = self.check_for_box_of_4(True)
                m2 =self.check_for_line_of_4(True)
                y.occupied_by_computer = False
                if m1:
                    if m2:
                        return [x , y.y];
        return False


    def see_if_computer_loses_unless_it_blocks(self):
#        print("hello see_if_computer_loses_unless_it_blocks(self)")
        og_copy = copy.deepcopy(self.slots)
#        print("1")
        for x in range(len(self.slots)):
#            print("2")
            y = self.find_lowest_avaialable_y_at_this_x(x)
            if type(y) != type(True):
                if y.empty():
    #                print("3")
            #        print(str(y)+ "  y  ")
                    y.occupied_by_player = True
                    m1 = self.check_for_box_of_4(True)
                    m2 =self.check_for_line_of_4(True)
                    y.occupied_by_player = False
                    if m1:
    #                    print("4")
                        return [x , y.y];
                    if m2:
    #                    print("5")
                        return [x , y.y];
            else:
                pass  ### its fine
    #    print("6")
        return False

    def find_lowest_avaialable_y_at_this_x(self , x):
        lowest_y = False
       # x = int(x)
        for y in self.slots[x]:
            if y.occupied_by_computer == False and y.occupied_by_player == False:
                lowest_y = y
        return lowest_y;




    def check_if_player_has_line_of_3_or_box_of_3(self):
        self.check_for_box_of_3()

    def computer_choose_connecting_slot(self):
        places_to_make_connections = []
        for x in range(len(self.slots)-1):

            connected = False
            slot = self.find_lowest_avaialable_y_at_this_x(x)

            try:
                y = slot.y
                if slot.occupied_by_computer ==True:
        #        print(str(x)+" , "+str(y)+ "    =    ")

                    if self.slots[x][y+1].occupied_by_computer == True:
                        connected = True
                    if self.slots[x+1][y].occupied_by_computer == True:
                        connected = True
                    if self.slots[x-1][y].occupied_by_computer == True:
                        connected = True
                    if connected:
                        places_to_make_connections.append([x , y])
            except AttributeError:
                pass
        try:
            index = random.randint(0,len(places_to_make_connections)-1)
            p = places_to_make_connections[index]
            print(p)

        except ValueError:
            slot = self.computer_choose_random_slot()
#            print(" choosing connection")
            return [slot.x , slot.y]
        return p;

    def computer_choose_random_slot(self):
        worked = False
        while not worked:
            x = random.randint(0, self.x_rows-1)
            slot = self.find_lowest_avaialable_y_at_this_x(x)
            if slot != False:
                slot.occupied_by_computer = True
                worked = True
                return slot
    def computer_plays_turn(self , difficulty = 2):
        chooser = random.random()
        if difficulty == 1:
            if chooser > 0.25:
            #    print("computer_plays_turn 1")
                num_occupied_by_computer = 0
                for x in self.slots:
                    for y in x:
                        if y.occupied_by_computer:
                            num_occupied_by_computer+= 1
                if num_occupied_by_computer == 0:
        #            print("computer_plays_turn 2")
                    self.computer_choose_random_slot()
                else:
        #            print("computer_plays_turn 3")
                    self.computer_choose_connecting_slot()
            else:
        #        print("computer_plays_turn 4")
                self.computer_choose_random_slot()
        elif difficulty == 2:

            A = self.see_if_computer_loses_unless_it_blocks()
            if type(A)== type(True):
                if A == False:
                    if chooser > 0.25:
                        self.computer_choose_connecting_slot()
                    else:
                        self.computer_choose_random_slot()
                else:
                    raise Exception("  how   ?")
            else:
                self.slots[A[0]][A[1]].occupied_by_computer = True

        elif difficulty == 3:
            V = self.find_xy_which_wins_the_game()
            if type(V)== type(True):
                if V == False:
                    A = self.see_if_computer_loses_unless_it_blocks()
                    if type(A)== type(True):
                        if A == False:
                            if chooser > 0.25:
                                self.computer_choose_connecting_slot()
                            else:
                                self.computer_choose_random_slot()
                        else:
                            raise Exception("  how   ?")
                    else:
                        self.slots[A[0]][A[1]].occupied_by_computer = True
                else:
                    raise Exception("  how   ?")
            else:
                self.slots[V[0]][V[1]].occupied_by_computer = True
        else:
            raise Exception("  no such difficulty ")
    def draw(self , display ):
        display.fill(white)
        screen_width = 800
        screen_height = 600
        x_spacing = (screen_width*0.9)/self.x_rows
        y_spacing = (screen_height*0.9)/self.y_rows
   #     print('d')
        for x in range(len(self.slots)):
    #        print(x)
            x_point = (x+1) * x_spacing
            for y in range(len(self.slots[x])):
                y_point = (y+1) * y_spacing
           #     print(str(x_point)+ "  ,  "+ str(y_point)+ "     =====   ")
                if self.slots[x][y].occupied_by_player == False and self.slots[x][y].occupied_by_computer == False:
                    pygame.draw.rect(display, black,[x_point, y_point, 20, 20])
                elif self.slots[x][y].occupied_by_player == True and self.slots[x][y].occupied_by_computer == False:
                    pygame.draw.rect(display, green,[x_point, y_point, 20, 20])
                elif self.slots[x][y].occupied_by_player == False and self.slots[x][y].occupied_by_computer == True:
                    pygame.draw.rect(display, yellow,[x_point, y_point, 20, 20])
                else:
                    pygame.draw.rect(display, red,[x_point, y_point, 20, 20])

        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render("wins = "+str(self.player_score), False, (0, 0, 0))
        display.blit(text_surface, (40,10))
        text_surface = my_font.render("loses = "+str(self.computer_score), False, (0, 0, 0))
        display.blit(text_surface, (250,10))
        text_surface = my_font.render("draws = "+str(self.draw_count), False, (0, 0, 0))
        display.blit(text_surface, (450,10))


        pygame.display.update()

    def initialize_screen(self):
        screen_width = 800
        screen_height = 600
        display = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('connect 4')
        clock = pygame.time.Clock()
        return display , clock
    def human_plays_turn(self , x = None):
#        x = int(input(""))
        if x == None:
            x = mi_turns[self.turn_counter]
        self.turn_counter+= 1
        y = self.find_lowest_avaialable_y_at_this_x(x)
        if type(y) != type(True):
            self.slots[x][y.y].occupied_by_player = True
            return True
        return False;
    #    print("human just did = "+str(x)+ "     ,     "+ str(y.y))
      #  time.sleep(3)

    def check_for_win(self , ret = False):
        A = self.check_for_line_of_4(ret)
        B = self.check_for_box_of_4(ret)
        if ret:
            if A or B:
                return True
        return False

    def one_human_game(self):
        display = self.initialize_screen()
        while self.game_over == False:
            self.draw(display)
            self.human_plays_turn()
            self.draw(display)
    #        print("   total      ")
       #     for x in self.slots:
        #        for y in x:
         #           if y.occupied_by_player:
          #              print(str(y.x)+"  ,  "+str(y.y))

           # time.sleep(1)
            self.check_for_win()
            self.computer_plays_turn()
          #  time.sleep(1)
            self.check_for_win()

    def draw_reset(self):
        self.draw_count += 1
        self.new_game();

    def play_thinker_step(self, move_decided):

        worked = self.human_plays_turn(x = move_decided)
        if worked == False:
#            all_failed = self.completletley_full_check()
#            if all_failed:
#                self.end_round_with_no_winner()
#                print("draw")
#                return self.reward, True , ratio , True;
            self.reward+= - 0.001;
            if (self.player_score > 0 and  self.computer_score > 0):
                ratio = (self.player_score / self.computer_score)
            else:
                 ratio = 0
            all_failed = self.completletley_full_check()
            if all_failed:
                self.end_round_with_no_winner()
#                print("draw")
                return self.reward, True , ratio , True;

            return self.reward, False , ratio , worked;
#        print(" game over ")
        game_over = self.check_for_win(True)
#        print(" game over  2  ")
        if (self.player_score > 0 and  self.computer_score > 0):
            ratio = (self.player_score / self.computer_score)
        else:
             ratio = 0
        all_failed = self.completletley_full_check()
        if all_failed:
            self.end_round_with_no_winner()
            print("draw")
            return self.reward, True , ratio , True;
        return self.reward, game_over , ratio , worked;

#thegame = connect_4_game()
#thegame.one_human_game()


