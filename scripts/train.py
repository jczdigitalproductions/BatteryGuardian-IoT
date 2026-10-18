"""Train on synthetic labels; not evidence of real battery fault performance."""
import argparse
from pathlib import Path
import torch
from batteryguardian.model import AnomalyNet

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='models/battery_synthetic.pt')
    args = p.parse_args()
    torch.manual_seed(17)
    n = 3000
    v = 2.8 + torch.rand(n, 1) * 1.6
    c = torch.rand(n, 1) * 3.5
    t = 20 + torch.rand(n, 1) * 55
    x = torch.cat(((v - 3.7)/0.5, c/3, (t-25)/50), dim=1)
    y = ((t >= 45) | (c >= 2.2) | (v < 3.0) | (v > 4.25)).float()
    model = AnomalyNet()
    opt = torch.optim.Adam(model.parameters(), lr=0.015)
    for _ in range(180):
        opt.zero_grad()
        loss = torch.nn.functional.binary_cross_entropy(model(x), y)
        loss.backward()
        opt.step()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), out)
    with torch.no_grad():
        pred = model(x).ge(0.5)
        print(f'synthetic training accuracy: {(pred == y.bool()).float().mean().item():.3f}; not validation')
    print(f'Saved {out}')

if __name__ == '__main__':
    main()
