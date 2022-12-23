# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.32
# 

Name:       harbour-tailscale

# >> macros
%global _missing_build_ids_terminate_build 0
# << macros

%{!?qtc_qmake:%define qtc_qmake %qmake}
%{!?qtc_qmake5:%define qtc_qmake5 %qmake5}
%{!?qtc_make:%define qtc_make make}
%{?qtc_builddir:%define _builddir %qtc_builddir}
Summary:    tailscale
Version:    0.0.1
Release:    1
Group:      Qt/Qt
License:    GPLv3
URL:        https://scarpino.dev
Source0:    %{name}-%{version}.tar.bz2
Source1:    tailscaled.service
Source2:    tailscale
Source3:    tailscaled
Source4:    tailscaled.defaults
Source100:  harbour-tailscale.yaml
Requires:   sailfishsilica-qt5 >= 0.10.9
BuildRequires:  pkgconfig(sailfishapp) >= 1.0.2
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  desktop-file-utils

%description

Tailscale makes networking easy

%if "%{?vendor}" == "chum"
PackageName: tailscale
Type: desktop-application
DeveloperName: Andrea Scarpino
Categories:
 - Network
Custom:
  Repo: https://github.com/ilpianista/harbour-tailscale
Screenshots:
 - https://github.com/ilpianista/harbour-tailscale/-/raw/master/screenshots/screenshot_1.png
Url:
  Homepage: https://github.com/ilpianista/harbour-tailscale
  Bugtracker: https://github.com/ilpianista/harbour-tailscale/-/issues
  Donation: https://liberapay.com/ilpianista
%endif


%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
# << build pre

%qtc_qmake5 

%qtc_make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%qmake5_install

# >> install post
install -d %{buildroot}%{_unitdir}
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}

install -m755 %{SOURCE2} %{buildroot}%{_bindir}
install -m755 %{SOURCE3} %{buildroot}%{_bindir}

install -d %{buildroot}%{_libdir}/tailscale

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -Dm644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/tailscaled
# << install post

desktop-file-install --delete-original       \
  --dir %{buildroot}%{_datadir}/applications             \
   %{buildroot}%{_datadir}/applications/*.desktop

%files
%defattr(-,root,root,-)
%attr(4755,root,root) %{_bindir}/%{name}
%{_bindir}/tailscale
%{_bindir}/tailscaled
%{_datadir}/%{name}
%{_sysconfdir}/sysconfig/tailscaled
%{_unitdir}/tailscaled.service
%dir %{_libdir}/tailscale
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
# >> files
# << files

%post
systemctl daemon-reload

%postun
if [ $1 = 0 ]; then
  systemctl stop tailscaled.service
  systemctl disable tailscaled.service
  systemctl daemon-reload
fi