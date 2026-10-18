"""Deterministic sensor simulation and independent safety rules."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Sample:
    voltage: float
    current: float
    temperature: float

def simulated_samples():
    return [Sample(3.9, 0.7, 29), Sample(3.85, 0.8, 30), Sample(3.8, 1.0, 33), Sample(3.72, 1.4, 39), Sample(3.65, 2.0, 47), Sample(3.55, 2.5, 58), Sample(3.5, 2.8, 66)]

def safety_level(s: Sample) -> int:
    """Demo-only thresholds; not suitable for battery protection."""
    if s.temperature >= 60 or s.voltage < 3.0 or s.voltage > 4.25:
        return 2
    if s.temperature >= 45 or s.current >= 2.2:
        return 1
    return 0

def features(s: Sample):
    return [(s.voltage - 3.7) / 0.5, s.current / 3.0, (s.temperature - 25) / 50]

def decide(s: Sample, model_score: float | None):
    rule = safety_level(s)
    ai = 1 if model_score is not None and model_score >= 0.7 else 0
    return max(rule, ai)
