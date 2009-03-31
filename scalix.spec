# TODO:
# - add subpackages for $PACKAGES
# - fix tomcat.home
%bcond_with     java_sun        # build with java-sun

%if "%{pld_release}" == "ti"
%define with_java_sun   1
%endif

%include        /usr/lib/rpm/macros.java
Summary:	Scalix Platform
Name:		scalix
Version:	11.4.3
Release:	0.1
# http://www.scalix.com/community/opensource/licensing.php
License:	Scalix Public License (SPL)
Group:		Applications/WWW
Source0:	http://downloads.scalix.com/.opensource/11.4.3/%{name}-%{version}-GA-source.tgz
# Source0-md5:	fb4794f841319ed07605a8619e5a9c36
Source1:	%{name}-sis-context.xml
Source2:	%{name}-caa-services.xml
Source3:	%{name}-admin-console.xml
Source4:	%{name}-res.xml
Patch0:		%{name}-python25_26.patch
Patch1:		%{name}-merlin-fixes.patch
Patch2:		%{name}-build.patch
URL:		http://www.scalix.com/community/
BuildRequires:	ant >= 1.6.5
BuildRequires:	ant-junit
BuildRequires:	ant-nodeps
BuildRequires:	antlr >= 2.7.6
BuildRequires:	apache-tomcat
BuildRequires:	asm2 >= 2.2.3
BuildRequires:	java-commons-cli
BuildRequires:	java-commons-codec
BuildRequires:	java-commons-collections
BuildRequires:	java-commons-el
BuildRequires:	java-commons-httpclient
BuildRequires:	java-commons-lang
BuildRequires:	java-commons-logging
%{!?with_java_sun:BuildRequires:        java-gcj-compat-devel}
BuildRequires:	java-ical4j
BuildRequires:	java-log4j
BuildRequires:	java-lucene-contrib
BuildRequires:	java-mail
BuildRequires:	java-saaj
BuildRequires:	java-servletapi5
%{?with_java_sun:BuildRequires: java-sun}
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

%package sac
Summary:	Scalix SAC
Group:		Applications/WWW
Requires:	%{name} = %{version}

%description sac
SAC for Scalix

%package sis
Summary:	Scalix SIS
Group:		Applications/WWW
Requires:	%{name} = %{version}

%description sis
SIS for Scalix

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

CLASSPATH=caa/build/WEB-INF/classes:res/build/WEB-INF/classes:$(build-classpath-directory %{_datadir}/tomcat/common/lib/):$(build-classpath activation antlr asm2 commons-cli commons-codec commons-collections commons-el commons-httpclient commons-lang commons-logging ical4j log4j lucene lucene-snowball jsp-api mail saaj servlet)
#PACKAGES="installer mobile platform sac sis"
PACKAGES="installer sac sis"

for i in $PACKAGES
do
cd scalix-$i
install -d build
#%{__sed} -i s/com.sun.xml.messaging.saaj.soap.impl.TextImpl/com.sun.xml.internal.messaging.saaj.soap.impl.TextImpl/ caa/com/scalix/caa/soap/SOAPHelper.java
%ant -Dbuild.sysclasspath=only
cd -
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/scalix
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost

# Installer
install -d $RPM_BUILD_ROOT%{_sbindir}
install scalix-installer/dist/scalix-installer $RPM_BUILD_ROOT%{_sbindir}/scalix-installer

# SAC
install -d $RPM_BUILD_ROOT%{_datadir}/scalix/{caa-services,scalix-admin-console,scalix-res}

install %{SOURCE2} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/
install %{SOURCE3} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/
install %{SOURCE4} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/

install scalix-sac/caa/dist/caa-services.war $RPM_BUILD_ROOT%{_datadir}/scalix/caa-services
install scalix-sac/console/scalix-admin-console.war $RPM_BUILD_ROOT%{_datadir}/scalix/scalix-admin-console
install scalix-sac/res/dist/scalix-res.war $RPM_BUILD_ROOT%{_datadir}/scalix/scalix-res

# SIS
install %{SOURCE1} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-sis.xml
cp -a scalix-sis/build/war $RPM_BUILD_ROOT%{_datadir}/scalix/scalix-sis

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_datadir}/scalix

%files installer
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/scalix-installer

%files sac
%defattr(644,root,root,755)
%config(noreplace) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-caa-services.xml
%config(noreplace) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-admin-console.xml
%config(noreplace) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-res.xml
%{_datadir}/scalix/caa-services
%{_datadir}/scalix/scalix-admin-console
%{_datadir}/scalix/scalix-res

%files sis
%defattr(644,root,root,755)
%config(noreplace) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-sis.xml
%{_datadir}/scalix/scalix-sis
