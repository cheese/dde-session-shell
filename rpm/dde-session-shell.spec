%global repo dde-session-shell
%if 0%{?fedora}
%global dde_prefix deepin
%else
%global dde_prefix dde
%global debug_package %{nil}
%debug_package %{nil}
%endif


Name:           %{dde_prefix}-session-shell
Version:        5.3.0.45
Release:        1%{?fedora:%dist}
Summary:        Deepin Desktop Environment - session-shell module
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
BuildRequires:  make
# provides needed directories
Requires:       dbus-common
Requires:       %{_bindir}/qdbus-qt5
Requires:       lightdm
Provides:       lightdm-deepin-greeter%{?_isa} = %{version}-%{release}
Provides:       lightdm-greeter = 1.2

%description
deepin-session-shell - Deepin desktop-environment - session-shell module.

%prep
%autosetup -p1 -n %{repo}-%{version}
sed -i 's:/usr/lib:%{_libexecdir}:' scripts/lightdm-deepin-greeter
sed -i 's/qdbus /qdbus-qt5 /' files/*-wapper
%if 0%{?fedora}
# https://github.com/linuxdeepin/dde-session-shell/issues/21
# work around by changing to Qt::FastTransformation
sed -i 's/Qt::SmoothTransformation/Qt::FastTransformation/' \
       src/widgets/fullscreenbackground.cpp
# We don't have common-auth on Fedora
sed -i 's/common-auth/password-auth/' src/libdde-auth/authagent.cpp
%endif

%build
export PATH=$PATH:%{_qt5_bindir}
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
chmod -v 755 %{buildroot}%{_bindir}/*wapper

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/dde-*.desktop

%files
%{_bindir}/dde-lock
%{_bindir}/dde-shutdown
%{_bindir}/dde-lock-wapper
%{_bindir}/dde-shutdown-wapper
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
* Tue Nov 17 2020 Robin Lee <cheeselee@fedoraproject.org> - 5.3.0.24-1
- Update to 5.3.0.24

* Sat Nov 14 2020 Robin Lee <cheeselee@fedoraproject.org> - 5.3.0.22-2
- Requires dbus-common

* Fri Nov 13 2020 Robin Lee <cheeselee@fedoraproject.org> - 5.3.0.22-1
- Initial packaging
