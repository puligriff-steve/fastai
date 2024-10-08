"""Train models faster using channels last format (beta)"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/18c_callback.channelslast.ipynb.

# %% ../../nbs/18c_callback.channelslast.ipynb 1
from __future__ import annotations
from ..basics import *
from .fp16 import AMPMode, MixedPrecision

from torch.cuda.amp import GradScaler

# %% auto 0
__all__ = ['ChannelsLast']

# %% ../../nbs/18c_callback.channelslast.ipynb 7
class ChannelsLast(Callback):
    "Channels last training using PyTorch's Channels Last Memory Format (beta)"
    order = -1 # Needs to run before any model modification callbacks occur
    def before_fit(self):
        self.learn.model.to(memory_format=torch.channels_last)

# %% ../../nbs/18c_callback.channelslast.ipynb 9
@patch
@delegates(GradScaler)
def to_channelslast(self:Learner,
    use_amp:bool=True, # Add `MixedPrecision` with `amp_mode`. Recommended for full channels last performance
    amp_mode:str|AMPMode=AMPMode.FP16, # Mixed Precision training mode. Supports fp16 and bf16.
    **kwargs
):
    "Set `Learner` and inputs to `channels_last` format and float16 Mixed Precision by default"
    if use_amp and not hasattr(self, 'mixed_precision') and not hasattr(self, 'channels_last'):
        return self.add_cbs([ChannelsLast(), MixedPrecision(amp_mode, **kwargs)])
    elif not hasattr(self, 'channels_last'):
        return self.add_cb(ChannelsLast())

# %% ../../nbs/18c_callback.channelslast.ipynb 10
@patch
def to_contiguous(self:Learner, to_fp32:bool=False):
    "Set `Learner` and inputs to `contiguous_format` (default format), optionally to single precision"
    self.model.to(memory_format=torch.contiguous_format)
    if to_fp32:
        return self.remove_cbs([ChannelsLast, MixedPrecision])
    else:
        return self.remove_cb(ChannelsLast)
