#
# TODO:
# - add subpackages for $PACKAGES
# - fix tomcat.home
Summary:	Scalix Platform
Name:		scalix
Version:	11.4.3
Release:	0.1
# http://www.scalix.com/community/opensource/licensing.php
License:	Scalix Public License (SPL)
Group:		Applications/WWW
Source0:	http://downloads.scalix.com/.opensource/11.4.3/%{name}-%{version}-GA-source.tgz	
# Source0-md5:	fb4794f841319ed07605a8619e5a9c36
URL:		http://www.scalix.com/community/
BuildRequires:	ant >= 1.6.5
BuildRequires:	python-devel >= 2.4
BuildRequires:	java-sun
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scalix Platform

%package installer
Summary:	Scalix Platform Installer
Group:		Applications/WWW
Requires:	awk
Requires:	perl-base

%description installer
Installer for Scalix Platform

%package mobile
Summary:        Scalix Platform for Mobile
Group:          Applications/WWW

%description mobile
Mobile Scalix

%prep
%setup -qc
%{__tar} zxf scalix-installer-src.tgz
%{__tar} zxf scalix-mobile-src.tgz
%{__tar} zxf scalix-platform-src.tgz
%{__tar} zxf scalix-sac-src.tgz
%{__tar} zxf scalix-sis-src.tgz

#PACKAGES="installer mobile platform sac sis"
PACKAGES="installer"

for i in $PACKAGES
do
cd scalix-$i
install -d build
%ant
cd -
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install scalix-installer/dist/scalix-installer $RPM_BUILD_ROOT%{_sbindir}/scalix-installer

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%files installer
%defattr(644,root,root,755
%attr(755,root,root) %{_sbindir}/scalix-installer
