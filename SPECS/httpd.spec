%define contentdir %{_datadir}/httpd
%define docroot /var/www
%define mmn 20120211
%define mmnisa %{mmn}%{__isa_name}%{__isa_bits}

%define _debugsource_template %{nil}
%define debug_package %{nil}

%if 0%{?rhel} >= 7
%define vstring %(source /etc/os-release; echo ${NAME})
%else
%define vstring centos
%endif

%global mpm prefork

%define aprver 1.7.0
%define apuver 1.6.1
%define aprlibver 1
%define apulibver 1

# https://github.com/rpm-software-management/rpm/blob/master/doc/manual/conditionalbuilds

%global rpmrel 3

%if 0%{?fedora} > 35 || 0%{?rhel} > 9
%bcond_without pcre2
%bcond_with pcre
%else
%bcond_with pcre2
%bcond_without pcre
%endif

# Similar issue to https://bugzilla.redhat.com/show_bug.cgi?id=2043092
%undefine _package_note_flags

Summary: Apache HTTP Server
Name: httpd
Version: 2.4.54
Release: %{rpmrel}%{?dist}
URL: https://httpd.apache.org/
Source0: https://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2
Source1: https://www.apache.org/dist/apr/apr-%{aprver}.tar.bz2
Source2: https://www.apache.org/dist/apr/apr-util-%{apuver}.tar.bz2
Source3: httpd.logrotate
Source6: httpd.tmpfiles
Source7: httpd.service
Source8: action-graceful.sh
Source9: action-configtest.sh
Source10: server-status.conf
Source11: httpd.conf
Source13: 00-mpm.conf
Source18: 00-ssl.conf
Source22: 05-ssl.conf
Source27: 10-listen443.conf
Source28: httpd.socket
Source30: README.confd
Source31: README.confmod
Source32: httpd.service.xml
Source33: htcacheclean.service.xml
Source34: httpd.conf.xml
Source35: index.html
Source36: httpd.sysconf
Source37: httpd.init
Source40: htcacheclean.service
Source41: htcacheclean.sysconf
Source44: httpd@.service
Source45: config.layout
Source46: apachectl.sh
Source47: apachectl.xml
Source48: apache-poweredby.png

# build/scripts patches
Patch1: httpd-2.4.1-apctl.patch
Patch2: httpd-2.4.43-apxs.patch
Patch3: httpd-2.4.43-deplibs.patch
# CentOS 7
Patch6: httpd-2.4.34-apctlsystemd.patch
# CentOS 6
Patch18: httpd-2.4.25-httpd-libs.patch
# Needed for socket activation and mod_systemd patch
Patch19: httpd-2.4.53-detect-systemd.patch
# Features/functional changes
Patch21: httpd-2.4.48-r1842929+.patch
Patch22: httpd-2.4.43-mod_systemd.patch
Patch23: httpd-2.4.53-export.patch
Patch24: httpd-2.4.43-corelimit.patch
Patch25: httpd-2.4.54-selinux.patch
Patch26: httpd-2.4.43-gettid.patch
Patch27: httpd-2.4.54-icons.patch
Patch30: httpd-2.4.43-cachehardmax.patch
Patch34: httpd-2.4.43-socket-activation.patch
Patch38: httpd-2.4.43-sslciphdefault.patch
Patch39: httpd-2.4.43-sslprotdefault.patch
Patch40: httpd-2.4.43-r1861269.patch
Patch41: httpd-2.4.43-r1861793+.patch
Patch42: httpd-2.4.48-r1828172+.patch
Patch45: httpd-2.4.43-logjournal.patch
Patch46: httpd-2.4.53-separate-systemd-fns.patch

# ulimit to apachectl
Patch50: httpd-2.4.27-apct2.patch
# compile apache statically with apr and apr-util
Patch51: httpd-2.4.27-static.patch
# compile apache with bundled APR and APR-Util
Patch52: httpd-2.4.27-apr.patch
# Set POSIX Semaphores as default
Patch53: httpd-2.4.41-sem.patch
# mod_rpaf
Patch55: httpd-2.4.39-modremoteip-rpaf.patch
Patch56: httpd-2.4.52-modremoteip-ssl-tls.patch

# Bug fixes
# https://bugzilla.redhat.com/show_bug.cgi?id=1397243
Patch60: httpd-2.4.43-enable-sslv3.patch
Patch61: httpd-2.4.48-r1878890.patch
Patch63: httpd-2.4.46-htcacheclean-dont-break.patch
Patch65: httpd-2.4.51-r1894152.patch

# Security fixes

License: ASL 2.0
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf, perl, perl-generators, pkgconfig, findutils, xmlto
BuildRequires: zlib-devel, libselinux-devel
%if %{with pcre2}
BuildRequires: pcre2-devel
%endif
%if %{with pcre}
BuildRequires: pcre-devel > 5.0
%endif
BuildRequires: gcc

