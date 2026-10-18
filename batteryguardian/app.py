"""Offline repeatable simulation; optional hardware bridge and ExecuTorch runner."""
import argparse
import json
import time
from .core import simulated_samples, features, decide


def run(bridge=False, scorer=None, delay=0):
    if bridge:
        from arduino.app_utils import Bridge
    for index, sample in enumerate(simulated_samples()):
        started = time.perf_counter()
        score = scorer(features(sample)) if scorer else None
        level = decide(sample, score)
        if bridge:
            Bridge.call('set_alert_level', level)
        record = {'index': index, 'voltage_v': sample.voltage, 'current_a': sample.current,
                  'temperature_c': sample.temperature, 'anomaly_score': score,
                  'level': level, 'mode': 'bridge' if bridge else 'simulation',
                  'elapsed_ms': round((time.perf_counter()-started)*1000, 3)}
        print(json.dumps(record), flush=True)
        if delay:
            time.sleep(delay)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bridge', action='store_true', help='Send alert level to Arduino Bridge (board only)')
    parser.add_argument('--delay', type=float, default=0)
    args = parser.parse_args()
    run(bridge=args.bridge, delay=args.delay)

if __name__ == '__main__':
    main()
