from typing import Optional, Sequence
import re
from functools import reduce
import torch
from torch import Tensor
import torch.nn.functional as F
from torch import nn
from torch.nn.modules.utils import _ntuple
from einops.layers.torch import Rearrange

def dot(x: Tensor, y: Tensor) -> Tensor:
    return torch.einsum('...mn,...mn->...', x, y).unsqueeze(-1)

def norm2(x: Tensor, w: Optional[Tensor]=None) -> Tensor:
    y = x.flatten(1).square()
    if w is not None:
        w = w.flatten(1)
        y *= w
    return torch.sqrt(torch.sum(y, dim=1))

def softmax(x: torch.Tensor, dim: int | Sequence[int]) -> torch.Tensor:
    dims = [dim] if isinstance(dim, int) else dim
    dims = [d if d >= 0 else x.ndim + d for d in dims]
    if len(dims) == 1:
        return F.softmax(x, dim=dims[0])
    non_target_dims = [d for d in range(x.ndim) if d not in dims]
    perm = non_target_dims + dims
    inverse_perm = [0] * x.ndim
    for i, p in enumerate(perm):
        inverse_perm[p] = i
    x_permuted = x.permute(perm)
    start_dim = len(non_target_dims)
    flattened = x_permuted.flatten(start_dim=start_dim)
    return F.softmax(flattened, dim=start_dim).view(x_permuted.shape).permute(inverse_perm)

def relative_error(x: Tensor, y: Tensor, w: Optional[Tensor]=None, eps: float=1e-16) -> Tensor:
    numerator = norm2(x - y, w) + eps
    denominator = norm2(x, w) + eps
    return numerator / denominator

def kl_divergence(x: Tensor, y: Tensor, eps: float=1e-16):
    x = x.clamp(min=eps)
    y = y.clamp(min=eps)
    kl_div = (x * torch.log(x / y) - x + y).flatten(1).mean(-1)
    return kl_div

class Reshape(nn.Module):

    def __init__(self, input_size: Sequence[int], equation: Optional[str]=None, shifts: Optional[Sequence[int]]=None, dims: Optional[Sequence[int]]=None, **kwargs) -> None:
        super().__init__()
        self.input_size = input_size
        if equation is None:
            self.rearrange = nn.Identity()
            self.rearrange_inv = nn.Identity()
            self.output_size = input_size
        else:
            self.equation = equation
            left, right = equation.split('->')
            self.left = left = left.rstrip().lstrip()
            self.right = right = right.rstrip().lstrip()
            self.rearrange = Rearrange(equation, **kwargs)
            self.dim_lengths = self.infer_dims(self.left, input_size, kwargs)
            self.output_size = self.compute_size(self.right, self.dim_lengths)
            self.equation_inv = equation_inv = ' -> '.join([right, left])
            self.rearrange_inv = Rearrange(equation_inv, **self.dim_lengths)
        if shifts is not None:
            self.shifts = shifts
            self.shifts_inv = tuple((-s for s in self.shifts))
            self.dims = dims

    @staticmethod
    def infer_dims(pattern: str, size: Sequence[int | None], dim_lengths: dict[str, int]) -> dict[str, int | None]:
        groups = re.findall('\\(([^)]+)\\)|(\\w+)', pattern)
        inferred_dims = {}
        for group, s in zip(groups, size):
            dims = group[0].split() if group[0] else [group[1]]
            if s is None or len([d for d in dims if d in dim_lengths]) < len(dims) - 1:
                for d in dims:
                    if d in dim_lengths:
                        inferred_dims[d] = dim_lengths[d]
                continue
            known_product = reduce(lambda x, y: x * y, (dim_lengths[d] for d in dims if d in dim_lengths), 1)
            unknown_dim = s // known_product
            for d in dims:
                inferred_dims[d] = dim_lengths.get(d, unknown_dim)
        return inferred_dims

    @staticmethod
    def compute_size(pattern: str, dim_lengths: dict[str, int]) -> Sequence[int | None]:
        groups = re.findall('\\(([^)]+)\\)|(\\w+)', pattern)
        sizes = []
        for group in groups:
            dims = group[0].split() if group[0] else [group[1]]
            if any((d not in dim_lengths for d in dims)):
                sizes.append(None)
            else:
                group_size = reduce(lambda x, y: x * y, (dim_lengths[d] for d in dims))
                sizes.append(group_size)
        return tuple(sizes)

    def forward(self, x: Tensor) -> Tensor:
        if hasattr(self, 'shifts'):
            x = torch.roll(x, self.shifts, self.dims)
        out = self.rearrange(x)
        return out

    def inverse_forward(self, x: Tensor) -> Tensor:
        out = self.rearrange_inv(x)
        if hasattr(self, 'shifts'):
            out = torch.roll(out, self.shifts_inv, self.dims)
        return out

