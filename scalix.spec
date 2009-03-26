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
Patch0:		%{name}-python25_26.patch
Patch1:		%{name}-merlin-fixes.patch
Patch2:		%{name}-build.patch
URL:		http://www.scalix.com/community/
BuildRequires:	ant >= 1.6.5
BuildRequires:	antlr >= 2.7.6
BuildRequires:	asm2 >= 2.2.3
BuildRequires:	java-mail
BuildRequires:	java-servletapi5
BuildRequires:	java-commons-cli
BuildRequires:	java-commons-codec
BuildRequires:	java-commons-collections
BuildRequires:	java-commons-httpclient
BuildRequires:	java-commons-lang
BuildRequires:	java-commons-logging
BuildRequires:	java-sun
BuildRequires:	python-devel >= 2.2.2
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
Summary:	Scalix Platform for Mobile
Group:		Applications/WWW

%description mobile
Mobile Scalix

%prep
%setup -qc
%{__tar} zxf scalix-installer-src.tgz
%{__tar} zxf scalix-mobile-src.tgz
%{__tar} zxf scalix-platform-src.tgz
%{__tar} zxf scalix-sac-src.tgz
%{__tar} zxf scalix-sis-src.tgz
%patch0 -p0
%patch1 -p0
#%patch2 -p1

%build

CLASSPATH=$(build-classpath activation antlr asm commons-cli commons-codec commons-collections commons-httpclient commons-lang commons-logging mail servlet)
#PACKAGES="installer mobile platform sac sis"
PACKAGES="installer mobile"

for i in $PACKAGES
do
cd scalix-$i
install -d build
%ant -Dbuild.sysclasspath=only
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
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/scalix-installer
