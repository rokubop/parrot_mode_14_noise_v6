# Parrot Mode v6 - 14 noises

**Parrot Mode v6 - 14 noises** is a mode where only noises are active, toggled on and off by one dedicated noise. Assumes a 14 noise parrot model with talon beta.

**While in command mode**
| Noise | Command |
|-------|---------|
| cluck | enable parrot mode |
| palatal click | repeat command |
| tut | undo repeat |

**While in parrot mode**
| Noise | Command | Noise | Command |
|-------|---------|-------|---------|
| mm    | click | pop  | click and disable parrot mode |
| hiss  | scroll down smooth | shush | scroll up smooth |
| ah    | mouse move left | oh    | mouse move right |
| guh   | mouse move down | t     | mouse move up |
| eh    | mouse to gaze   | ee    | stop all movement |
| er    | restore last mouse position | palate    | repeat command |
| cluck | disable parrot mode | tut \<noise> | 14+ more commands possible |

---

## Prerequisites

- Talon beta
- Parrot
- Your own trained parrot model with 14 noises
- parrot_config
- mouse_move_adv

## Installation

1. Download or clone this repository and its prerequisites into your Talon user directory.

    ```sh
    # mac and linux
    cd ~/.talon/user

    # windows
    cd ~/AppData/Roaming/talon/user

    git clone https://github.com/rokubop/roku-talon-shared.git
    git clone https://github.com/rokubop/parrot_mode_14_noise_v6.git
    ```

2. Update [parrot.talon](parrot.talon) to use your own noises
3. Update [parrot_mode.talon](parrot_mode.talon) to use your own noises
4. Update [parrot_mode.py](parrot_mode.py) to use your own noises and setup your own desired config. You can check out the [parrot_actions.py](parrot_actions.py) file available actions.