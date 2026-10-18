"""Optional CPU ExecuTorch export. QNN delegation requires a compatible board SDK."""
import argparse
from pathlib import Path
import torch
from batteryguardian.model import AnomalyNet

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--weights', default='models/battery_synthetic.pt')
    p.add_argument('--output', default='models/battery_cpu.pte')
    args = p.parse_args()
    from executorch.exir import to_edge_transform_and_lower
    model = AnomalyNet().eval()
    model.load_state_dict(torch.load(args.weights, map_location='cpu', weights_only=True))
    example = (torch.zeros(1, 3),)
    exported = torch.export.export(model, example)
    program = to_edge_transform_and_lower(exported).to_executorch()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(program.buffer)
    print(f'Wrote CPU ExecuTorch program: {output}; no QNN delegation claimed')

if __name__ == '__main__':
    main()
