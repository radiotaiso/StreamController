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
