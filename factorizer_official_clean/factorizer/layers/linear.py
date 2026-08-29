from typing import Optional
import torch
from torch import nn

class Linear(nn.Module):

    def __init__(self, in_channels: int, out_channels: int, bias: bool=True, device: Optional[torch.device]=None, dtype: Optional[torch.dtype]=None):
        super().__init__()
        self.flatten = nn.Flatten(start_dim=2)
        self.linear = nn.Conv1d(in_channels, out_channels, kernel_size=1, bias=bias, device=device, dtype=dtype)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        original_shape = x.shape
        x = self.flatten(x)
        x = self.linear(x)
        x = x.view(original_shape[0], -1, *original_shape[2:])
        return x