Summary:	Scalix
Name:		scalix
Version:	11.3.0
Release:	0.1
# http://www.scalix.com/community/opensource/licensing.php
License:	Scalix Public License (SPL)
Group:		Applications/WWW
Source0:	http://downloads.scalix.com/.opensource/11.3/%{name}-%{version}-source.tgz
# Source0-md5:	1fe0a3d817decd19823c9f04b9a3e5ae
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
