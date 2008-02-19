# TODO
# - check what the free software means (distributable or not)
Summary:	Scalix
Name:		scalix
Version:	11.3.0
Release:	0.1
License:	Free software
Group:		Applications/WWW
Source0:	http://downloads.scalix.com/.opensource/11.3/%{name}-%{version}-source.tgz
# NoSource0-md5:	1fe0a3d817decd19823c9f04b9a3e5ae
NoSource:	0
URL:		http://www.scalix.com/community/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%prep
%setup -qc

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
