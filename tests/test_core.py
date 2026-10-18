from batteryguardian.core import Sample, safety_level, decide, simulated_samples

def test_normal():
    assert safety_level(Sample(3.8, 1.0, 30)) == 0

def test_warning():
    assert safety_level(Sample(3.8, 1.0, 47)) == 1

def test_critical():
    assert safety_level(Sample(3.8, 1.0, 65)) == 2

def test_ai_cannot_downgrade_rule():
    assert decide(Sample(3.8, 1.0, 65), 0.01) == 2

def test_repeatable():
    assert simulated_samples() == simulated_samples()
