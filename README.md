# W3C WoT Integration

This integration allows devices conforming to W3C WoT to be integrated with Home Assistant

> This integration is pre-alpha, using it in production is not-advised

### Installation

Copy this folder to `<config_dir>/custom_components/wot/`.

Add the following entry in your `configuration.yaml`:

```yaml
light:
  - platform: wot
    td: URL_TO_DEVICE_TD
  
```
