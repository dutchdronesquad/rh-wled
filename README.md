## Rotorhazard WLED plugin

This plugin makes it possible to control a matrix display with [WLED][wled], through the [RotorHazard][rotorhazard] events. Please note that this is still a rough draft and is still being worked on.

## Pre-requisites

- wled library installed in your venv (pip install wled)
- Python 3.11 or higher

Note: You need to use at least Python 3.11 or higher.

## LED behaviour

| Event | LED behaviour |
| ----- | ------------- |
| Start | Green |
| Stop | Red |
| Stage | Pulsing blue |
| Lap | Yellow |

### Development

To get started, you obviously need a working development environment from RotorHazard.

1. Fork / Clone the repository
2. Create a symlink to the wled_plugin folder in the RotorHazard plugin folder

```bash
ln -s ~/rh-wled-plugin/wled_plugin/ ~/RotorHazard/src/server/plugins/wled_plugin
```

3. Start or restart RotorHazard
4. Start developing 😄

## TODO

- Check if the plugin works on python 3.10 or lower

## License

Distributed under the **MIT** License. See [`LICENSE`](LICENSE) for more information.

<!-- LINKS -->
[wled]: https://github.com/Aircoookie/WLED
[RotorHazard]: https://github.com/RotorHazard/RotorHazard