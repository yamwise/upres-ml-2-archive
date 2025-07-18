import torch
import torch.nn as nn

# Load the 2x checkpoint
ckpt_2x = torch.load('/teamspace/studios/this_studio/neosr/experiments/train_plksr/models/net_g_165000.pth')
state_dict_2x = ckpt_2x['params'] if 'params' in ckpt_2x else ckpt_2x

# Create a new state dict for 3x model
state_dict_3x = {}

# Copy all weights except the final layer
for k, v in state_dict_2x.items():
    if 'feats.29' not in k:  # Skip the incompatible layer
        state_dict_3x[k] = v
        print(f"Copied: {k}")

# Save as a new checkpoint
new_ckpt = {'params': state_dict_3x}
torch.save(new_ckpt, 'plksr_2x_to_3x_init.pth')
print(f"\nSaved adapted checkpoint with {len(state_dict_3x)} parameters")