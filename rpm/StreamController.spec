%define debug_package %{nil}
%define _python_bytecompile_extra 0

Name:           streamcontroller
Version:        __VERSION__
Release:        1%{?dist}
Summary:        Elegant Linux application for Elgato Stream Deck with plugin support

License:        GPL-3.0-or-later
URL:            https://github.com/StreamController/StreamController
Source0:        %{name}-%{version}.tar.gz

# Build dependencies
BuildRequires:  python3-devel >= 3.11
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme

# GTK and GI dependencies
Requires:       gtk4 >= 4.0
Requires:       libadwaita >= 1.0
Requires:       python3-gobject >= 3.42
Requires:       gobject-introspection

# Core Python dependencies
Requires:       python3 >= 3.11
Requires:       python3-dbus
Requires:       python3-requests
Requires:       python3-cairo
Requires:       python3-pillow
Requires:       python3-yaml
Requires:       python3-psutil
Requires:       python3-setproctitle
Requires:       python3-loguru
Requires:       python3-Pyro5

# Optional but recommended dependencies
Recommends:     python3-pulsectl
Recommends:     python3-pygobject-devel
Recommends:     python3-setuptools
Recommends:     udev

# USB and hardware access
Requires:       libusb1 >= 1.0.21
Requires:       hidapi
Requires:       python3-pyusb

# System integration
Requires:       systemd
Requires:       dbus

%description
StreamController is an elegant Linux application designed for the Elgato Stream Deck.
It offers advanced features including:
- Plugin support with built-in store
- Automatic page switching based on active applications
- Custom wallpapers and screen savers
- Multi-device support for various Stream Deck models
- Auto-lock functionality when system is locked
- Native Linux integration with GNOME, KDE, and other desktop environments

This application is designed specifically for Linux users who want powerful
Stream Deck integration without compromising on performance or functionality.

%prep
%autosetup -n %{name}-%{version}

%build
# Build any native dependencies if needed
# Most dependencies will be installed via pip in %install

%install
# Create base directories
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions

# Install the application files
cp -r . %{buildroot}%{_datadir}/%{name}/
# Remove unnecessary files from installation
rm -rf %{buildroot}%{_datadir}/%{name}/.git*
rm -rf %{buildroot}%{_datadir}/%{name}/rpm
rm -rf %{buildroot}%{_datadir}/%{name}/flatpak
rm -rf %{buildroot}%{_datadir}/%{name}/__pycache__
rm -rf %{buildroot}%{_datadir}/%{name}/.venv
find %{buildroot}%{_datadir}/%{name} -name "*.pyc" -delete
find %{buildroot}%{_datadir}/%{name} -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Fix ambiguous Python shebangs
find %{buildroot}%{_datadir}/%{name} -name "*.py" -type f -exec sed -i 's|#!/usr/bin/env python$|#!/usr/bin/python3|g' {} \;

# Install Python dependencies to a local directory
# Note: Skipping automatic dependency installation for now due to complexity
# Users will need to install Python dependencies manually with:
# pip3 install -r /usr/share/streamcontroller/requirements.txt
# cd %{buildroot}%{_datadir}/%{name}
# PYTHONUSERBASE=%{buildroot}%{_datadir}/%{name}/vendor pip3 install --user --no-warn-script-location -r requirements.txt

# Create wrapper script
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/bin/bash
# StreamController launcher script

# Set up Python path
export PYTHONPATH="%{_datadir}/%{name}:$PYTHONPATH"

# Set the working directory
cd %{_datadir}/%{name}

# Launch the application
exec python3 main.py "$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

# Install desktop file
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=StreamController
Comment=Elegant Linux application for Elgato Stream Deck
GenericName=Stream Deck Controller
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Utility;AudioVideo;
Keywords=streamdeck;elgato;stream;deck;controller;
StartupNotify=true
StartupWMClass=StreamController
EOF

# Validate desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install icon
if [ -f flatpak/icon_256.png ]; then
    cp flatpak/icon_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
elif [ -f Assets/icons/hicolor/scalable/apps/com.core447.StreamController.png ]; then
    cp Assets/icons/hicolor/scalable/apps/com.core447.StreamController.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
elif [ -f flatpak/icon.png ]; then
    cp flatpak/icon.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
elif [ -f Assets/Onboarding/icon.png ]; then
    cp Assets/Onboarding/icon.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
fi

# Install udev rules for Stream Deck access
if [ -f udev.rules ]; then
    cp udev.rules %{buildroot}%{_sysconfdir}/udev/rules.d/70-streamcontroller.rules
fi

# Install documentation
cp README.md %{buildroot}%{_datadir}/doc/%{name}/
cp LICENSE %{buildroot}%{_datadir}/licenses/%{name}/

%post
# Update icon cache
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

# Reload udev rules
/usr/bin/udevadm control --reload-rules &>/dev/null || :
/usr/bin/udevadm trigger --subsystem-match=usb &>/dev/null || :

# Set up USB device access for Stream Deck
if [ "$1" -eq 1 ]; then
    echo ""
    echo "=== StreamController Post-Installation Setup ==="
    echo "To use StreamController, your user needs USB device access."
    echo ""
    
    # Check if plugdev group exists, create if not
    if ! getent group plugdev >/dev/null 2>&1; then
        echo "Creating 'plugdev' group for USB device access..."
        groupadd -r plugdev 2>/dev/null || true
        if getent group plugdev >/dev/null 2>&1; then
            echo "✓ plugdev group created successfully"
        else
            echo "⚠ Failed to create plugdev group - you may need to create it manually"
        fi
    else
        echo "✓ plugdev group already exists"
    fi
    
    echo ""
    echo "Next steps:"
    echo "1. Add your user to the 'plugdev' group:"
    echo "   sudo usermod -a -G plugdev \$USER"
    echo ""
    echo "2. Log out and log back in for group changes to take effect"
    echo ""
    echo "3. Verify group membership with:"
    echo "   groups \$USER"
    echo ""
    echo "Alternative USB access methods:"
    echo "• Add user to 'input' group instead: sudo usermod -a -G input \$USER"
    echo "• Run with sudo (not recommended): sudo streamcontroller"
    echo ""
    echo "If you installed from RPM, you may need Python dependencies:"
    echo "  pip3 install --user -r %{_datadir}/%{name}/requirements.txt"
    echo ""
    echo "For troubleshooting, see: %{_datadir}/doc/%{name}/README.md"
    echo "========================================================"
    echo ""
fi

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%doc %{_datadir}/doc/%{name}/README.md
%{_datadir}/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%config(noreplace) %{_sysconfdir}/udev/rules.d/70-streamcontroller.rules

%changelog
* Fri Jun 27 2025 StreamController Team <dev@streamcontroller.org> - 1.5.2-1
- Fixed RPM packaging dependencies (python3-pycairo -> python3-cairo)
- Enhanced RPM packaging with proper dependency management
- Added comprehensive system integration
- Improved udev rules and permissions handling
- Better desktop environment integration
- Removed bundled Python dependencies for system compatibility

* Wed Jan 01 2025 StreamController Team <dev@streamcontroller.org> - 1.5.0-1
- Updated to version 1.5.0
- Added plugin store integration
- Enhanced multi-device support
- Improved auto-lock functionality

* Mon Jan 01 2024 StreamController Team <dev@streamcontroller.org> - 1.1-4
- Initial RPM packaging
- Basic functionality and dependencies