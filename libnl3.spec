Summary: Convenience library for kernel netlink sockets
Group: Development/Libraries
License: LGPLv2
Name: libnl3
Version: 3.2.21
Release: 8%{?dist}
URL: http://www.infradead.org/~tgr/libnl/
Source: http://www.infradead.org/~tgr/libnl/files/libnl-%{version}.tar.gz
Source1: http://www.infradead.org/~tgr/libnl/files/libnl-doc-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: flex bison
BuildRequires: python
Patch0: rh1057024_ifa_flags_1.patch
Patch1: rh1057024_ifa_flags_2.patch
Patch2: rh1057024_ifa_flags_3.patch
Patch3: rh1040626-nl-Increase-receive-buffer-size-to-4-pages.patch
Patch4: 0004-add-nl_has_capability.patch
Patch5: 0005-rtnl_route_build_msg-set-scope.patch
Patch6: 0006-nl_msec2str-fix.patch
Patch7: 0007-relax-parsing-protinfo.patch
Patch8: 0008-add-private-header-can-netlink-h.patch
Patch9: 0009-get-kernel-nle-opnotsupp-rh1168915.patch

%description
This package contains a convenience library to simplify
using the Linux kernel's netlink sockets interface for
network manipulation

%package devel
Summary: Libraries and headers for using libnl3
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-cli = %{version}-%{release}
Requires: kernel-headers

%description devel
This package contains various headers for using libnl3

%package cli
Summary: Command line interface utils for libnl3
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description cli
This package contains various libnl3 utils and additional
libraries on which they depend

%package doc
Summary: API documentation for libnl3
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
This package contains libnl3 API documentation

%prep
%setup -q -n libnl-%{version}
%patch0 -p1 -b .0000-rh1057024_ifa_flags_1.orig
%patch1 -p1 -b .0001-rh1057024_ifa_flags_2.orig
%patch2 -p1 -b .0002-rh1057024_ifa_flags_3.orig
%patch3 -p1 -b .0003-rh1040626.orig
%patch4 -p1 -b .0004-add-nl_has_capability.orig
%patch5 -p1 -b .0005-rtnl_route_build_msg-set-scope.orig
%patch6 -p1 -b .0006-nl_msec2str-fix.orig
%patch7 -p1 -b .0007-relax-parsing-protinfo.orig
%patch8 -p1 -b .0008-add-private-header-can-netlink-h.orig
%patch9 -p1

tar -xzf %SOURCE1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name \*.la -delete

%post -p /sbin/ldconfig
%post cli -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%postun cli -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%exclude %{_libdir}/libnl-cli*.so.*
%{_libdir}/libnl-*.so.*
%config(noreplace) %{_sysconfdir}/*

%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_includedir}/libnl3/netlink/
%dir %{_includedir}/libnl3/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files cli
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libnl-cli*.so.*
%{_libdir}/libnl/
%{_sbindir}/*
%{_mandir}/man8/* 

%files doc
%defattr(-,root,root,-)
%doc COPYING
%doc libnl-doc-%{version}/*.html
%doc libnl-doc-%{version}/*.css
%doc libnl-doc-%{version}/stylesheets/*
%doc libnl-doc-%{version}/images/*
%doc libnl-doc-%{version}/images/icons/*
%doc libnl-doc-%{version}/images/icons/callouts/*
%doc libnl-doc-%{version}/api/*

%changelog
* Sun Nov 22 2015 Thomas Haller <thaller@redhat.com> - 3.2.21-8
- properly return NLE_OPNOTSUPP on rtnl_link_get_kernel() failure (rh #1168915)

* Tue Apr 29 2014 Thomas Haller <thaller@redhat.com> - 3.2.21-7
- Add local header file linux/can/netlink.h to build on rhel-6

* Fri Mar 21 2014 Thomas Haller <thaller@redhat.com> - 3.2.21-6
- fix rtnl_link_get_stat() for IPSTATS_MIB_* after kernel API breakage
- fix parsing IFLA_PROTINFO which broke on older kernels (rh #1062533)
- fix printing in nl_msec2str for whole seconds
- don't reset route scope in rtnl_route_build_msg if set to RT_SCOPE_NOWHERE
- backport nl_has_capability function

* Wed Feb 26 2014 Thomas Graf <tgraf@redhat.com> - 3.2.21-5
- nl-Increase-receive-buffer-size-to-4-pages.patch (rh #1040626)

* Tue Jan 28 2014 Daniel Mach <dmach@redhat.com> - 3.2.21-4
- Mass rebuild 2014-01-24

* Fri Jan 24 2014 Thomas Haller <thaller@redhat.com> - 3.2.21-3
- Backport extended IPv6 address flags (rh #1057024)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.2.21-2
- Mass rebuild 2013-12-27

* Fri Jan 25 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.21-1
- Update to 3.2.21

* Wed Jan 23 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.20-1
- Update to 3.2.20

* Sun Jan 20 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.19-2
- Age fix

* Thu Jan 17 2013 Jiri Pirko <jpirko@redhat.com> - 3.2.19-1
- Update to 3.2.19

* Tue Oct 30 2012 Dan Williams <dcbw@redhat.com> - 3.2.14-1
- Update to 3.2.14

* Mon Sep 17 2012 Dan Williams <dcbw@redhat.com> - 3.2.13-1
- Update to 3.2.13

* Fri Feb 10 2012 Dan Williams <dcbw@redhat.com> - 3.2.7-1
- Update to 3.2.7

* Tue Jan 17 2012 Jiri Pirko <jpirko@redhat.com> - 3.2.6-1
- Initial build
