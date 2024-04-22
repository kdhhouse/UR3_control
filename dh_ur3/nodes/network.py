import torch
import torch.nn as nn


class Regression(nn.Module):
    def __init__(self):
        super(Regression, self).__init__()
        self.model1 = nn.Sequential(
            nn.Linear(6, 6), nn.Tanh(),
        )
        self.model2 = nn.Sequential(
            nn.Linear(6, 100), nn.Tanh(),
            nn.Linear(100, 6)
        )


    def forward(self, x):
        result = self.model1(x)
        result = self.model2(result)
        return result