%if 0%{?rhel} >= 7
BuildRequires: systemd-devel
%endif

Requires: /etc/mime.types, redhat-logos
Provides: webserver
Provides: httpd-mmn = %{mmn}, httpd-mmn = %{mmnisa}
Requires: httpd-tools = %{version}-%{release}
Requires: httpd-filesystem = %{version}-%{release}
Requires(pre): httpd-filesystem

%if 0%{?rhel} >= 7
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units
%endif

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%package apr
Group: System Environment/Libraries
Summary: Apache Portable Runtime library
BuildRequires: libtool >= 1.4
Requires: httpd = %{version}-%{release}
Conflicts: apr, apr-devel

%description apr
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.

%package apr-util
Group: System Environment/Libraries
Summary: Apache Portable Runtime Utility library
BuildRequires: expat-devel
Requires: httpd = %{version}-%{release}
Requires: httpd-apr = %{version}-%{release}
Conflicts: apr-util, apr-util-devel

%description apr-util
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

%package devel
Group: Development/Libraries
Summary: Development interfaces for the Apache HTTP Server
Requires: pkgconfig, libtool
Requires: httpd = %{version}-%{release}
Requires: httpd-apr = %{version}-%{release}
Requires: httpd-apr-util = %{version}-%{release}
BuildConflicts: apr-devel
BuildConflicts: apr-util-devel

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP Server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package filesystem
Group: System Environment/Daemons
Summary: The basic directory layout for the Apache HTTP Server
BuildArch: noarch
Requires(pre): /usr/sbin/useradd

%description filesystem
The httpd-filesystem package contains the basic directory layout
for the Apache HTTP Server including the correct permissions
for the directories.

%package tools
Group: System Environment/Daemons
Summary: Tools for use with the Apache HTTP Server

%description tools
The httpd-tools package contains tools which can be used with
the Apache HTTP Server.

%package -n mod_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP Server
Epoch: 1
BuildRequires: openssl-devel
Requires(pre): httpd-filesystem
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
# mod_ssl/mod_nss cannot both be loaded simultaneously
Conflicts: mod_nss

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache HTTP
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%prep
%setup -q
%setup -q -T -D -a 1
%setup -q -T -D -a 2

# Make sure you have APR and APR-Util already installed on your system. If you
# don't, or prefer to not use the system-provided versions, download the latest
# versions of both APR and APR-Util from Apache APR, unpack them into
# /httpd_source_tree_root/srclib/apr and /httpd_source_tree_root/srclib/apr-util
# (be sure the directory names do not have version numbers; for example, the APR
# distribution must be under /httpd_source_tree_root/srclib/apr/) and use
# ./configure's --with-included-apr option.
mv apr-%{aprver} srclib/apr
mv apr-util-%{apuver} srclib/apr-util

%patch1 -p1 -b .apctl
%patch2 -p1 -b .apxs
%patch3 -p1 -b .deplibs

%if 0%{?rhel} >= 7
%patch19 -p1 -b .detectsystemd
%else
%patch18 -p1 -b .hlibs
%endif

%patch21 -p1 -b .r1842929+
%patch22 -p1 -b .mod_systemd
%patch23 -p1 -b .export
%patch24 -p1 -b .corelimit
%patch25 -p1 -b .selinux
%patch26 -p1 -b .gettid
%patch27 -p1 -b .icons

%patch30 -p1 -b .cachehardmax

%if 0%{?rhel} >= 7
%patch34 -p1 -b .socketactivation
%endif

%patch38 -p1 -b .sslciphdefault
%patch39 -p1 -b .sslprotdefault
%patch40 -p1 -b .r1861269
%patch41 -p1 -b .r1861793+
%patch42 -p1 -b .r1828172+
%patch45 -p1 -b .logjournal
%patch46 -p1 -b .separatesystemd

%patch50 -p1 -b .apct2
%patch51 -p1 -b .static
%patch52 -p1 -b .apr
%patch53 -p1 -b .sem
%patch55 -p1 -b .rpaf
%patch56 -p1 -b .rpaf

%patch60 -p1 -b .enable-sslv3
%patch61 -p1 -b .r1878890
%patch63 -p1 -b .htcacheclean-dont-break
%patch65 -p1 -b .r1894152

# Patch in the vendor string
sed -i '/^#define PLATFORM/s/Unix/%{vstring}/' os/unix/os.h

cp -p $RPM_SOURCE_DIR/server-status.conf server-status.conf

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}
   : Update the mmn macro and rebuild.
   exit 1
fi

# A new logo which comes together with a new test page
cp %{SOURCE48} ./docs/icons/apache_pb3.png

# Provide default layout
cp $RPM_SOURCE_DIR/config.layout .

