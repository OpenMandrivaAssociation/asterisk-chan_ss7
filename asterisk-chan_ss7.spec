%define rname	chan_ss7
%define	version 1.2
%define	asterisk_version 1.6.1.2
%define release %mkrel %{asterisk_version}.0.0.svn.25.1

Summary:	This module adds SS7 protocol support to the Asterisk PBX
Name:		asterisk-%{rname}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.sifira.dk/chan-ss7/
# svn http://svn.dicea.dk/chan_ss7/trunk/
Source0:	%{rname}-%{version}.tar.gz
#Source0:	http://www.dicea.dk/download/%{rname}-%{version}.tar.gz
# S1,S2 is from zaptel-1.4.10.1
Source1:	mtp3d.rc
Patch0:		chan_ss7-mdv.diff
BuildRequires:	asterisk-devel = %{asterisk_version}
BuildRequires:	tonezone-devel
Requires:	asterisk = %{asterisk_version}
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}

%description
chan_ss7 is a channel driver for Asterisk that implements SS7
connectivity.

%prep

%setup -q -n %{rname}-%{version}
%patch0 -p1

sed 's/lib/lib\/asterisk/g' -i Makefile
sed 's/lib/%{_lib}/g' -i Makefile

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
	if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done
    
# fix dir perms
find . -type d | xargs chmod 755
    
# fix file perms
find . -type f | xargs chmod 644

%build

%make 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/asterisk
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_libdir}/asterisk/modules
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}

%makeinstall INSTALL_PREFIX=%{buildroot}/%{_prefix}
install -m0644 ss7.conf.template.single-link %{buildroot}%{_sysconfdir}/asterisk/ss7.conf
install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/mtp3d
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/ss7
# mtp3d config directory
MTP3CONFDIR=/etc
# Full path to mtp3d binary
MTP3DAEMON=/usr/sbin/mtp3d
# mtp3d process identificaton file
PIDFILE=/var/run/mtp3d.pid
# Please uncomment to debug
#MTP3OPTDEBUG=-d
# The log file
MTP3LOGFILE=/var/log/mtp3d.log
# Please uncomment to dump
#MTP3PDUDUMP="-m /tmp/mtp3d.pcap"
# Full path to safe_mtp3d script
SAFE_MTP3D=/sbin/safe_mtp3d

EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ASTERISK_VARIABLES COPYING NEWS README ss7.conf.*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/asterisk/ss7.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/ss7
%attr(0755,root,root) %{_libdir}/asterisk/modules/chan_ss7.so
%attr(0755,root,root) %{_initrddir}/mtp3d
%attr(0755,root,root) %{_sbindir}/mtp3d
%attr(0755,root,root) %{_sbindir}/safe_mtp3d
%attr(0755,root,root) %{_bindir}/mtp3cli
