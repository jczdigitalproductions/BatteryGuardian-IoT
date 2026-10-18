# BatteryGuardian IoT — ExecuTorch Hackathon Starter
The Internet of Things (IoT) refers to a vast network of physical objects—such as vehicles, appliances, machinery, and wearable devices—that are embedded with sensors, software, and network connectivity to collect and share data. In this project, IoT is a Battery.

Offline battery anomaly demonstration for the **Arduino VENTUNO Q** (Qualcomm Dragonwing IQ8 / QCS8275 + STM32H5F5). Linux orchestrates simulated battery readings and optional PyTorch/ExecuTorch experiments; Arduino Bridge sends bounded status levels to an MCU LED.

> **Status:** Desktop simulation and unit tests are provided. No board execution, Arduino Bridge connectivity, QNN NPU delegation, battery fault validation, or hardware latency has been verified. This is a starter, **not** a production battery management system. The default app uses deterministic safety rules, **not ExecuTorch inference**. The included `.pte` exporter is optional and does not yet connect its inference to the live Bridge loop.

## Quick start (offline after dependencies installed)

```bash
python -m batteryguardian.app
python -m pytest -q
```

The output is JSONL. Levels: `0` normal, `1` warning, `2` critical. The same seven synthetic sensor records are replayed each time. No network requests or cloud API are used.

## Architecture

```text
Simulated readings (or future physical sensors)
       |                    [MCU sensor sampling not implemented]
Linux batteryguardian.app  --> deterministic safety_level()
       |                        optional synthetic PyTorch model (separate)
       +--> Arduino Bridge.call('set_alert_level', 0/1/2)
                       |
             STM32H5F5 MCU sketch
                       |
            Built-in LED / blink pattern
```

The MCU sketch rejects invalid alert levels, provides a communications timeout, and never switches power electronics. The Python process cannot downgrade a critical deterministic rule via an AI score. **For real batteries, the MCU must independently sample hardware sensors and enforce certified protection; this demonstration does not do so.**

## Train a tiny synthetic PyTorch model (optional)

```bash
python -m pip install -r requirements-dev.txt
python -m scripts.train
```

The generated labels are rules applied to random synthetic samples. Reported training accuracy is not a real-world validation result. No labeled physical fault dataset is included.

## Optional CPU ExecuTorch export (advanced)

After installing a **compatible** ExecuTorch Python checkout/environment, run:

```bash
python -m scripts.export_executorch
```

This writes `models/battery_cpu.pte` if your checkout supports the exporter API. It is **not** a QNN/Hexagon NPU artifact. This project does not claim the command was tested with the hackathon runtime. The stock `qnn_executor_runner` is not assumed to support this custom model's I/O without an explicit input-list and output decoding adapter. To complete integration: export with the board-supported QNN partitioner; prepare binary float32 input tensors in the exact exported shape; run with a compatible ARM64 runner; parse output; validate against PyTorch; then connect the inference result to `decide()` and the Bridge loop. Verify actual NPU delegation with exporter reports and board profiling before claiming acceleration.

## VENTUNO Q board setup

1. Follow the [official IoT guide](https://github.com/aaishikasb/qc-executorch-guide/blob/main/IoT/README.md) and [HackerSquad builder guide](https://hackersquad.io/events/executorch-hackathon-iot-track/resources).
2. Obtain the organizer's **board-supported image, Linux ARM64 runners, matching QNN/QAIRT libraries and model bundle**. These files are not supplied in this repository.
3. In Arduino App Lab, install/upload `arduino/BatteryGuardianBridge.ino` to the STM32H5F5. Check the actual built-in LED polarity and router UART mapping.
4. Check `systemctl status arduino-router` on Linux. Test the organizer's known-working LED Bridge example before running this project.
5. In the **Arduino App Lab Python environment**, use `scripts/app_lab_main.py` as the Python application entrypoint. It calls `App.run(user_loop=loop)` and uses the official `Bridge.call()` API. Ensure the `batteryguardian` package is available to that environment.
6. Start the sketch and App Lab Python app together. The MCU LED is off for normal, slow blink for warning, fast blink for critical, and very fast blink for missing updates. Hardware behavior is not yet tested. `python -m batteryguardian.app --bridge` is an advanced alternative only if your Bridge runtime has already been initialized.

**Note:** The current Python Bridge entrypoint is a scaffold; the App Lab lifecycle adapter must be confirmed on the board. The hackathon guide's `Bridge.call()` and `Bridge.provide_safe()` methods are used, not an invented transport.

## ExecuTorch smoke test on the board

```bash
export EXECUTORCH_ROOT="$HOME/executorch"
export MODEL_OUTPUT="$HOME/model_output"
export QNN_RUNNER="$EXECUTORCH_ROOT/cmake-out/examples/qualcomm/executor_runner/qnn_executor_runner"
uname -m
test -x "$QNN_RUNNER"
ldd "$QNN_RUNNER"
"$QNN_RUNNER" --help
mkdir -p "$MODEL_OUTPUT/add-run/outputs"
cd "$MODEL_OUTPUT/add-run"
"$QNN_RUNNER" --model_path "$MODEL_OUTPUT/add.pte"
```

This is a smoke test only. It does not prove accuracy, QNN delegation, or that the BatteryGuardian model ran.

## Verification matrix

| Capability | Status |
|---|---|
| Offline deterministic replay | Implemented; run locally |
| Unit tests | Included; run locally |
| Synthetic PyTorch training | Implemented; run with torch |
| CPU `.pte` export | Experimental; depends on ExecuTorch checkout |
| ExecuTorch runtime driving live alerts | Not implemented |
| Arduino Bridge LED handler | Sketch provided; board unverified |
| Linux App Lab Bridge lifecycle | `scripts/app_lab_main.py` provided; board unverified |
| Physical battery sensors | Not implemented |
| QNN/Hexagon NPU | Not implemented or verified |
| Real battery safety certification | Not applicable / not validated |

## Measurements to collect on actual hardware

Document the board image, `uname -m`, runtime versions, input/output accuracy against PyTorch, actual delegated operations, model-only latency (warm-up + multiple iterations), end-to-end sensor-to-LED latency, memory peak, thermals, and Wi-Fi-disabled replay. Record both successes and failures. Do not present simulation timing as physical sensor-to-action timing.

## Five-minute demo

1. Explain why local anomaly alerts matter.
2. Run `python -m batteryguardian.app` and show repeatable JSONL transitions.
3. On a working VENTUNO Q App Lab setup, show normal/off, warning/slow blink, critical/fast blink.
4. Show `add.pte` running in the board-supported ExecuTorch runner as a **separate** inference smoke test.
5. State clearly that integrating custom ExecuTorch inference into the LED path and NPU profiling are future work.

## Submission checklist

- [ ] Add actual team names and email addresses
- [ ] Confirm hackathon rules and final deadline with organizers
- [ ] Capture a real hardware demo video (do not represent simulation as hardware)
- [ ] Include verified board setup and measured performance
- [ ] Add GitHub repository URL and license
- [ ] Confirm whether custom ExecuTorch model integration is required for eligibility

## Limitations

This starter is intended for educational use. Synthetic labels are derived from thresholds and do not establish predictive health monitoring. No real battery should be connected without qualified electrical engineering review and independently enforced hardware protection.
