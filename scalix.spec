# TODO:
# - add PLD as Supported distro for installer
# - package spring framework: http://springsource.org
# - after packaging spring, use it instead of interla spring.jar from scalix
# - descriptions/summaries
#
# Conditional build:
%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif
#
%include        /usr/lib/rpm/macros.java
Summary:	Scalix Collaboration Platform
Name:		scalix
Version:	11.4.3
Release:	0.1
# http://www.scalix.com/community/opensource/licensing.php
License:	Scalix Public License (SPL)
Group:		Applications/WWW
Source0:	http://downloads.scalix.com/.opensource/11.4.3/%{name}-%{version}-GA-source.tgz
# Source0-md5:	fb4794f841319ed07605a8619e5a9c36
Source1:	%{name}-sis-context.xml
Source2:	%{name}-caa-services-context.xml
Source3:	%{name}-admin-console-context.xml
Source4:	%{name}-res-context.xml
Source5:	%{name}-mobile-context.xml
Patch0:		%{name}-python25_26.patch
Patch1:		%{name}-merlin-fixes.patch
URL:		http://www.scalix.com/community/
BuildRequires:	ant >= 1.6.5
BuildRequires:	ant-junit
BuildRequires:	ant-nodeps
BuildRequires:	antlr >= 2.7.6
BuildRequires:	apache-tomcat-jasper
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
BuildRequires:	java-jdom
BuildRequires:	java-log4j
BuildRequires:	java-lucene-contrib
BuildRequires:	java-mail
BuildRequires:	java-saaj
BuildRequires:	java-servletapi5
%{?with_java_sun:BuildRequires: java-sun}
BuildRequires:	java-xerces
BuildRequires:	python-devel >= 2.2.2
BuildRequires:	rpm >= 4.4.9-56
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scalix Collaboration Platform is a robust, enterprise-class email and
group calendaring solution that is the open alternative to Exchange.
It integrates via open standards with your existing and future
messaging clients, infrastructure, and applications, protecting your
investments and giving you choice. It provides full-feature support of
Outlook and is directory agnostic.

The Scalix Server, providing comprehensive messaging with email, group
calendaring, contacts, tasks, and shared public folders, Scalix Proxy
Folders as well as a native Linux file system for your message store.

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
Requires:	%{name} = %{version}-%{release}

%description sac
SAC for Scalix

%package sis
Summary:	Scalix SIS
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

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

%build
required_jars="
	activation antlr asm2 commons-cli commons-codec commons-collections commons-el
	commons-httpclient commons-lang commons-logging ical4j log4j lucene lucene-snowball jasper-compiler
	jasper-runtime jdom jsp-api mail saaj servlet xalan xercesImpl
"
CLASSPATH=caa/build/WEB-INF/classes:res/build/WEB-INF/classes:lib/spring.jar:lib/hibernate3.jar:lib/c3p0-0.9.1.jar:$(build-classpath $required_jars)

PACKAGES="installer mobile platform sac sis"

for i in $PACKAGES; do
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

# Mobile
install -d $RPM_BUILD_ROOT%{_datadir}/scalix/scalix-mobile
install %{SOURCE5} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/
install scalix-mobile/build/scalix-mobile.war $RPM_BUILD_ROOT%{_datadir}/scalix/scalix-mobile

# SAC
install -d $RPM_BUILD_ROOT%{_datadir}/scalix/{caa-services,scalix-admin-console,scalix-res}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-caa-services.xml
install %{SOURCE3} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-admin-console.xml
install %{SOURCE4} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-res.xml
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

%files mobile
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-mobile.xml
%{_datadir}/scalix/scalix-mobile

%files sac
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-caa-services.xml
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-admin-console.xml
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-res.xml
%{_datadir}/scalix/caa-services
%{_datadir}/scalix/scalix-admin-console
%{_datadir}/scalix/scalix-res

%files sis
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/scalix-sis.xml
%{_datadir}/scalix/scalix-sis
