from typing import Optional
import torch
from torch import nn
from torch.nn.modules.utils import _pair
from .linear import Linear

class MLP(nn.Module):

    def __init__(self, in_channels: int, out_channels: Optional[int]=None, hidden_channels: Optional[int]=None, ratio: float=3.0, dropout: float | tuple[float, float]=0.0, **kwargs):
        super().__init__()
        out_channels = out_channels or in_channels
        hidden_channels = hidden_channels or int(ratio * in_channels)
        dropout = _pair(dropout)
        self.block = nn.Sequential(Linear(in_channels, hidden_channels, **kwargs), nn.GELU(), nn.Dropout(dropout[0]), Linear(hidden_channels, out_channels, **kwargs), nn.Dropout(dropout[1]))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)