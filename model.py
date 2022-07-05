import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

###     self.model = Linear_QNet(3 * self.game.y_rows * self.game.x_rows, 6 * self.game.y_rows * self.game.x_rows,self.game.x_rows)#### input len = area of game board x 3
class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
    def forward(self , x):
        first_hidden_output = self.linear1(x)
        prev_rectified = F.relu(first_hidden_output)
        output = self.linear2(prev_rectified)
        return output

    def save(self, file_name = 'model.pth'):
        torh.save(self.state_dict() , file_name)

class Linear_QNet_extra_layers(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear1_5 = nn.Linear(hidden_size, hidden_size*2)
        self.linear1_6 = nn.Linear(hidden_size*2, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)
    def forward(self , x):
        first_hidden_output = self.linear1(x)
        prev_rectified = F.relu(first_hidden_output)
        second_hidden_output = self.linear1_5(prev_rectified)
        second_rectified = F.relu(second_hidden_output)
        third_hidden_output = self.linear1_6(second_rectified)
        prev_rectified = F.relu(third_hidden_output)
        output = self.linear2(prev_rectified)
        return output

    def save(self, file_name = 'model.pth'):
        torh.save(self.state_dict() , file_name)

class QTrainer:
    def __init__(self, model , lr , gama):
        self.lr = lr
        self.gamma = gama
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state_old, action, reward, state_new, game_over , all_failed):

        if all_failed == False:
    #        print(str(state_old)+ " = old state ")
    #        print(str(action) + " = action ")
    #        print(str(reward)+ " = reward ")
    #        print(str(state_new)+ " = new state ")
    #        print(str(game_over)+ " = game_over ")
            state_old, state_new, action, reward = torch.tensor(state_old, dtype = torch.float) , torch.tensor( state_new , dtype = torch.float) , torch.tensor(action, dtype = torch.float) , torch.tensor(reward, dtype = torch.float) ,

            if len(state_old.shape) == 1:
                state_old = torch.unsqueeze(state_old, 0)
                state_new = torch.unsqueeze(state_new, 0)
                reward = torch.unsqueeze(reward, 0)
                action = torch.unsqueeze(action, 0)
                game_over = (game_over,)

            #Q = model dot predict(state0)
            #Q new = R+gamma dot maz(Q(state1))

            # predict q value with current state
            pred = self.model(state_old)

            # r + gama * max(next predicted q )
            target = pred.clone()
        #    print(target)
            for idx in range(len(game_over)):
        #        for r in reward:
        #            print(str(idx) + "     =  ")
        #            print(str(r))
                    #print(str(r[idx]))
                Q_new = reward[idx]
                if not game_over[idx]:
                    Q_new = reward[idx]+ self.gamma * torch.max(self.model(state_new[idx]))
        #        print(str(idx)+ "      idx    this is the idx init     ")
        #        print(torch.argmax(action).item())
        #        for t in target[idx]:
        #            print(t)
                target[idx][torch.argmax(action).item()] = Q_new


            self.optimizer.zero_grad()
            loss = self.criterion(target, pred)
            self.optimizer.step()
