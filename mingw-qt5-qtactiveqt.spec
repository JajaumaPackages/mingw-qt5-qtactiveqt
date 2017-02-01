%?mingw_package_header

%global qt_module qtactiveqt
#%%global pre rc1

#%%global snapshot_date 20121111
#%%global snapshot_rev 435fac3b

%if 0%{?snapshot_date}
%global source_folder qt-%{qt_module}
%else
%global source_folder %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
%endif

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-qt5-%{qt_module}
Version:        5.6.0
Release:        1%{?pre:.%{pre}}%{?snapshot_date:.git%{snapshot_date}.%{snapshot_rev}}%{?dist}
Summary:        Qt5 for Windows - QtActiveQt component

License:        GPLv3 with exceptions or LGPLv2 with exceptions or BSD
Group:          Development/Libraries
URL:            http://qt.io/

%if 0%{?snapshot_date}
# To regenerate:
# wget http://qt.gitorious.org/qt/%{qt_module}/archive-tarball/%{snapshot_rev} -O qt5-%{qt_module}-%{snapshot_rev}.tar.gz
Source0:        qt5-%{qt_module}-%{snapshot_rev}.tar.gz
%else
%if "%{?pre}" != ""
Source0:        http://download.qt-project.org/development_releases/qt/%{release_version}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0:        http://download.qt-project.org/official_releases/qt/%{release_version}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 96
BuildRequires:  mingw32-qt5-qtbase >= 5.6.0

BuildRequires:  mingw64-filesystem >= 96
BuildRequires:  mingw64-qt5-qtbase >= 5.6.0

# Fix linker error:
# qaxserverbase.cpp:1769: undefined reference to `qt_sendSpontaneousEvent(QObject*, QEvent*)'
Patch0:         qt5-activeqt-fix-compilation.patch

# Don't try to build stuff which requires windows.h with the native Linux gcc
Patch1:         qtactiveqt-fix-build.patch

# dumpcpp and MetaObjectGenerator::readClassInfo do not handle win64
# https://bugreports.qt.io/browse/QTBUG-46827
Patch2:         qtactiveqt-win64.patch


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtActiveQt component

%description -n mingw32-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win64
%package -n mingw64-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtActiveQt component

%description -n mingw64-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%?mingw_debug_package


%prep
%setup -q -n %{source_folder}
%patch0 -p0
%patch1 -p1
%patch2 -p1


%build
%mingw_qmake_qt5 ../%{qt_module}.pro
%mingw_make %{?_smp_mflags}


%install
%mingw_make install INSTALL_ROOT=$RPM_BUILD_ROOT

# .prl files aren't interesting for us
find $RPM_BUILD_ROOT -name "*.prl" -delete

# The ActiveQt libraries are only built as static libraries
# so there's no need to rename them to .dll.a


# Win32
%files -n mingw32-qt5-%{qt_module}
%license LGPL_EXCEPTION.txt LICENSE.FDL LICENSE.LGPLv21 LICENSE.LGPLv3
%{mingw32_bindir}/dumpcpp.exe
%{mingw32_bindir}/dumpdoc.exe
%{mingw32_bindir}/idc.exe
%{mingw32_bindir}/testcon.exe
%{mingw32_includedir}/qt5/ActiveQt/
%{mingw32_libdir}/libQt5AxBase.a
%{mingw32_libdir}/libQt5AxContainer.a
%{mingw32_libdir}/libQt5AxServer.a
%{mingw32_libdir}/cmake/Qt5AxBase/
%{mingw32_libdir}/cmake/Qt5AxContainer/
%{mingw32_libdir}/cmake/Qt5AxServer/
%{mingw32_libdir}/pkgconfig/Qt5AxBase.pc
%{mingw32_libdir}/pkgconfig/Qt5AxContainer.pc
%{mingw32_libdir}/pkgconfig/Qt5AxServer.pc
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_axbase.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_axbase_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_axcontainer.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_axcontainer_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_axserver.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_axserver_private.pri

# Win64
%files -n mingw64-qt5-%{qt_module}
%license LGPL_EXCEPTION.txt LICENSE.FDL LICENSE.LGPLv21 LICENSE.LGPLv3
%{mingw64_bindir}/dumpcpp.exe
%{mingw64_bindir}/dumpdoc.exe
%{mingw64_bindir}/idc.exe
%{mingw64_bindir}/testcon.exe
%{mingw64_includedir}/qt5/ActiveQt/
%{mingw64_libdir}/libQt5AxBase.a
%{mingw64_libdir}/libQt5AxContainer.a
%{mingw64_libdir}/libQt5AxServer.a
%{mingw64_libdir}/cmake/Qt5AxBase/
%{mingw64_libdir}/cmake/Qt5AxContainer/
%{mingw64_libdir}/cmake/Qt5AxServer/
%{mingw64_libdir}/pkgconfig/Qt5AxBase.pc
%{mingw64_libdir}/pkgconfig/Qt5AxContainer.pc
%{mingw64_libdir}/pkgconfig/Qt5AxServer.pc
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_axbase.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_axbase_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_axcontainer.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_axcontainer_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_axserver.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_axserver_private.pri


%changelog
* Sun Apr 10 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-1
- Update to 5.6.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-1
- Update to 5.5.1

* Fri Aug  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0

* Sat Jun 27 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.2-1
- Update to 5.4.2
- Changed URL to http://qt.io/
- Use the %%license tag and use BSD license
- dumpcpp and MetaObjectGenerator::readClassInfo do not handle win64 (QTBUG-46827)

* Tue Mar 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-1
- Update to 5.4.1

* Thu Jan  1 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-1
- Update to 5.4.0

* Sun May 25 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.0-1
- Update to 5.3.0

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Fri Jan 10 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-2
- Added license files

* Sun Jan  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0

* Fri Nov 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.1.rc1
- Update to 5.2.0 RC1

* Sun Jul 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0

* Fri May 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2

* Sat Feb  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1

* Thu Jan  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-1
- Update to 5.0.0 Final

* Sun Nov 11 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.2.beta1.git20121111.435fac3b
- Update to 20121111 snapshot (rev 4cbcad7f)
- Rebuild against latest mingw-qt5-qtbase

* Mon Sep 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.1.beta1
- Initial release

