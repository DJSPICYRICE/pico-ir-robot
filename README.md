# Pico W IR Remote-Control Robot

A two-wheel mobile robot driven by a **Raspberry Pi Pico W** running MicroPython. It's steered with an infrared remote, has blinking turn signals and hazard lights, and uses an ultrasonic sensor to stop itself before hitting obstacles.

Final project for **CMPEH 472** (Penn State Harrisburg), Fall 2025 — by Mouli Grandhi and Michael Zimmerman.

## Features

- **IR remote control** — forward, reverse, left, right, stop (NEC protocol)
- **Turn signals** — yellow LEDs blink on the side you're turning
- **Hazard lights** — red LEDs blink while reversing
- **Collision avoidance** — HC-SR04 stops the robot when something is within 10 cm; forward and turns stay blocked until you back up
- **Motor balancing** — PWM duty cycles trim the two motors so the robot drives straight

## Hardware

- Raspberry Pi Pico W
- 2× DC motors + motor driver module
- IR remote + IR receiver
- HC-SR04 ultrasonic sensor
- 2× red LEDs, 2× yellow LEDs, 330 Ω resistors
- Switch, small breadboard, AA battery pack
- Chassis parts from the Raspberry Pi Pico Advanced Kit

## Pin map

| Function | GPIO |
|---|---|
| Left motor forward | 10 |
| Left motor backward | 11 |
| Right motor backward | 12 |
| Right motor forward | 13 |
| IR receiver | 20 |
| Left turn LED (yellow) | 0 |
| Left stop/hazard LED (red) | 1 |
| Right turn LED (yellow) | 2 |
| Right stop/hazard LED (red) | 4 |
| Ultrasonic trigger | 6 |
| Ultrasonic echo | 7 |

## Remote buttons

| Button | Code | Action |
|---|---|---|
| Up | `0x18` | Forward |
| Down | `0x52` | Reverse (clears obstacle stop) |
| Left | `0x08` | Turn left |
| Right | `0x5A` | Turn right |
| OK | `0x1C` | Stop |

## Repo layout

```
src/
  lab13_motor_test.py   # Lab 13: basic motor direction test
  lab14_ir_control.py   # Lab 14: IR remote + PWM motor balancing
  main.py               # Lab 15: final robot (lights + ultrasonic stop)
lib/README.md           # Third-party libraries to install
docs/CMPEH_472_final_report.pdf
```

## Setup

1. Flash MicroPython onto the Pico W.
2. Copy the libraries listed in [`lib/README.md`](lib/README.md) onto the Pico.
3. Copy `src/main.py` to the Pico root so it runs on boot (Thonny or `mpremote cp src/main.py :main.py`).
4. Power up and drive.

## Development notes

- **Lab 13:** Built the chassis and wrote the basic drive functions.
- **Lab 14:** Got IR decoding working with Peter Hinch's `micropython_ir` driver. PWM speed control turned out to be impractical — the bottom ~70–80% of the duty range couldn't reliably turn the motors.
- **Lab 15:** Added turn signals, hazards, and the ultrasonic stop. PWM was repurposed to balance motor speeds instead of variable speed.

See the [full report](docs/CMPEH_472_final_report.pdf) for details.

## License

[MIT](LICENSE)
