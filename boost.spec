%define tarball_name boost_1_32_0

Name: boost
Summary: The Boost C++ Libraries
Version: 1.32.0
Release: 1
License: Boost Software License
URL: http://www.boost.org/
Group: System Environment/Libraries
Source: %{tarball_name}.tar.bz2
BuildRoot: %{_tmppath}/boost-%{version}-root
Prereq: /sbin/ldconfig
BuildRequires: libstdc++-devel python 
Obsoletes: boost <= 1.31.0
Obsoletes: boost-devel <= 1.31.0
Obsoletes: boost-doc <= 1.30.2
Obsoletes: boost-python <= 1.30.2
Patch0: boost-base.patch
Patch1: boost-gcc-tools.patch

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library.  One goal is to establish "existing practice" and provide
reference implementations so that the Boost libraries are suitable for
eventual standardization. (Some of the libraries have already been
proposed for inclusion in the C++ Standards Committee's upcoming C++
Standard Library Technical Report.)

%package devel
Summary: The Boost C++ Headers
Group: System Environment/Libraries
Requires: boost = %{version}-%{release}
Obsoletes: boost-python-devel <= 1.30.2
Provides: boost-python-devel = %{version}-%{release}

%description devel
Headers for the Boost C++ libraries

%prep
rm -rf $RPM_BUILD_ROOT

%setup -n %{tarball_name} -q
%patch0 -p0
%patch1 -p0

%build
#build bjam
(cd tools/build/jam_src && ./build.sh)
#build boost with bjam
BJAM=`find tools/build/jam_src/ -name bjam -a -type f`
PYTHON_VERSION=`python -V 2>&1 |sed 's,.* \([0-9]\.[0-9]\)\(\.[0-9]\)\?.*,\1,'`
PYTHON_FLAGS="-sPYTHON_ROOT=/usr -sPYTHON_VERSION=$PYTHON_VERSION"
#$BJAM $PYTHON_FLAGS "-sTOOLS=gcc" "-sBUILD=release <dllversion>1" stage 
$BJAM $PYTHON_FLAGS "-sTOOLS=gcc" "-sBUILD=release" stage 

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}

# install lib
for i in `find stage -type f -name \*.a`; do
  NAME=`basename $i`;
  install -m 755 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
done;
for i in `find stage -type f -name \*.so.*`; do
  NAME=`basename $i`;
  install -m 755 $i $RPM_BUILD_ROOT%{_libdir}/$NAME;
done;

# install include files
for i in `find boost -type d`; do
  mkdir -p $RPM_BUILD_ROOT%{_includedir}/$i
done
for i in `find boost -type f`; do
  install -m 644 $i $RPM_BUILD_ROOT%{_includedir}/$i
done

%clean
rm -rf $RPM_BUILD_ROOT 

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/boost
%{_libdir}/*.a

%changelog
* Mon Nov 29 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-1
- Update to 1.32.0
- (#122817: libboost_*.so symlinks missing)

* Wed Sep 22 2004 Than Ngo <than@redhat.com> 1.31.0-9
- cleanup specfile
- fix multiarch problem

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 05 2004 Warren Togami <wtogami@redhat.com> 1.31.0-7
- missing Obsoletes boost-python

* Mon May 03 2004 Benjamin Kosnik <bkoz@redhat.com> 
- (#121630: gcc34 patch needed)

* Wed Apr 21 2004 Warren Togami <wtogami@redhat.com>
- #121415 FC2 BLOCKER: Obsoletes boost-python-devel, boost-doc
- other cleanups

* Tue Mar 30 2004 Benjamin Kosnik <bkoz@redhat.com> 
- Remove bjam dependency. (via Graydon).
- Fix installed library names.
- Fix SONAMEs in shared libraries.
- Fix installed header location.
- Fix installed permissions.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 09 2004 Benjamin Kosnik <bkoz@redhat.com> 1.31.0-2
- Update to boost-1.31.0

* Thu Jan 22 2004 Benjamin Kosnik <bkoz@redhat.com> 1.31.0-1
- Update to boost-1.31.0.rc2
- (#109307:  Compile Failure with boost libraries)
- (#104831:  Compile errors in apps using Boost.Python...)
- Unify into boost, boost-devel rpms.
- Simplify installation using bjam and prefix install.

* Tue Sep 09 2003 Nalin Dahyabhai <nalin@redhat.com> 1.30.2-2
- require boost-devel instead of devel in subpackages which require boost-devel
- remove stray Prefix: tag

* Mon Sep 08 2003 Benjamin Kosnik <bkoz@redhat.com> 1.30.2-1
- change license to Freely distributable
- verify installation of libboost_thread
- more boost-devel removals
- deal with lack of _REENTRANT on ia64/s390
- (#99458) rpm -e fixed via explict dir additions
- (#103293) update to 1.30.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 13 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove packager, change to new Group:

* Tue May 06 2003 Tim Powers <timp@redhat.com> 1.30.0-3
- add deffattr's so we don't have unknown users owning files
