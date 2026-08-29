import math
import torch
from torch import nn
from .linear import Linear
from ..utils.helpers import as_tuple, partialize

class DoubleConv(nn.Module):

    def __init__(self, in_channels, out_channels, mid_channels=None, conv=(nn.Conv3d, {'kernel_size': 3, 'padding': 1}), norm=(nn.GroupNorm, (8,)), act=nn.LeakyReLU, drop=(nn.Dropout, {'p': 0.0}), stride=1, **kwargs):
        super().__init__()
        mid_channels = out_channels if mid_channels is None else mid_channels
        conv = partialize(conv)
        drop = partialize(drop)
        norm = partialize(norm)
        act = partialize(act)
        self.block1 = nn.Sequential(conv(in_channels, mid_channels, stride=stride), drop(), norm(mid_channels), act())
        self.block2 = nn.Sequential(conv(mid_channels, out_channels, stride=1), drop(), norm(out_channels), act())

    def forward(self, x):
        out = self.block1(x)
        out = self.block2(out)
        return out

class BasicBlock(nn.Module):

    def __init__(self, in_channels, out_channels, mid_channels=None, conv=(nn.Conv3d, {'kernel_size': 3, 'padding': 1}), norm=(nn.GroupNorm, (8,)), act=nn.LeakyReLU, drop=(nn.Dropout, {'p': 0.0}), stride=1, **kwargs):
        super().__init__()
        mid_channels = out_channels if mid_channels is None else mid_channels
        conv1 = partialize(conv)
        conv2 = partialize(conv)
        drop = partialize(drop)
        norm = partialize(norm)
        act = partialize(act)
        self.conv1 = conv1(in_channels, mid_channels, stride=stride)
        self.drop1 = drop()
        self.norm1 = norm(mid_channels)
        self.conv2 = conv2(mid_channels, out_channels)
        self.drop2 = drop()
        self.norm2 = norm(out_channels)
        self.act = act()
        if math.prod(as_tuple(stride)) != 1 or in_channels != out_channels:
            conv = self.conv1.__class__
            self.shortcut = conv(in_channels, out_channels, kernel_size=1, stride=stride, bias=False)
        else:
            self.shortcut = nn.Identity()

    def forward(self, x):
        shortcut = self.shortcut(x)
        out = self.conv1(x)
        out = self.drop1(out)
        out = self.norm1(out)
        out = self.act(out)
        out = self.conv2(out)
        out = self.drop2(out)
        out = self.norm2(out)
        out = out + shortcut
        out = self.act(out)
        return out

class PreActivationBlock(nn.Module):

    def __init__(self, in_channels, out_channels, mid_channels=None, conv=(nn.Conv3d, {'kernel_size': 3, 'padding': 1}), norm=(nn.GroupNorm, (8,)), act=nn.LeakyReLU, drop=(nn.Dropout, {'p': 0.0}), stride=1, **kwargs):
        super().__init__()
        mid_channels = out_channels if mid_channels is None else mid_channels
        conv1 = partialize(conv)
        conv2 = partialize(conv)
        drop = partialize(drop)
        norm = partialize(norm)
        act = partialize(act)
        self.norm1 = norm(in_channels)
        self.act = act()
        self.conv1 = conv1(in_channels, mid_channels, stride=stride)
        self.drop1 = drop()
        self.norm2 = norm(mid_channels)
        self.conv2 = conv2(mid_channels, out_channels)
        self.drop2 = drop()
        if math.prod(as_tuple(stride)) != 1 or in_channels != out_channels:
            conv = self.conv1.__class__
            self.shortcut = conv(in_channels, out_channels, kernel_size=1, stride=stride, bias=False)

    def forward(self, x):
        out = self.norm1(x)
        out = self.act(out)
        shortcut = self.shortcut(out) if hasattr(self, 'shortcut') else x
        out = self.conv1(out)
        out = self.drop1(out)
        out = self.norm2(out)
        out = self.act(out)
        out = self.conv2(out)
        out = self.drop2(out)
        out = out + shortcut
        return out

class SepConv(nn.Module):

    def __init__(self, in_channels, out_channels=None, hidden_channels=None, ratio=2, spatial_dims=3, act=nn.GELU, kernel_size=5, stride=1, padding=2, dilation=1, bias=True, padding_mode='zeros', device=None, dtype=None, **kwargs):
        super().__init__()
        out_channels = in_channels if out_channels is None else out_channels
        hidden_channels = int(ratio * in_channels) if hidden_channels is None else hidden_channels
        conv = getattr(nn, f'Conv{spatial_dims}d')
        act = partialize(act)
        self.pwconv1 = Linear(in_channels, hidden_channels, bias=False)
        self.act = act()
        self.dwconv = conv(hidden_channels, hidden_channels, kernel_size=kernel_size, groups=hidden_channels, stride=stride, padding=padding, dilation=dilation, bias=bias, padding_mode=padding_mode, device=device, dtype=dtype)
        self.pwconv2 = Linear(hidden_channels, out_channels)

    def forward(self, x):
        out = self.pwconv1(x)
        out = self.act(out)
        out = self.dwconv(out)
        out = self.pwconv2(out)
        return out