sed '
s,@MPM@,%{mpm},g
s,@DOCROOT@,%{docroot},g
s,@LOGDIR@,%{_localstatedir}/log/httpd,g
' < $RPM_SOURCE_DIR/httpd.conf.xml \
    > httpd.conf.xml

xmlto man ./httpd.conf.xml
%if 0%{?rhel} >= 7
xmlto man $RPM_SOURCE_DIR/htcacheclean.service.xml
xmlto man $RPM_SOURCE_DIR/httpd.service.xml
%endif
# apachectl.xml => apachectl.8
xmlto man %{SOURCE47}

: Building with MMN %{mmn}, MMN-ISA %{mmnisa}
: Default MPM is %{mpm}, vendor string is '%{vstring}'
: Regex Engine: PCRE=%{with pcre} PCRE2=%{with pcre2}

%build
# reconfigure to enable wired minds module
./buildconf

# regenerate configure scripts
autoheader && autoconf || exit 1

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
	support/apxs.in

# -fPIC required for compilling APR and APR-Util and linking them with PIE httpd
# and tools (--enable-pie)
# https://lists.debian.org/debian-devel/2016/05/msg00309.html
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export LDFLAGS="-Wl,-z,relro,-z,now"

# httpd-2.4.25-selinux.patch adds -lselinux flag into HTTPD_LIBS which not in
# use by autotools
export LIBS="-lselinux"

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

# Build the daemon
./configure \
    --prefix=%{_sysconfdir}/httpd \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir}/httpd/conf \
    --includedir=%{_includedir}/httpd \
    --libexecdir=%{_libdir}/httpd/modules \
    --datadir=%{contentdir} \
    --enable-layout=Fedora \
    --with-installbuilddir=%{_libdir}/httpd/build \
    --enable-mpms-shared=all \
%if %{with pcre2}
    --with-pcre2=%{_bindir}/pcre2-config \
%endif
%if %{with pcre}
    --with-pcre=%{_bindir}/pcre-config \
%endif
    --enable-pie \
    --with-included-apr \
    --enable-modules=none \
    --enable-mods-static=few \
    --enable-include \
    --enable-deflate \
    --enable-expires \
    --enable-proxy \
        --enable-proxy-ftp=no \
        --enable-proxy-fcgi=no \
        --enable-proxy-scgi=no \
        --enable-proxy-fdpass=no \
        --enable-proxy-ajp=no \
        --enable-proxy-balancer=no \
        --enable-proxy-express=no \
        --enable-proxy-uwsgi=no \
        --enable-proxy-wstunnel=no \
    --enable-asis \
    --enable-cgi \
    --enable-vhost-alias \
    --enable-negotiation \
    --enable-actions \
    --enable-remoteip \
    --enable-rewrite \
    --enable-socache-shmcb \
    --enable-speling \
    --enable-substitute \
    --enable-unique-id \
    --enable-userdir \
    --enable-ssl=shared \
%if 0%{?rhel} >= 7
    --enable-systemd=static \
%endif
    --disable-reqtimeout \
    --disable-status

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%if 0%{?rhel} >= 7
# Install systemd service files (CentOS 7)
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
for s in httpd.service htcacheclean.service httpd.socket httpd@.service; do
  install -p -m 644 $RPM_SOURCE_DIR/${s} \
                    $RPM_BUILD_ROOT%{_unitdir}/${s}
done
%else
# install SYSV init stuff
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 %{SOURCE37} \
        $RPM_BUILD_ROOT/etc/rc.d/init.d/httpd
%endif

# install conf file/directory
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d
install -m 644 $RPM_SOURCE_DIR/README.confd \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/README
install -m 644 $RPM_SOURCE_DIR/README.confmod \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/README
for f in \
    00-mpm.conf 00-ssl.conf; do
    install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/$f
done

sed -i '/^#LoadModule mpm_%{mpm}_module /s/^#//' \
     $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/00-mpm.conf
touch -r $RPM_SOURCE_DIR/00-mpm.conf \
     $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/00-mpm.conf

%if 0%{?rhel} >= 7
# install systemd override drop directory
# Web application packages can drop snippets into this location if
# they need ExecStart[pre|post].
mkdir $RPM_BUILD_ROOT%{_unitdir}/httpd.service.d
mkdir $RPM_BUILD_ROOT%{_unitdir}/httpd.socket.d
install -m 644 -p $RPM_SOURCE_DIR/10-listen443.conf \
    $RPM_BUILD_ROOT%{_unitdir}/httpd.socket.d/10-listen443.conf
%endif

for f in \
    05-ssl.conf; do
    install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/$f
done

# Split-out extra config shipped as default in conf.d:
# we have single httpd.conf with all standard settings inside
#for f in autoindex; do
#  install -m 644 docs/conf/extra/httpd-${f}.conf \
#        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/${f}.conf
#done

rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/*.conf
install -m 644 -p $RPM_SOURCE_DIR/httpd.conf \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf

mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 -p $RPM_SOURCE_DIR/httpd.sysconf \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/httpd
install -m 644 -p $RPM_SOURCE_DIR/htcacheclean.sysconf \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/htcacheclean

%if 0%{?rhel} >= 7
# tmpfiles.d configuration (CentOS 7)
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 644 -p $RPM_SOURCE_DIR/httpd.tmpfiles \
    $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/httpd.conf
%endif

# Other directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/httpd
%if 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT/run/httpd/htcacheclean
%else
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/httpd/htcacheclean
%endif

# Substitute in defaults which are usually done (badly) by "make install"
sed -i \
   "/^DavLockDB/d;
    s,@@ServerRoot@@/user.passwd,/etc/httpd/conf/user.passwd,;
    s,@@ServerRoot@@/docs,%{docroot},;
    s,@@ServerRoot@@,%{docroot},;
    s,@@Port@@,80,;" \
    docs/conf/extra/*.conf

# Set correct path for httpd binary in apachectl script
sed 's,@HTTPDBIN@,%{_sbindir}/httpd,g' $RPM_SOURCE_DIR/apachectl.sh \
    > apachectl.sh

# Create cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/proxy \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/ssl

mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}

# Make the MMN accessible to module packages
echo %{mmnisa} > $RPM_BUILD_ROOT%{_includedir}/httpd/.mmn

cat > macros.httpd <<EOF
%%_httpd_mmn %{mmnisa}
%%_httpd_apxs %%{_libdir}/httpd/build/vendor-apxs
%%_httpd_modconfdir %%{_sysconfdir}/httpd/conf.modules.d
%%_httpd_confdir %%{_sysconfdir}/httpd/conf.d
%%_httpd_contentdir %{contentdir}
%%_httpd_moddir %%{_libdir}/httpd/modules
%%_httpd_requires Requires: httpd-mmn = %%{_httpd_mmn}
EOF

%if 0%{?rhel} >= 7
mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
install -m 644 -D macros.httpd \
           $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.httpd
%else
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -m 644 -c macros.httpd \
           $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.httpd
%endif


# Handle contentdir
mkdir $RPM_BUILD_ROOT%{contentdir}/noindex \
      $RPM_BUILD_ROOT%{contentdir}/server-status
ln -s ../../testpage/index.html \
       $RPM_BUILD_ROOT%{contentdir}/noindex/index.html
install -m 644 -p docs/server-status/* \
        $RPM_BUILD_ROOT%{contentdir}/server-status
rm -rf $RPM_BUILD_ROOT%{contentdir}/htdocs

# remove manual sources
find $RPM_BUILD_ROOT%{contentdir}/manual \( \
    -name \*.xml -o -name \*.xml.* -o -name \*.ent -o -name \*.xsl -o -name \*.dtd \
    \) -print0 | xargs -0 rm -f

# Strip the manual down just to English and replace the typemaps with flat files:
set +x
for f in `find $RPM_BUILD_ROOT%{contentdir}/manual -name \*.html -type f`; do
   if test -f ${f}.en; then
      cp ${f}.en ${f}
      rm ${f}.*
   fi
done
set -x

# Clean Document Root
rm -rf $RPM_BUILD_ROOT%{docroot}/html/*.html \
      $RPM_BUILD_ROOT%{docroot}/cgi-bin/*

# Symlink for the powered-by-$DISTRO image:
ln -s ../../pixmaps/poweredby.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/poweredby.png

# Symlink for the system logo
%if 0%{?rhel} >= 9
ln -s ../../pixmaps/system-noindex-logo.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/system_noindex_logo.png
%endif

# symlinks for /etc/httpd
rmdir $RPM_BUILD_ROOT/etc/httpd/{state,run}
ln -s ../..%{_localstatedir}/log/httpd $RPM_BUILD_ROOT/etc/httpd/logs
ln -s ../..%{_localstatedir}/lib/httpd $RPM_BUILD_ROOT/etc/httpd/state
%if 0%{?rhel} >= 7
ln -s /run/httpd $RPM_BUILD_ROOT/etc/httpd/run
%else
ln -s %{_localstatedir}/run/httpd $RPM_BUILD_ROOT/etc/httpd/run
%endif
ln -s ../..%{_libdir}/httpd/modules $RPM_BUILD_ROOT/etc/httpd/modules

%if 0%{?rhel} >= 7
# Install scripts
install -m 755 apachectl.sh $RPM_BUILD_ROOT%{_sbindir}/apachectl
touch -r $RPM_SOURCE_DIR/apachectl.sh $RPM_BUILD_ROOT%{_sbindir}/apachectl
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd
for f in graceful configtest; do
    install -p -m 755 $RPM_SOURCE_DIR/action-${f}.sh \
        $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd/${f}
done
%endif

# Install logrotate config
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 644 -p $RPM_SOURCE_DIR/httpd.logrotate \
	$RPM_BUILD_ROOT/etc/logrotate.d/httpd

%if 0%{?rhel} >= 7
# Install systemd service man pages (CentOS 7)
install -m 644 -p httpd.service.8 httpd.socket.8 httpd@.service.8 \
    htcacheclean.service.8 \
    $RPM_BUILD_ROOT%{_mandir}/man8
%endif
install -m 644 -p apachectl.8 $RPM_BUILD_ROOT%{_mandir}/man8

# Install man pages
install -d $RPM_BUILD_ROOT%{_mandir}/man5
install -m 644 -p httpd.conf.5 \
    $RPM_BUILD_ROOT%{_mandir}/man5

# fix man page paths
sed -e "s|/usr/local/apache2/conf/httpd.conf|/etc/httpd/conf/httpd.conf|" \
    -e "s|/usr/local/apache2/conf/mime.types|/etc/mime.types|" \
    -e "s|/usr/local/apache2/conf/magic|/etc/httpd/conf/magic|" \
    -e "s|/usr/local/apache2/logs/error_log|/var/log/httpd/error_log|" \
    -e "s|/usr/local/apache2/logs/access_log|/var/log/httpd/access_log|" \
    -e "s|/usr/local/apache2/logs/httpd.pid|/run/httpd/httpd.pid|" \
    -e "s|/usr/local/apache2|/etc/httpd|" < docs/man/httpd.8 \
  > $RPM_BUILD_ROOT%{_mandir}/man8/httpd.8

# Make ap_config_layout.h libdir-agnostic
sed -i '/.*DEFAULT_..._LIBEXECDIR/d;/DEFAULT_..._INSTALLBUILDDIR/d' \
    $RPM_BUILD_ROOT%{_includedir}/httpd/ap_config_layout.h

# Fix path to instdso in special.mk
sed -i '/instdso/s,top_srcdir,top_builddir,' \
    $RPM_BUILD_ROOT%{_libdir}/httpd/build/special.mk

# vendor-apxs uses an unsanitized config_vars.mk which may
# have dependencies on redhat-rpm-config.  apxs uses the
# config_vars.mk with a sanitized config_vars.mk
cp -p $RPM_BUILD_ROOT%{_libdir}/httpd/build/config_vars.mk \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor_config_vars.mk

# Sanitize CFLAGS & LIBTOOL in standard config_vars.mk
sed -e '/^CFLAGS/s,=.*$,= -O2 -g -Wall,' \
    -e '/^LIBTOOL/s,/.*/libtool,%{_bindir}/libtool,' \
    -i $RPM_BUILD_ROOT%{_libdir}/httpd/build/config_vars.mk
