<!-- Header -->
![alt Header of the WLED RH plugin](https://raw.githubusercontent.com/dutchdronesquad/rh-wled/main/assets/header_rh_wled-min.png)

<!-- PROJECT SHIELDS -->
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

## About

This plugin makes it possible to control a WS2812B [Matrix display][matrix_panel_ali] with [WLED][wled], through the [RotorHazard][rh] API events. Please note that this is still an alpha version.

## Pre-requisites

- This plugin only works with Python 3.11 or higher
- You must install the additional packages in your virtual environment (venv) that are listed in the [requirements.txt](./requirements.txt).

## LED behaviour

| Event | LED behaviour      |
| ----- | ------------------ |
| Start | Green              |
| Stop  | Red                |
| Stage | Pulsing blue       |
| Lap   | Pilot seat color   |

### Installation

1. Install the WLED RH Plugin like any other plugin ([RH Plugin Documentation][rh-plugin-docs])

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/dutchdronesquad/rh-wled/main/tools/install.sh)"
```

2. Install the extra PyPi packages from [requirements.txt](./requirements.txt)
3. Restart RotorHazard

### Development

To get started, you obviously need a working [development environment][rh_dev] from RotorHazard.

1. Fork / Clone the repository
2. Create a symlink to the `wled` folder in the RotorHazard plugin folder

```bash
ln -s ~/rh-wled/wled/ ~/RotorHazard/src/server/plugins/wled
```

3. Start or restart RotorHazard

```bash
sudo systemctl restart rotorhazard.service
```
4. Start developing 😄

## License

Distributed under the **MIT** License. See [`LICENSE`](LICENSE) for more information.

<!-- LINKS -->
[wled]: https://github.com/Aircoookie/WLED
[rh]: https://github.com/RotorHazard/RotorHazard
[rh_dev]: https://github.com/RotorHazard/RotorHazard/blob/main/doc/Development.md

[matrix_panel_ali]: https://tc.tradetracker.net/?c=15640&m=12&a=417111&r=&u=https%3A%2F%2Faliexpress.com%2Fitem%2F32944813367.html

[license-shield]: https://img.shields.io/github/license/dutchdronesquad/rh-wled.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2024.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg