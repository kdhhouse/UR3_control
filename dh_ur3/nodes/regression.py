import os
import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import DataLoader, random_split
import pandas as pd

import numpy as np

from network import Regression
from data_load import DatasetLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

lr1 = 0.001
lr2 = 0.0005
lr3 = 0.00001
beta1 = 0.5
beta2 = 0.99
epochs = 201
input_dir = "Type3_15_train_900.csv"
test_dir = "Type3_15_test_rand.csv"
num = 1000
batch_size = 5


def train():

    print("data loading")
    dataset = DatasetLoader(input_dir, num)
    testset = DatasetLoader(test_dir, num)
    train_loader = DataLoader(
        dataset, batch_size=batch_size, shuffle=True, num_workers=8, pin_memory=True
    )
    test_loader = DataLoader(
        testset, batch_size=batch_size, shuffle=True, num_workers=8, pin_memory=True
    )
    model = Regression().to(device=device)

    criterionMSE = nn.MSELoss().to(device)

    optimizer1 = optim.Adam(model.parameters(), lr1, [beta1, beta2])
    optimizer2 = optim.Adam(model.parameters(), lr2, [beta1, beta2])
    optimizer3 = optim.Adam(model.parameters(), lr3, [beta1, beta2])
    loss_list_epoch = np.zeros((2,0))
    for epoch in range(epochs):
        print("epoch: ", epoch)
        loss_list = []
        output_data = []
        loss_list_test = []
        output_data_test = []
        for sample in train_loader:
            input_data = sample["input_data"].to(device=device)
            label_data = sample["label_data"].to(device=device)


            output = model(input_data)
            loss = criterionMSE(output, label_data)
            output_data.append(output)

            if np.mean(np.array(loss_list)) > 1:
                optimizer1.zero_grad()
                loss.backward()
                optimizer1.step()
            elif 1 >= np.mean(np.array(loss_list)) > 0.1:
                optimizer2.zero_grad()
                loss.backward()
                optimizer2.step()
            else:
                optimizer3.zero_grad()
                loss.backward()
                optimizer3.step()

            loss_list.append(loss.item())
        for sample in test_loader:
            input_data_test = sample["input_data"].to(device=device)
            label_data_test = sample["label_data"].to(device=device)


            output_test = model(input_data_test)
            loss_test = criterionMSE(output_test, label_data_test)
            output_data_test.append(output_test)


            loss_list_test.append(loss_test.item())

        if epoch % 20 == 0:
            if not os.path.exists("checkpoint"):
                os.mkdir("checkpoint")
            if not os.path.exists(os.path.join("checkpoint", "result")):
                os.mkdir(os.path.join("checkpoint", "result"))
            net_g_model_out_path = "checkpoint/{}/model_epoch_{}.pth".format(
                "result", epoch
            )
            torch.save(model.state_dict(), net_g_model_out_path)

            print("Checkpoint saved to {}".format("checkpoint" + "result"))
        print(np.mean(np.array(loss_list)),np.mean(np.array(loss_list_test)))
        loss_list_epoch = np.append(loss_list_epoch, [[np.mean(np.array(loss_list))], [np.mean(np.array(loss_list_test))]], 1)
    print(loss_list_epoch)
    df = pd.DataFrame(loss_list_epoch)
    df.to_csv('regression_test.csv', index=False)
if __name__ == "__main__":
    train()
