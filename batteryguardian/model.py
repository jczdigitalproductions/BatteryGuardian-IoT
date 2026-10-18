"""Tiny PyTorch classifier used only for a synthetic demonstration."""
import torch
from torch import nn

class AnomalyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(3, 12), nn.ReLU(), nn.Linear(12, 1))

    def forward(self, x):
        return torch.sigmoid(self.net(x))
