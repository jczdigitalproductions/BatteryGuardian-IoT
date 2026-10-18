"""Arduino App Lab entrypoint: run inside its supported Python application environment."""
from arduino.app_utils import App, Bridge
from batteryguardian.core import simulated_samples, decide

samples = simulated_samples()
index = 0

def loop():
    global index
    import json
    import time
    sample = samples[index % len(samples)]
    level = decide(sample, None)
    Bridge.call('set_alert_level', level)
    print(json.dumps({'sample': index, 'level': level, 'voltage': sample.voltage,
                      'current': sample.current, 'temperature': sample.temperature}), flush=True)
    index += 1
    time.sleep(0.5)

App.run(user_loop=loop)
