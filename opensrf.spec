# TODO
# - FHS
# - pld deps
# - can't build itself: /usr/bin/ld: cannot find -lopensrf
Summary:	OpenSRF Message Routing Network
Name:		opensrf
Version:	2.0.1
Release:	0.1
License:	GPL 2+
Group:		Development/Libraries
URL:		http://www.evergreen-ils.org/opensrf.php
Source0:	http://evergreen-ils.org/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	3d3baa4f43817cc9c18bc780d57021f6
Source1:	ejabberd.patch
Patch0:		%{name}-apache.patch
Patch1:		%{name}-perl.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	check
BuildRequires:	check-devel
#BuildRequires:	ejabberd
BuildRequires:	expat-devel
BuildRequires:	gcc
BuildRequires:	gdbm-devel
#BuildRequires:	httpd
#BuildRequires:	httpd-devel
BuildRequires:	less
BuildRequires:	libgcrypt-devel
BuildRequires:	libmemcached
BuildRequires:	libmemcached-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
#BuildRequires:	libxml2-python
BuildRequires:	libxslt-devel
#BuildRequires:	memcached
#BuildRequires:	mod_perl
#BuildRequires:	perl-Cache-Memcached
#BuildRequires:	perl-Class-DBI
#BuildRequires:	perl-Class-DBI-AbstractSearch
#BuildRequires:	perl-Class-DBI-SQLite
#BuildRequires:	perl-DateTime-Format-Builder
#BuildRequires:	perl-DateTime-Format-ISO8601
#BuildRequires:	perl-DateTime-Format-Mail
#BuildRequires:	perl-DateTime-Set
#BuildRequires:	perl-Error
#BuildRequires:	perl-File-Find-Rule
#BuildRequires:	perl-JSON-XS
#BuildRequires:	perl-Log-Log4perl
#BuildRequires:	perl-Module-Build
#BuildRequires:	perl-Net-Jabber
#BuildRequires:	perl-Net-Server
#BuildRequires:	perl-RPC-XML
#BuildRequires:	perl-SQL-Abstract-Limit
#BuildRequires:	perl-Template-Toolkit
#BuildRequires:	perl-Test-Deep
#BuildRequires:	perl-Test-Exception
#BuildRequires:	perl-Test-Pod
#BuildRequires:	perl-Tie-IxHash
#BuildRequires:	perl-UNIVERSAL-require
#BuildRequires:	perl-Unix-Syslog
#BuildRequires:	perl-XML-LibXML
#BuildRequires:	perl-XML-LibXSLT
#BuildRequires:	perl-XML-Simple
BuildRequires:	perl-devel
#BuildRequires:	perl-libwww-perl
#BuildRequires:	psmisc
#BuildRequires:	python-devel
#BuildRequires:	python-dns
#BuildRequires:	python-memcached
#BuildRequires:	python-setuptools
#BuildRequires:	python-simplejson
BuildRequires:	readline-devel
Requires:	ejabberd
Requires:	expat
Requires:	expat-devel
Requires:	gcc
Requires:	gdbm
#Requires:	httpd
Requires:	less
Requires:	libgcrypt
Requires:	libmemcached
Requires:	libtool
Requires:	libxml2
Requires:	libxml2-python
Requires:	libxslt
Requires:	memcached
#Requires:	mod_perl
Requires:	perl-Cache-Memcached
Requires:	perl-Class-DBI
Requires:	perl-Class-DBI-AbstractSearch
Requires:	perl-Class-DBI-SQLite
Requires:	perl-DateTime-Format-Builder
Requires:	perl-DateTime-Format-ISO8601
Requires:	perl-DateTime-Format-Mail
Requires:	perl-DateTime-Set
Requires:	perl-Error
Requires:	perl-File-Find-Rule
Requires:	perl-JSON-XS
Requires:	perl-Log-Log4perl
Requires:	perl-Module-Build
Requires:	perl-Net-Jabber
Requires:	perl-Net-Server
Requires:	perl-RPC-XML
Requires:	perl-SQL-Abstract-Limit
Requires:	perl-Template-Toolkit
Requires:	perl-Test-Deep
Requires:	perl-Test-Exception
Requires:	perl-Test-Pod
Requires:	perl-Tie-IxHash
Requires:	perl-UNIVERSAL-require
Requires:	perl-Unix-Syslog
Requires:	perl-XML-LibXML
Requires:	perl-XML-LibXSLT
Requires:	perl-XML-Simple
Requires:	perl-devel
Requires:	perl-libwww-perl
Requires:	psmisc
Requires:	python
Requires:	python-dns
Requires:	python-memcached
Requires:	python-setuptools
Requires:	python-simplejson
Requires:	readline
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open Service Request Framework (OpenSRF, pronounced "open surf")
OpenSRF is a message routing network that offers scalability and
failover support for individual services and entire servers with
minimal development and deployment overhead.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./autogen.sh
./configure \
	--prefix=/opensrf \
	--sysconfdir=/opensrf/conf
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/opensrf/var/log $RPM_BUILD_ROOT/opensrf/var/run $RPM_BUILD_ROOT/opensrf/var/lock
install -Dm644 %{_sourcedir}/ejabberd.patch $RPM_BUILD_ROOT%{_sysconfdir}/ejabberd/opensrf.patch
install -Dm755 %{_sourcedir}/opensrf.init $RPM_BUILD_ROOT%{_initrddir}/opensrf
install -d "$RPM_BUILD_ROOT/opensrf/var/log" "$RPM_BUILD_ROOT/opensrf/var/run" "$RPM_BUILD_ROOT/opensrf/var/lock"

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
%post
/sbin/chkconfig --add opensrf
HFQDN=$(perl -MNet::Domain -e 'print Net::Domain::hostfqdn() . "\n";')
HOSTS_FILE_TAG="OPENSRF_RPM Addresses"
if ! grep -q "$HOSTS_FILE_TAG" %{_sysconfdir}/hosts; then
	cp -f %{_sysconfdir}/hosts %{_sysconfdir}/hosts.orig
	sed -i "\$a\#$HOSTS_FILE_TAG" %{_sysconfdir}/hosts
	sed -i "\$a\127.0.1.2\tpublic.$HFQDN\tpublic #OPENSRF_RPM" %{_sysconfdir}/hosts
	sed -i "\$a\127.0.1.3\tprivate.$HFQDN\tprivate #OPENSRF_RPM" %{_sysconfdir}/hosts