diff -u $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor_config_vars.mk \
    $RPM_BUILD_ROOT%{_libdir}/httpd/build/config_vars.mk || true

sed 's/config_vars.mk/vendor_config_vars.mk/' \
    $RPM_BUILD_ROOT%{_bindir}/apxs \
    > $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor-apxs
touch -r $RPM_BUILD_ROOT%{_bindir}/apxs \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor-apxs
chmod 755 $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor-apxs

# Remove unpackaged files
rm -vf \
      $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT/etc/httpd/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/{ap?-config,dbmmanage} \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/etc/httpd/conf/{original,extra}

%pre filesystem
getent group apache >/dev/null || groupadd -g 48 -o -r apache
getent passwd apache >/dev/null || \
  useradd -r -o -u 48 -g apache -s /sbin/nologin \
    -d %{contentdir} -c "Apache" apache

%post
%if 0%{?rhel} >= 7
%systemd_post httpd.service htcacheclean.service httpd.socket
%else
/sbin/chkconfig --add httpd
%endif

%preun
%if 0%{?rhel} >= 7
%systemd_preun httpd.service htcacheclean.service httpd.socket
%else
if [ $1 = 0 ]; then
        /sbin/service httpd stop > /dev/null 2>&1
        /sbin/chkconfig --del httpd
fi
%endif

%postun
%if 0%{?rhel} >= 7
%systemd_postun httpd.service htcacheclean.service httpd.socket
%endif

