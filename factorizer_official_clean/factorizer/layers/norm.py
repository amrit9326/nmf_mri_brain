import torch
from torch import nn

class LayerNorm(nn.Module):

    def __init__(self, dim: int, **kwargs):
        super(LayerNorm, self).__init__()
        self.norm = nn.LayerNorm(dim, **kwargs)

    def forward(self, x):
        out = torch.einsum('b c ... -> b ... c', x)
        out = self.norm(out)
        out = torch.einsum('b ... c -> b c ...', out)
        return out