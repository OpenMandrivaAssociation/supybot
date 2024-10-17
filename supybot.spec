%define name	supybot
%define tar_name Supybot
%define version 0.83.4.1
%define plugins_date 20060723
%define release 3

Summary:	A flexible IRC bot
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/supybot/%{tar_name}-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/supybot/%{tar_name}-data.tar.bz2
Source2:	http://prdownloads.sourceforge.net/supybot/%{tar_name}-plugins-%{plugins_date}.tar.bz2
License:	BSD
Group:		Networking/IRC
URL:	    	https://supybot.sourceforge.net/
Requires:	python
Requires:	python-sqlite
BuildRequires:  pkgconfig(python)
BuildArch:      noarch

%description
Supybot is a flexible IRC bot written in python.
It features many plugins, is easy to extend and to use.

To run it, just use supybot-wizard to create the configuration file.


%package Dcc
Summary:        Supybot Dcc Plugin
Group:          Networking/IRC
Requires:       %{name} = %{version}
Requires:	python-twisted-core

%description Dcc
Supybot Dcc Plugin


%package Webserver
Summary:        Supybot Webserver Plugin
Group:          Networking/IRC
Requires:       %{name} = %{version}
Requires:	python-twisted-web

%description Webserver
Supybot Webserver Plugin


%package Sshd
Summary:        Supybot Sshd Plugin
Group:          Networking/IRC
Requires:       %{name} = %{version}
Requires:	python-twisted-conch

%description Sshd
Supybot Sshd Plugin


%package Gateway
Summary:        Supybot Gateway plugin
Group:          Networking/IRC
Requires:       %{name} = %{version}
Requires:	python-twisted-conch

%description Gateway
Supybot Gateway plugin


%package ExternalNotice
Summary:        Supybot ExternalNotice plugin
Group:          Networking/IRC
Requires:       %{name} = %{version}
Requires:	python-twisted-core

%description ExternalNotice
Supybot ExternalNotice plugin


%prep

%setup -q -n %{tar_name}-%{version}
tar -xjf %{SOURCE1}
tar -xjf %{SOURCE2}

%build
perl -pi -e 's!Download it at <http://pysqlite.sf.net/>!Install the python-sqlite package ( urpmi python-sqlite )!' plugins/*.py
CFLAGS="%{optflags}" python setup.py build

# compile plugins
python %{_libdir}/python%{py_ver}/compileall.py \
  -d %{py_puresitedir}/%{name}/plugins \
  %{tar_name}-plugins-%{plugins_date}

%install
rm -rf %{buildroot}

python setup.py install \
    --root="%{buildroot}" \
    --record="INSTALLED_FILES"
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
cp -R %{name}-data $RPM_BUILD_ROOT/%{_datadir}/%{name}

# install plugins
cp -R %{tar_name}-plugins-%{plugins_date}/* $RPM_BUILD_ROOT/%{py_puresitedir}/%{name}/plugins

%files
%doc ACKS README  RELNOTES  ChangeLog
%doc docs/GETTING_STARTED
#%doc  examples tools
%{_bindir}/*
%{py_puresitedir}/%{name}*
%{_datadir}/%{name}
%exclude %{py_puresitedir}/%{name}/plugins/Dcc
%exclude %{py_puresitedir}/%{name}/plugins/Webserver
%exclude %{py_puresitedir}/%{name}/plugins/Sshd
%exclude %{py_puresitedir}/%{name}/plugins/Gateway
%exclude %{py_puresitedir}/%{name}/plugins/ExternalNotice

%files Dcc
%{py_puresitedir}/%{name}/plugins/Dcc

%files Webserver
%{py_puresitedir}/%{name}/plugins/Webserver

%files Sshd
%{py_puresitedir}/%{name}/plugins/Sshd

%files Gateway
%{py_puresitedir}/%{name}/plugins/Gateway

%files ExternalNotice
%{py_puresitedir}/%{name}/plugins/ExternalNotice