class Matricize(Reshape):

    def __init__(self, input_size: Sequence[int], num_heads: Optional[int]=None, head_dim: Optional[int]=None, grid_size: Optional[int | Sequence[int]]=None, patch_size: Optional[int | Sequence[int]]=None, shifts: Optional[int | Sequence[int]]=None, **kwargs) -> None:
        assert (num_heads, head_dim) != (None, None), "'num_heads' or 'head_dim' must be specified."
        assert (grid_size, patch_size) != (None, None), "'grid_size' or 'kernel_size' must be specified."
        spatial_dim = len(input_size) - 2
        to_ntuple = _ntuple(spatial_dim)
        left = f"b (h d) {' '.join([f'(g{i} p{i})' for i in range(spatial_dim)])}"
        right = '(b h) '
        right += f"({' '.join([f'g{i}' for i in range(spatial_dim)])}) "
        right += f"d ({' '.join([f'p{i}' for i in range(spatial_dim)])})"
        equation = f'{left} -> {right}'
        dims_lengths = {}
        if num_heads is not None:
            dims_lengths['h'] = max(num_heads, 1)
        if head_dim is not None:
            dims_lengths['d'] = max(head_dim, 1)
        for j, g in enumerate(to_ntuple(grid_size)):
            if g is not None:
                dims_lengths[f'g{j}'] = max(g, 1)
        for j, p in enumerate(to_ntuple(patch_size)):
            if p is not None:
                dims_lengths[f'p{j}'] = max(p, 1)
        if shifts is not None:
            dims = tuple((j + 2 for j in range(spatial_dim)))
            shifts = to_ntuple(shifts)
        else:
            dims = None
        super().__init__(input_size, equation=equation, shifts=shifts, dims=dims, **dims_lengths, **kwargs)

class SWMatricize(nn.Module):

    def __init__(self, input_size: Sequence[int], num_heads: Optional[int]=None, head_dim: Optional[int]=None, grid_size: Optional[int | Sequence[int]]=None, patch_size: Optional[int | Sequence[int]]=None, shifts: Optional[Sequence[None | int | Sequence[int]]]=None, **kwargs) -> None:
        super().__init__()
        spatial_dim = len(input_size) - 2
        to_ntuple = _ntuple(spatial_dim)
        patch_size = to_ntuple(patch_size)
        grid_size = to_ntuple(grid_size)
        if shifts is None:
            shifts = [None, tuple((s // 2 for s in patch_size))]
        shifted_windows = []
        for s in shifts:
            shifted_windows.append(Matricize(input_size, num_heads=num_heads, head_dim=head_dim, grid_size=grid_size, patch_size=patch_size, shifts=s, **kwargs))
        self.shifted_windows = nn.ModuleList(shifted_windows)
        self.output_size = self.shifted_windows[0].output_size

    def forward(self, x: Tensor) -> Tensor:
        out = []
        for shifted_window in self.shifted_windows:
            out.append(shifted_window(x))
        return torch.cat(out)

    def inverse_forward(self, x: Tensor) -> Tensor:
        b = x.shape[0]
        num_shifts = len(self.shifted_windows)
        out = 0.0
        for j in range(num_shifts):
            slc = slice(j * (b // num_shifts), (j + 1) * (b // num_shifts))
            z = x[None, slc, ...][0]
            out = out + self.shifted_windows[j].inverse_forward(z)
        out = out / num_shifts
        return out