fi
if ! grep -q "^opensrf:" %{_sysconfdir}/passwd; then
	useradd -m -s /bin/bash opensrf
fi
if ! grep -q "/opensrf/bin" /home/opensrf/.bashrc; then
	sed -i "\$a\export PATH=/opensrf/bin:\$PATH" /home/opensrf/.bashrc
fi

patch -N -p1 %{_sysconfdir}/ejabberd/ejabberd.cfg < %{_sysconfdir}/ejabberd/opensrf.patch

###/etc/init.d/ejabberd restart
###sleep 5
ejabberdctl --node ejabberd@`hostname -s` register router private.localhost password
ejabberdctl --node ejabberd@`hostname -s` register opensrf private.localhost password
ejabberdctl --node ejabberd@`hostname -s` register router public.localhost password
ejabberdctl --node ejabberd@`hostname -s` register opensrf public.localhost password
ldconfig
su - opensrf -c "cp /opensrf/conf/srfsh.xml.example /home/opensrf/.srfsh.xml"
cp /opensrf/conf/opensrf.xml.example /opensrf/conf/opensrf.xml
cp /opensrf/conf/opensrf_core.xml.example /opensrf/conf/opensrf_core.xml
cp /opensrf/conf/srfsh.xml.example /opensrf/conf/srfsh.xml
chown -R opensrf:opensrf /opensrf
%endif

%files
%defattr(644,root,root,755)
%doc README LICENSE.txt
/opensrf
%{_sysconfdir}/ejabberd/opensrf.patch
%{_initrddir}/*
%{_libdir}/httpd/modules/*
%{perl_vendorlib}/*
%{_libdir}/perl5/vendor_perl/auto/OpenSRF/.packlist
%{_mandir}/man3/*
