# set to nil when packaging a release, 
# or the long commit tag for the specific git branch
%global commit_tag %{nil}

# set with the commit date only if commit_tag not nil 
# git version (i.e. master) in format date +Ymd
%if "%{commit_tag}" != "%{nil}"
%global commit_date %(git show -s --date=format:'%Y%m%d' %{commit_tag})
%endif

# repack non-release git branches as .xz with the commit date
# in the following format <name>-<version>-<commit_date>.xz

Name:           fcitx5
Version:        5.1.12
Release:        %{?commit_date:~0.%{commit_date}.}1
Summary:        maybe a new fcitx.
Group:          Development
License:        LGPLv2.1+
URL:            https://github.com/fcitx/fcitx5

# change the source URL depending on if the package is a release version or a git version
%if "%{commit_tag}" != "%{nil}"
Source0:        https://github.com/<org_name>/<project_name>/archive/%{commit_tag}.tar.gz#/%{name}-%{version}.xz
%else
Source0:        %url/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

Source1:        %name.service
Source2:        xim.d-%name
Source3:        macros.%name
Source4:        Fcitx.svg

BuildSystem:    cmake
# has a bug where it needs a library it needs to build (wrong path) 
# to write spellcheck from a download
BuildOption:    -DBUILD_SPELL_DICT:BOOL=OFF -DENABLE_TEST:BOOL=OFF

BuildRequires:  librsvg2
BuildRequires:  gettext-devel
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(ECM)
BuildRequires:  cmake(json-c)
BuildRequires:  cmake(dbus1)
BuildRequires:  cmake(xcbimdkit)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(cldr-emoji-annotation)
BuildRequires:  pkgconfig(enchant-2)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  pkgconfig(xkeyboard-config)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)

Provides:       fcitx = %{version}
Obsoletes:      fcitx < 5
Provides:       inputmethod

%description
Fcitx 5 is a generic input method framework

%package devel
Summary:        Development files for %name
Group:          Development/Libraries/C and C++
Requires:       fcitx5 = %{version}
Requires:       %{_lib}Fcitx5Config6 = %{version}
Requires:       %{_lib}Fcitx5Core7 = %{version}
Requires:       %{_lib}Fcitx5Utils2 = %{version}
Provides:       fcitx-devel = %{version}
Obsoletes:      fcitx-devel < 5

%description devel
This package provides development files for %name.

%package -n %{_lib}Fcitx5Config6
Summary:        Configuration library for %name
Group:          System/Libraries
Provides:       %{_lib}Fcitx5Config5 = %{version}
Obsoletes:      %{_lib}Fcitx5Config5 < %{version}
Obsoletes:      %{_lib}fcitx-config4 < 5

%description -n %{_lib}Fcitx5Config6
This package provides configuration libraries for %name.

%package -n %{_lib}Fcitx5Core7
Summary:        Core library for %name
Group:          System/Libraries
Provides:       %{_lib}fcitx-4_2_9 = %{version}
Obsoletes:      %{_lib}fcitx-4_2_9 < 5
Provides:       %{_lib}Fcitx5Core5 = %{version}
Obsoletes:      %{_lib}Fcitx5Core5 < %{version}
Provides:       %{_lib}fcitx-core0 = %{version}
Obsoletes:      %{_lib}fcitx-core0 < 5

%description -n %{_lib}Fcitx5Core7
This package provides core libraries for %name.

%package -n %{_lib}Fcitx5Utils2
Summary:        Utility library for %name
Group:          System/Libraries
Provides:       %{_lib}Fcitx5Utils1 = %{version}
Obsoletes:      %{_lib}Fcitx5Utils1 < %{version}
Provides:       %{_lib}fcitx-utils0 = %{version}
Obsoletes:      %{_lib}fcitx-utils0 < 5

%description -n %{_lib}Fcitx5Utils2
This package provides utility libraries for %name.

%install
install -D -m 0644 %{S:1} %{buildroot}%{_userunitdir}/%name.service

mkdir -p %{buildroot}%{_sysconfdir}/X11/xim.d/
install -m 644 %{S:2} %{buildroot}%{_sysconfdir}/X11/xim.d/%name 
priority=30 
pushd  %{buildroot}%{_sysconfdir}/X11/xim.d/ 
    for lang in am ar as bn el fa gu he hi hr ja ka kk kn ko lo ml my \
                pa ru sk vi zh_TW zh_CN zh_HK zh_SG \
                de fr it es nl cs pl da nn nb fi en sv ; do 
        mkdir $lang 
        pushd $lang 
            ln -s ../%name $priority-%name 
        popd 
    done 
popd 

install -Dm 0644 %{S:3} %{buildroot}%{_prefix}/lib/rpm/macros.d/macros.%name

for i in 16 22 24 32 48 512; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
  rsvg-convert -h $i -w $i %{S:4} -o %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/fcitx.png
done
install -D -m 0644 %{S:4} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/fcitx.svg

%buildsystem_cmake_install

%files
%license LICENSES
%doc README.md
%{_sysconfdir}/X11/xim.d/
%dir %{_sysconfdir}/xdg/Xwayland-session.d
%{_sysconfdir}/xdg/Xwayland-session.d/20-fcitx-x11
%{_sysconfdir}/xdg/autostart/org.fcitx.Fcitx5.desktop
%{_bindir}/%name
%{_bindir}/%name-configtool
%{_bindir}/%name-remote
%{_bindir}/%name-diagnose
%{_libdir}/%name
%{_libexecdir}/%name-wayland-launcher
%{_userunitdir}/%name.service
%{_datadir}/applications/org.fcitx.Fcitx5.desktop
%{_datadir}/applications/fcitx5-configtool.desktop
%{_datadir}/applications/fcitx5-wayland-launcher.desktop
%{_datadir}/%name
%{_datadir}/icons/hicolor/*/apps/fcitx.*
%{_datadir}/icons/hicolor/*/apps/org.fcitx.Fcitx5.*
%{_datadir}/dbus-1/services/org.fcitx.Fcitx5.service
%{_datadir}/metainfo/org.fcitx.Fcitx5.metainfo.xml
%{_datadir}/locale/*

%files devel
%{_prefix}/lib/rpm/macros.d/macros.%name
%{_includedir}/Fcitx5
%{_libdir}/cmake/Fcitx5*
%{_libdir}/libFcitx5Config.so
%{_libdir}/libFcitx5Core.so
%{_libdir}/libFcitx5Utils.so
%{_libdir}/pkgconfig/Fcitx5*.pc

%files -n %{_lib}Fcitx5Config6
%{_libdir}/libFcitx5Config.so.6
%{_libdir}/libFcitx5Config.so.%{version}

%files -n %{_lib}Fcitx5Core7
%{_libdir}/libFcitx5Core.so.7
%{_libdir}/libFcitx5Core.so.%{version}

%files -n %{_lib}Fcitx5Utils2
%{_libdir}/libFcitx5Utils.so.2
%{_libdir}/libFcitx5Utils.so.%{version}

