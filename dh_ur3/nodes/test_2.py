import torch
import torch.nn as nn
from torch import optim
from torch.utils.data import DataLoader, random_split

model1 = torch.load('model_epoch_FT.pth')
model = torch.load('model_epoch_DP.pth')
torch.save(model.state_dict(), 'Test.pth')
model2 = torch.load('model_epoch_DP.pth')
model3 = torch.load('Test.pth')

print(model1.keys())
print(model3.keys())

for key, value in model1.items():
    if key == 'model1.0.weight' or key == 'model1.0.bias':
        model3[key] = value
        print(value)

torch.save(model3, 'model_pos.pth')