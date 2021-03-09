%global repo dde-session-shell
%if 0%{?fedora}
%global dde_prefix deepin
%else
%global dde_prefix dde
%global debug_package %{nil}
%debug_package %{nil}
%endif


Name:           %{dde_prefix}-session-shell
Version:        5.3.0.39
Release:        1%{?fedora:%dist}
Summary:        deepin-session-shell - Deepin desktop-environment - session-shell module
License:        GPLv3+
%if 0%{?fedora}
URL:            https://github.com/linuxdeepin/%{repo}
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
%else
URL:            http://shuttle.corp.deepin.com/cache/repos/eagle/release-candidate/RERFNS4wLjAuNzYxMA/pool/main/d/dde-session-shell/
Source0:        %{name}_%{version}.orig.tar.xz
%endif

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  dtkcore-devel >= 5.1
BuildRequires:  qt5-linguist
BuildRequires:  dtkwidget-devel >= 5.1
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXi-devel
BuildRequires:  xcb-util-wm xcb-util-wm-devel
BuildRequires:  %{dde_prefix}-qt-dbus-factory-devel
BuildRequires:  gsettings-qt-devel
BuildRequires:  lightdm-qt5-devel
BuildRequires:  pam-devel
Requires:       lightdm
Provides:       lightdm-deepin-greeter%{?_isa} = %{version}-%{release}
Provides:       lightdm-greeter = 1.2

%description
deepin-session-shell - Deepin desktop-environment - session-shell module.

%prep
%autosetup -p1 -n %{repo}-%{version}



%build
export PATH=$PATH:%{_qt5_bindir}
cmake_version=$(cmake --version | head -1 | awk '{print $3}')
sed -i "s|VERSION 3.13.4|VERSION $cmake_version|g" CMakeLists.txt
%cmake %{!?fedora:.}
%if 0%{?fedora}
%cmake_build
%else
%make_build
%endif

%install
%if 0%{?fedora}
%cmake_install
%else
%make_install
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/dde-*.desktop

%files
%license LICENSE
%{_bindir}/dde-lock
%{_bindir}/dde-lock-wrapper
%{_bindir}/dde-shutdown
%{_bindir}/dde-shutdown-wrapper
%{_bindir}/lightdm-deepin-greeter
%attr(755,root,root) %{_bindir}/deepin-greeter
%{_sysconfdir}/deepin/greeters.d/00-xrandr
%{_sysconfdir}/deepin/greeters.d/lightdm-deepin-greeter
%{_datadir}/dde-session-shell/
%{_datadir}/applications/dde-lock.desktop
%{_datadir}/applications/dde-shutdown.desktop
%{_datadir}/xgreeters/lightdm-deepin-greeter.desktop
%{_datadir}/dbus-1/services/com.deepin.dde.lockFront.service
%{_datadir}/dbus-1/services/com.deepin.dde.shutdownFront.service

%changelog
* Thu Jun 11 2020 uoser <uoser@uniontech.com> - 5.0.0.8
- Update to 5.0.0.8
