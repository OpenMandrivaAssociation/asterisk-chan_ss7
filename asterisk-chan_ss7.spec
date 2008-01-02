%define rname	chan_ss7

Summary:	This module adds SS7 protocol support to the Asterisk PBX
Name:		asterisk-%{rname}
Version:	0.8.4
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://www.sifira.dk/chan-ss7/
Source0:	http://www.sifira.dk/chan-ss7/0.8.2/%{rname}-%{version}.tar.bz2
Patch0:		chan_ss7-0.8-missing_headers.diff
BuildRequires:	asterisk-devel >= 1.2
Requires:	asterisk >= 1.2
Buildroot:	%{_tmppath}/%{name}-%{version}

%description
chan_ss7 is a channel driver for Asterisk that implements SS7
connectivity.

%prep

%setup -q -n %{rname}-%{version}
%patch0 -p1

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done
    
# fix dir perms
find . -type d | xargs chmod 755
    
# fix file perms
find . -type f | xargs chmod 644

%build

make CFLAGS="%{optflags} -pipe -Wall -fPIC -DPIC -D_REENTRANT -D_GNU_SOURCE"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/asterisk
install -d %{buildroot}%{_libdir}/asterisk

install -m0644 ss7.conf.template.single-link %{buildroot}%{_sysconfdir}/asterisk/ss7.conf
install -m0755 chan_ss7.so %{buildroot}%{_libdir}/asterisk/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ANNOUNCE COPYING INSTALL README ss7.conf.*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/asterisk/ss7.conf
%attr(0755,root,root) %{_libdir}/asterisk/chan_ss7.so

