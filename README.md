# StreamController

[![RPM Release](https://img.shields.io/badge/RPM-latest-blueviolet?logo=fedora)](https://github.com/radiotaiso/StreamController/releases/latest)

![Gluten Free](https://forthebadge.com/images/featured/featured-gluten-free.svg)

![It works no idea why](https://forthebadge.com/images/badges/it-works-no-idea-why.svg)

![You didn't ask for this](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)

## WAIT A MINUTE

This repo is only a wrapper with a github action set up to auto build a `.rpm` package of `StreamController` the motivation behind this is my despise for flatpaks and that I've been using fedora on main.

The only changes are in `/rpm`; otherwise, it is the same as upstream. Check the [README](./rpm/README.md) inside for more info.

![Wait a minute tf2 scout](https://media1.tenor.com/m/aYNpQ7uZhR4AAAAd/tf2-scout.gif)

## Back to regular programming

**StreamController** is an elegant Linux application designed for the Elgato Stream Deck, offering advanced features like plug-ins and automatic page switching to enhance your streaming and productivity setup.

![Main Screen](https://core447.com/assets/screenshots/main_screen.png)  
*Background image by [kvacm](https://kvacm.artstation.com)*

## In Action

[![YouTube](http://i.ytimg.com/vi/kIJOj_6Jimk/hqdefault.jpg)](https://www.youtube.com/watch?v=kIJOj_6Jimk)  
(click on the image to play)

@danie10 created this amazing video going over all the details and features of StreamController. You can use the available timestamps to jump to specific parts of the video.

## Supported Devices

StreamController supports the following Elgato Stream Deck models:

- Stream Deck Original (2)
- Stream Deck Mini
- Stream Deck XL
- Stream Deck Pedal
- Stream Deck Plus
- Stream Deck Neo (only the normal buttons)
- Stream Deck Modules

## Features

### Plugins

StreamController features plugin support with a built-in store to download your favorite actions. You can also publish your own plugins. For more details, visit the [Wiki](https://streamcontroller.github.io/docs).

### Wallpapers

Customize your Stream Deck pages with cool wallpapers and videos to make them more engaging.

### Screen Saver

Set up a custom screen saver to display a picture or video when your Stream Deck is in idle.

### Automatic Page Switching

Available for GNOME, Hyprland, Sway, KDE (when kdotool is installed) and all X11 desktops, this feature allows you to automatically change your active page based on the active window. For example, you can switch to your favorite music albums when you open Spotify, your projects when you open VSCode, or your favorite websites in Firefox.

## Auto-Lock

Lock your Stream deck when your system is locked, preventing unwanted use from third parties (available on KDE and GNOME, and Cinnamon).

## Installation

RPM Package is not affiliated with StreamController, I just hate flatpaks.

To install StreamController, click the button below or follow the [installation instructions](https://streamcontroller.github.io/docs/latest/installation/):

Download the latest `.rpm` file from [the release page](https://github.com/radiotaiso/StreamController/releases)

`sudo dnf install streamcontroller-1.5.0beta.11-1.fc42.x86_64.rpm`

### Unofficial Packages

The following packages are functional but unofficial and maintained by our community:

[![Packaging status](https://repology.org/badge/vertical-allrepos/streamcontroller.svg)](https://repology.org/project/streamcontroller/versions)

## Warning

StreamController is currently in beta. While core features like actions and pages are stable, high memory usage can still be an issue. We are actively working to resolve this and bring the app to a stable release soon. Please report any issues you encounter.

## Contributing

We welcome contributions! Feel free to open pull requests to improve StreamController.

If you're interested in helping with the development of this app, you can contact me on our [Discord server](https://discord.gg/MSyHM8TN3u) to request write access to our [Dev planning board](https://github.com/orgs/StreamController/projects/2). For more information see [Dev-Planning-Board](Dev-Planning-Board.md).

### Contributors

Thank you to all our contributors for your hard work and support!

<a href="https://github.com/streamcontroller/streamcontroller/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=streamcontroller/streamcontroller"/>
</a>

## Links

- [Website](https://core447.com)
- [Wiki](https://streamcontroller.github.io/docs)
- [Discord](https://discord.gg/MSyHM8TN3u)

## Note

This application is unofficial and not affiliated with Elgato.
