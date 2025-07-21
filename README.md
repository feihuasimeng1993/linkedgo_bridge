
# Linkedgo Bridge Integration for Home Assistant

[English](./README.md) | [简体中文](./README_zh.md)

<p align="left">
  <img src="https://omo-oss-image.thefastimg.com/portal-saas/pg2024022210453839417/cms/image/314152a9-c7a1-4082-8a0e-d7e5c7f81df9.png_186xaf.png" alt="linkedgo" title="linkedgo" la="la">
</p>

Linekdgo Bridge Integration is officially supported by linkedgo company. It allows you to control your linkedgo devices in Home Assistant. Currently, it has already supported thomerstate (ST830, ST1800HN, ST2000).

## Installation

> Home Assistant version requirement:
>
> - Core $\geq$ 2024.4.4
> - Operating System $\geq$ 13.0


### Method: [HACS](https://hacs.xyz/)

One-click installation from HACS:

[![Open your Home Assistant instance and open the Linkedgo Bridge integration inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Linkedgo&repository=linkedgo_bridge&category=integration)

Or, HACS > In the search box, type **Linkedgo Bridge** > Click **Linkedgo Bridge**, getting into the detail page > DOWNLOAD

## Configuration

### Linkedgo APP
1. Download linkedgo app from IOS store or Google store.
2. Register your linkedgo account by Phone number or E-mail.
3. Create a house
4. Add devices to your house following the app's instructions and assgin a region and a room to each device.

### Linkedgo Bridge Integration Login
[Settings > Devices & services > ADD INTEGRATION](https://my.home-assistant.io/redirect/brand/?brand=linekdgo bridge) > Search `Linkedgo Bridge` > NEXT > Click here to login > Sign in with Linkedgo App account

[![Open your Home Assistant instance and start setting up a new Linkedgo Bridge integration instance.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=linkedgo bridge)

### Add Linkedgo Devices
After logging in successfully, a dialog box named "Select House and Devices" pops up. You can select the House containing the device that you want to import in Home Assistant.