# disabled while SysV not configured
%posttrans
%if 0%{?rhel} >= 7
test -f /etc/sysconfig/httpd-disable-posttrans || \
    /bin/systemctl try-restart --no-block httpd.service htcacheclean.service >/dev/null 2>&1 || :
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%doc ABOUT_APACHE README CHANGES LICENSE VERSIONING NOTICE
%doc docs/conf/extra/*.conf
%doc server-status.conf

%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/state
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic

%config(noreplace) %{_sysconfdir}/logrotate.d/httpd

%dir %{_sysconfdir}/httpd/conf.modules.d
%{_sysconfdir}/httpd/conf.modules.d/README
%{_sysconfdir}/httpd/conf.modules.d/00-mpm.conf

%config(noreplace) %{_sysconfdir}/sysconfig/htcacheclean
%config(noreplace) %{_sysconfdir}/sysconfig/httpd

%if 0%{?rhel} >= 7
%{_prefix}/lib/tmpfiles.d/httpd.conf
%dir %{_libexecdir}/initscripts/legacy-actions/httpd
%{_libexecdir}/initscripts/legacy-actions/httpd/*
%endif

%{_sbindir}/ht*
%{_sbindir}/fcgistarter
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_libdir}/httpd/modules/mod_mpm_*.so

%dir %{contentdir}/error
%dir %{contentdir}/error/include
%dir %{contentdir}/noindex
%dir %{contentdir}/server-status
%{contentdir}/icons/*
%{contentdir}/error/README
%{contentdir}/error/*.var
%{contentdir}/error/include/*.html
%{contentdir}/noindex/index.html
%{contentdir}/server-status/*
%if 0%{?rhel} >= 7
%attr(0710,root,apache) %dir /run/httpd
%attr(0700,apache,apache) %dir /run/httpd/htcacheclean
%else
%attr(0710,root,apache) %dir %{_localstatedir}/run/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/run/httpd/htcacheclean
%endif
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/lib/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd/proxy
%{_mandir}/man8/*
%{_mandir}/man5/*

%if 0%{?rhel} >= 7
%{_unitdir}/httpd.service
%{_unitdir}/httpd@.service
%{_unitdir}/htcacheclean.service
%{_unitdir}/*.socket
%else
%{_sysconfdir}/rc.d/init.d/httpd
%endif
# skip manual packaging (Mon Aug 21 2017 - aursu)
%exclude %{contentdir}/manual

%files filesystem
%dir %{_sysconfdir}/httpd
%dir %{_sysconfdir}/httpd/conf.d
%{_sysconfdir}/httpd/conf.d/README
%dir %{docroot}
%dir %{docroot}/cgi-bin
%dir %{docroot}/html
%dir %{contentdir}
%dir %{contentdir}/icons
%if 0%{?rhel} >= 7
%attr(755,root,root) %dir %{_unitdir}/httpd.service.d
%attr(755,root,root) %dir %{_unitdir}/httpd.socket.d
%endif

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%doc LICENSE NOTICE
%exclude %{_bindir}/apxs
%exclude %{_mandir}/man1/apxs.1*

%files apr
%defattr(-,root,root,-)
%{_libdir}/libapr-%{aprlibver}.so.*
%{_bindir}/apr-%{aprlibver}-config
%{_libdir}/libapr-%{aprlibver}.*a
%{_libdir}/libapr-%{aprlibver}.so
%{_libdir}/pkgconfig/apr-%{aprlibver}.pc
%dir %{_libdir}/apr-%{aprlibver}
%dir %{_libdir}/apr-%{aprlibver}/build
%{_libdir}/apr-%{aprlibver}/build/*
%dir %{_includedir}/apr-%{aprlibver}
%{_includedir}/apr-%{aprlibver}/*.h

%files apr-util
%defattr(-,root,root,-)
%{_libdir}/libaprutil-%{apulibver}.so.*
%{_bindir}/apu-%{apulibver}-config
%{_libdir}/libaprutil-%{apulibver}.*a
%{_libdir}/libaprutil-%{apulibver}.so
%{_libdir}/pkgconfig/apr-util-%{apulibver}.pc
%{_libdir}/apr-util-%{apulibver}/apr_crypto_openssl*

%files -n mod_ssl
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/05-ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/httpd/ssl
%if 0%{?rhel} >= 7
%{_unitdir}/httpd.socket.d/10-listen443.conf
%endif

%files devel
%defattr(-,root,root)
%{_includedir}/httpd
%{_bindir}/apxs
%{_mandir}/man1/apxs.1*
%dir %{_libdir}/httpd/build
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/*.sh
%{_libdir}/httpd/build/vendor-apxs
%if 0%{?rhel} >= 7
%{_rpmconfigdir}/macros.d/macros.httpd
%else
%{_sysconfdir}/rpm/macros.httpd
%endif

%changelog
* Fri Jun 17 2022 Joe Orton <jorton@redhat.com> - 2.4.54-3
- update PCRE config selection

* Thu Jun 09 2022 Luboš Uhliarik <luhliari@redhat.com> - 2.4.54-2
- new version 2.4.54

* Mon May 16 2022 Joe Orton <jorton@redhat.com> - 2.4.53-7
- disable package notes

* Wed Apr 20 2022 Joe Orton <jorton@redhat.com> - 2.4.53-4
- switch to PCRE2 for new releases

* Wed Dec 22 2021 Joe Orton <jorton@redhat.com> - 2.4.52-1
- update to 2.4.52

* Mon Dec 06 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.4.51-3
- Use NAME from os-release(5) for vendor string
  Related: #2029071 - httpd on CentOS identifies as RHEL

* Tue Oct 12 2021 Joe Orton <jorton@redhat.com> - 2.4.51-2
- mod_ssl: updated patch for OpenSSL 3.0 compatibility (#2007178)
- mod_deflate/core: add two brigade handling correctness fixes

* Wed Jun 02 2021 Luboš Uhliarik <luhliari@redhat.com> - 2.4.48-1
- new version 2.4.48
- Resolves: #1964746 - httpd-2.4.48 is available

* Fri May 21 2021 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.46-14
- added rpaf patches for remoteip module

* Mon May 03 2021 Lubos Uhliarik <luhliari@redhat.com> - 2.4.46-13
- Related: #1934739 - Apache trademark update - new logo

* Fri Apr  9 2021 Joe Orton <jorton@redhat.com> - 2.4.46-12
- use OOMPolicy=continue in httpd.service, httpd@.service (#1947475)

* Tue Feb 23 2021 Joe Orton <jorton@redhat.com> - 2.4.46-10
- add Conflicts: with mod_nss
- drop use of apr_ldap_rebind (r1878890, #1847585)

* Mon Feb 01 2021 Lubos Uhliarik <luhliari@redhat.com> - 2.4.46-9
- Resolves: #1914182 - RFE: CustomLog should be able to use journald

* Wed Jan 20 2021 Artem Egorenkov <aegorenk@redhat.com> - 2.4.46-7
- prevent htcacheclean from while break when first file processed

* Fri Nov  6 2020 Joe Orton <jorton@redhat.com> - 2.4.46-5
- add %%_httpd_requires to macros

* Thu Aug 27 2020 Joe Orton <jorton@redhat.com> - 2.4.46-3
- strip /usr/bin/apxs CFLAGS further

* Thu Aug 27 2020 Joe Orton <jorton@redhat.com> - 2.4.46-2
- sanitize CFLAGS used by /usr/bin/apxs by default (#1873020)
- add $libdir/httpd/build/vendor-apxs which exposes full CFLAGS
- redefine _httpd_apxs RPM macro to use vendor-apxs
- added MPM event and worker
- made MPM prefork shared

* Tue Aug 25 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.46-1
- new version 2.4.46
- remove obsolete parts of this spec file
- fix systemd detection patch

* Thu Jul  9 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.43-6
- fix macro in mod_lua for lua 4.5

* Thu Jul  9 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.43-5
- Remove %ghosted /etc/sysconfig/httpd file (#1850082)

* Tue Jul  7 2020 Joe Orton <jorton@redhat.com> - 2.4.43-4
- use gettid() directly and use it for built-in ErrorLogFormat

* Fri Apr 17 2020 Joe Orton <jorton@redhat.com> - 2.4.43-3
- mod_ssl: updated coalescing filter to improve TLS efficiency

* Fri Apr 17 2020 Joe Orton <jorton@redhat.com> - 2.4.43-2
- mod_ssl: fix leak in OCSP stapling code (PR 63687, r1876548)
- mod_systemd: restore descriptive startup logging

* Tue Mar 31 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.43-1
- new version 2.4.43 (#1819023)

* Mon Jan 20 2020 Joe Orton <jorton@redhat.com> - 2.4.41-12
- mod_systemd: fix timeouts on reload w/ExtendedStatus off (#1590877)

* Mon Jan  6 2020 Joe Orton <jorton@redhat.com> - 2.4.41-11
- apachectl(8): update authors

* Sat Dec  7 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 2.4.41-10
- apachectl: Add man page for Fedora version

* Thu Nov 21 2019 Joe Orton <jorton@redhat.com> - 2.4.41-9
- mod_ssl: fix request body buffering w/TLSv1.3 PHA (#1775146)

* Wed Nov 13 2019 Joe Orton <jorton@redhat.com> - 2.4.41-8
- apachectl: in graceful/graceful-stop, only signal main process (#1758798)

* Fri Oct  4 2019 Joe Orton <jorton@redhat.com> - 2.4.41-6
- mod_cgid/mod_cgi: further upstream consolidation patches

* Thu Oct  3 2019 Joe Orton <jorton@redhat.com> - 2.4.41-5
- mod_proxy_balancer: fix balancer-manager XSRF check (PR 63688)

* Wed Oct  2 2019 Joe Orton <jorton@redhat.com> - 2.4.41-4
- mod_cgid: possible stdout timeout handling fix (#1757683)

* Wed Oct  2 2019 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.41-3
- enable SSL/EVP support for included APR

* Thu Aug 15 2019 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.41-2
- upgrade APR to version 1.7.0

* Thu Aug 15 2019 Joe Orton <jorton@redhat.com> - 2.4.41-1
- update to 2.4.41

* Thu Apr  4 2019 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.39-3
- upgrade APR to version 1.6.5

* Tue Apr  2 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.39-1
- update to 2.4.39

* Thu Feb 28 2019 Joe Orton <jorton@redhat.com> - 2.4.38-6
- apachectl: cleanup and replace script wholesale (#1641237)
 * drop "apachectl fullstatus" support
 * run systemctl with --no-pager option
 * implement graceful&graceful-stop by signal directly
- run "httpd -t" from legacy action script

* Tue Feb  5 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.38-5
- segmentation fault fix (FIPS)

* Tue Feb  5 2019 Joe Orton <jorton@redhat.com> - 2.4.38-4
- use serverroot-relative statedir, rundir by default

* Fri Feb  1 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.38-2
- new version 2.4.38 (#1668125)

* Mon Dec 10 2018 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.37-6
- added mod_systemd into CentOS 7 build

* Fri Nov 23 2018 Lubos Uhliarik <luhliari@redhat.com> - 2.4.37-5
- Resolves: #1652678 - TLS connection allowed while all protocols are forbidden

* Thu Nov  8 2018 Joe Orton <jorton@redhat.com> - 2.4.37-4
- add httpd.conf(5) (#1611361)

* Wed Nov  7 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.37-3
- Resolves: #1647241 - fix apachectl script

* Wed Oct 31 2018 Joe Orton <jorton@redhat.com> - 2.4.37-2
- add DefaultStateDir/ap_state_dir_relative()
- mod_dav_fs: use state dir for default DAVLockDB
- mod_md: use state dir for default MDStoreDir

* Wed Oct 31 2018 Joe Orton <jorton@redhat.com> - 2.4.37-1
- update to 2.4.37

* Wed Oct 31 2018 Joe Orton <jorton@redhat.com> - 2.4.34-11
- add htcacheclean.service(8) man page

* Fri Sep 28 2018 Joe Orton <jorton@redhat.com> - 2.4.34-10
- apachectl: don't read /etc/sysconfig/httpd

* Tue Sep 25 2018 Joe Orton <jorton@redhat.com> - 2.4.34-9
- fix build if OpenSSL built w/o SSLv3 support

* Fri Sep 21 2018 Joe Orton <jorton@redhat.com> - 2.4.34-8
- comment-out SSLProtocol, SSLProxyProtocol from ssl.conf in
  default configuration; now follow OpenSSL system default (#1468322)

* Fri Sep 21 2018 Joe Orton <jorton@redhat.com> - 2.4.34-7
- mod_ssl: follow OpenSSL protocol defaults if SSLProtocol
  is not configured (Rob Crittenden, #1618371)

* Tue Aug 28 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.34-6
- mod_ssl: enable SSLv3 and change behavior of "SSLProtocol All"
  configuration (#1624777)

* Tue Aug 21 2018 Joe Orton <jorton@redhat.com> - 2.4.34-5
- mod_ssl: further TLSv1.3 fix (#1619389)

* Mon Aug 13 2018 Joe Orton <jorton@redhat.com> - 2.4.34-4
- mod_ssl: backport TLSv1.3 support changes from upstream (#1615059)

* Fri Jul 20 2018 Joe Orton <jorton@redhat.com> - 2.4.34-3
- mod_ssl: fix OCSP regression (upstream r1555631)

* Wed Jul 18 2018 Joe Orton <jorton@redhat.com> - 2.4.34-1
- update to 2.4.34 (#1601160)

* Mon Jul 16 2018 Joe Orton <jorton@redhat.com> - 2.4.33-10
- don't block on service try-restart in posttrans scriptlet
- add Lua-based /server-status example page to docs

* Tue Jul 10 2018 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.33-5
- add httpd@.service; update httpd.service(8) and add new stub
- mod_md: change hard-coded default MdStoreDir to state/md (#1563846)
- updated APR and Apr-Util libraries

* Mon May 28 2018 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.33-1
- mod_ssl: drop implicit 'SSLEngine on' for vhost w/o certs (#1564537)

* Fri Jan 05 2018 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.29-3
- fixed pid file location for CentOS 6
- fixed default httpd.conf

* Tue Oct 31 2017 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.29-2
- fixed rebuild script call

* Wed Oct 25 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.29-1
- new version 2.4.29

* Mon Oct  9 2017 Joe Orton <jorton@redhat.com> - 2.4.27-7
- move httpd.service.d, httpd.socket.d dirs to -filesystem
- add new content-length filter (upstream PR 61222)
- update mod_systemd (r1802251)

* Fri Sep 22 2017 Joe Orton <jorton@redhat.com> - 2.4.27-13
- drop Requires(post) for mod_ssl

* Tue Sep 12 2017 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.27-2
- disabled proxy balancer and protocols SCGI, AJP and FTP

* Mon Sep 11 2017 Alexander Ursu <alexander.ursu@gmail.com> - 2.4.27-1
- configured according to Apache 2.2 configuration

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild
