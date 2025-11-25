# RPM Packaging for StreamController

This document provides an overview of the RPM packaging mechanism for StreamController, designed for easy building and deployment on RPM-based Linux distributions (e.g., Fedora, CentOS, openSUSE).

## Quick Start

To build the RPM package, ensure you have the necessary build tools, then run `make`:

```bash
# Install build dependencies (on Fedora)
sudo dnf install rpm-build desktop-file-utils python3-wheel

# Build the RPM
make -C rpm/ rpm
```

The built RPM file will be located in `~/rpmbuild/RPMS/`.

### Targeting Fedora 43 builds

The build script now honors a `TARGET_DIST` environment variable so we can force
the RPM dist tag even when CI runners lag behind the latest Fedora release. By
default it uses the host's `%{?dist}` value and falls back to `.fc43` if unset.
To guarantee Fedora 43 tagging (useful when GitHub Actions is still on a 42
image), run:

```bash
TARGET_DIST=.fc43 make -C rpm/ rpm
```

That value is passed to `rpmbuild -bs/-bb` via `--define 'dist …'`, ensuring the
resulting packages are labeled `*.fc43`. Adjust the variable if you need to
target a different Fedora release.

## Runtime Python Dependencies

This fork intentionally keeps the upstream application code unchanged, so no
third-party Python modules are vendored inside the RPM. Instead, the spec file
declares every runtime dependency that Fedora/Nobara already ship as
`python3-*` packages. Installing the RPM via DNF now brings in:

- Core UI/runtime libs: `python3-gobject`, `python3-typing-extensions`,
    `python3-requests`, `python3-yaml`, `python3-psutil`,
    `python3-setproctitle`, `python3-loguru`.
- Graphics & media helpers: `python3-pillow` (PIL), `python3-opencv` (`cv2`),
    `python3-cairosvg`, `python3-fonttools`, `python3-imageio`,
    `python3-matplotlib`, `python3-numpy`, `python3-packaging`.
- Hardware/Wayland integration: `python3-pyusb` (`usb`), `python3-evdev`,
    `python3-async-lru`, `python3-pyclip`, `python3-pywayland` (`import wayland`),
    `python3-rpyc`, plus the long-standing GTK stack dependencies.
- Miscellaneous helpers: `python3-fuzzywuzzy` for string matching and
    `python3-cairo` for rendering support.

For the authoritative list, refer to the `Requires:` block in
`rpm/StreamController.spec`.

### Modules without Fedora RPMs

Some upstream Python libraries (most notably the StreamDeck SDK and the plugin
tooling helpers) are still missing from the Fedora/Nobara repos. Because this
fork must not modify upstream sources or vendor additional code, install the
following modules with pip *after* installing the RPM (system-wide or in a
virtualenv, your choice):

```bash
python3 -m pip install --user streamdeck Pyro5 streamcontroller_plugin_tools \
    usbmonitor videoprops indexed_bzip2
```

Those six packages cover every import that currently lacks a native RPM (`pip`
will skip ones you already installed). If Fedora ever gains official packages
for them, feel free to drop the manual step and rely solely on DNF.

## Key Files

The packaging process is managed by three main files in this directory:

1. **`Makefile`**: The primary entry point for developers. It provides simple targets for common operations.
    - `make rpm`: Builds the binary RPM package.
    - `make srpm`: Builds the source RPM package.
    - `make install`: Installs the built RPM locally.
    - `make clean`: Removes build artifacts.
    - `make check-deps`: Verifies that all build dependencies are installed.

2. **`build_rpm.sh`**: A shell script that orchestrates the entire build process. It is called by the `Makefile`. Its responsibilities include:
    - Setting up the `rpmbuild` directory structure in `~/rpmbuild`.
    - Creating a source tarball (`.tar.gz`) of the application, excluding development files.
    - Invoking `rpmbuild` to create the source and binary packages based on the spec file.

3. **`StreamController.spec`**: The core of the RPM package. This file defines the package's metadata, dependencies, and installation logic.
    - **Metadata**: Name, version, license, and summary.
    - **Dependencies**: Lists both build-time (`BuildRequires`) and runtime (`Requires`) dependencies.
    - **`%install` section**: Contains shell commands that copy the application files into the build root, which becomes the final package structure.
    - **`%files` section**: Explicitly lists all files and directories to be included in the RPM.
    - **`%post` script**: A post-installation script that runs on the user's system to handle tasks like reloading `udev` rules and displaying setup instructions.

## Build Process Explained

When you run `make rpm`, the following steps are executed:

1. The `Makefile` invokes the `./build_rpm.sh` script.
2. The script creates a standard RPM build environment inside `~/rpmbuild`.
3. It archives the project source code into a tarball and places it in `~/rpmbuild/SOURCES`.
4. It copies the `StreamController.spec` file to `~/rpmbuild/SPECS`.
5. Finally, it calls `rpmbuild -bb`, which reads the spec file and performs the build:
    - It unpacks the source tarball.
    - It executes the commands in the `%install` section to stage the files.
    - It packages the staged files, along with the defined metadata and scripts, into a binary RPM file.

The final package is placed in a subdirectory within `~/rpmbuild/RPMS/`.

## GitHub Actions Automation

This repository uses GitHub Actions to automate the process of building and releasing RPM packages whenever a new version of the upstream StreamController is released. The automation is handled by two workflows located in the `.github/workflows/` directory.

### 1. `check-upstream-tags.yml`

This workflow acts as a scheduler to check for new releases.

- **Purpose**: To monitor the official `StreamController/StreamController` repository for new tags (versions).
- **Trigger**: Runs automatically every Monday at 10 AM UTC and can also be triggered manually.
- **Process**:
  1. It fetches the latest version tag from the upstream repository.
  2. It checks if a corresponding GitHub Release already exists in this repository.
  3. If the release does **not** exist, it triggers the `rpm-autobuild-simple.yml` workflow to start the build process.

### 2. `rpm-autobuild-simple.yml`

This workflow performs the actual build and release of the RPM package.

- **Purpose**: To build the RPM, create a GitHub Release, and upload the package.
- **Trigger**: Called by the `check-upstream-tags.yml` workflow or can be run manually.
- **Process**:
  1. **Setup**: It runs inside a Fedora container to ensure a consistent build environment.
  2. **Source Checkout**: It downloads the source code of the latest upstream tag and combines it with the RPM packaging files (`.spec`, `Makefile`) from this repository.
  3. **Build**: It runs the `make rpm` command to build the binary RPM package.
  4. **Release**: It creates a new GitHub Release in this repository, with a tag that matches the upstream version.
  5. **Upload**: It uploads the newly built `.rpm` file as an asset to the GitHub Release, making it available for download.
