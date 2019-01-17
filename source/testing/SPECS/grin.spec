# GRIM - a digital currency implementing Mimblewimble - full node and wallet
# Reference implementation
# vim:tw=0:ts=2:sw=2:et:
#
# This is the rpm spec for building a Grim client and full node.
#
# Packages built:
# * grin
# * grin-debuginfo (not always/often built)
#
# DISCLAIMER:
# This RPM spec file is a work in progress (the dash references here and there
# are because this was originally templated from my dashcore RPM specfile)
#
# Enjoy. -t0dd

# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

Name: grin
Summary: Peer-to-peer digital currency implementing mimblewimble (wallet and node)


%define targetIsProduction 0

# ARCHIVE QUALIFIER - edit this if applies
# ie. if the dev team includes things like rc3 in the filename
%define archiveQualifier rc1
%define includeArchiveQualifier 0

# VERSION - edit this
%define vermajor 1.0
%define verminor 0
Version: %{vermajor}.%{verminor}

# RELEASE - edit this
# package release, and potentially extrarel
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.1
%endif

# MINORBUMP - edit this
# builder's initials and often a numeral for very small or rapid iterations
# taw, taw0, taw1, etc.
%define minorbump taw

#
# Build the release string - don't edit this
#

%define snapinfo testing
%if %{includeArchiveQualifier}
  %define snapinfo %{archiveQualifier}
  %if %{targetIsProduction}
    %undefine snapinfo
  %endif
%endif

# pkgrel will be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%define includeMinorbump 1
%if ! %{includeMinorbump}
  %undefine minorbump
%endif
%if 0%{?snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section

# grin source tarball file basename
# the archive name and directory tree can have some variances
# v1.0.0.tar.gz
%define _archivename_alt1 v%{version}
# grin-1.0.0.tar.gz
%define _archivename_alt2_grin %{name}-%{version}
# mainnet-release.tar.gz
%define _archivename_alt3 mainnet-release
# grin-mainnet-release.tar.gz
%define _archivename_alt4_grin %{name}-mainnet-release

# our selection for this build - edit this
%define _archivename0 %{_archivename_alt2_grin}
%define _srccodetree0 %{_archivename_alt2_grin}

%if %{includeArchiveQualifier}
  %define archivename0 %{_archivename0}-%{archiveQualifier}
  %define srccodetree0 %{_srccodetree0}-%{archiveQualifier}
%else
  %define archivename0 %{_archivename0}
  %define srccodetree0 %{_srccodetree0}
%endif

# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               grin-1.0
#      \_srccodetree0       \_grin-1.0.0
#      \_srccontribtree     \_grin-1.0-contrib
%define srcroot %{name}-%{vermajor}
%define srccontribtree %{name}-%{vermajor}-contrib
# srccodetrees defined earlier

# Note, that ...
# https://github.com/mimblewimble/grin/archive/mainnet-release.tar.gz
# ...is the same as...
# https://github.com/mimblewimble/grin/archive/mainnet-release/grin-mainnet-release.tar.gz
%if %{includeArchiveQualifier}
Source0: https://github.com/mimblewimble/grin/archive/v%{version}-%{archiveQualifier}/%{archivename0}.tar.gz
%else
Source0: https://github.com/mimblewimble/grin/archive/v%{version}/%{archivename0}.tar.gz
%endif
#Source2: https://github.com/taw00/grin-rpm/blob/master/source/testing/SOURCES/%%{srccontribtree}.tar.gz

# If you comment out "debug_package" RPM will create additional RPMs that can
# be used for debugging purposes. I am not an expert at this, BUT ".build_ids"
# are associated to debug packages, and I have lately run into packaging
# conflicts because of them. This is a topic I can't share a whole lot of
# wisdom about, but for now... I turn all that off.
#
# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
# ...flip-flop next two lines in order to disable (nil) or enable (1) debuginfo package build
%define debug_package 1
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_pie
%define _hardened_build 1

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing
# https://spdx.org/licenses/
License: Apache-2.0
URL: http://www.grin-tech.org/
# Note, for example, this will not build on ppc64le
ExclusiveArch: x86_64 i686 i386

# As recommended by...
# https://github.com/mimblewimble/grin/blob/master/doc/build.md
BuildRequires: patch
BuildRequires: rust >= 1.31 cargo
BuildRequires: pkgconf-pkg-config
BuildRequires: clang zlib-devel llvm
BuildRequires: openssl-devel
BuildRequires: cmake >= 3.11.0
BuildRequires: ncurses-devel ncurses-libs
# Other BuildRequires listed per package below

# tree, vim-enhanced, and less for mock build environment introspection
%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils curl wget
%endif


# src, wallet, and node
%description
MimbleWimble is a blockchain format and protocol that provides extremely good
scalability, privacy and fungibility by relying on strong cryptographic
primitives. It addresses gaps existing in almost all current blockchain
implementations.

Grin is an open source software project that implements a MimbleWimble
blockchain and fills the gaps required for a full blockchain and cryptocurrency
deployment.

The main goal and characteristics of the Grin project are:

* Privacy by default. This enables complete fungibility without precluding the
  ability to selectively disclose information as needed.

* Scales mostly with the number of users and minimally with the number of
  transactions (<100 byte kernel), resulting in a large space saving compared
  to other blockchains.

* Strong and proven cryptography. MimbleWimble only relies on Elliptic Curve
  Cryptography which has been tried and tested for decades.

* Design simplicity that makes it easy to audit and maintain over time.

* Community driven, encouraging mining decentralization.


Learn more at www.grin-tech.org


%prep
# Prep section starts us in directory .../BUILD (aka {_builddir})

### Message if EL7 found
### (probably should check for other unsupported OSes as well)
##%%if 0%%{?rhel} && 0%%{?rhel} < 8
##  %%{error: "EL7 builds no longer supported due to outdated build tools (c++, cmake, etc)"}
##  # exit doesn't do anything during build phase?
##  exit 1
##%%endif

mkdir -p %{srcroot}
# grin
%setup -q -T -D -a 0 -n %{srcroot}
# contributions
# {_builddir}/grin-1.0.0/grin-1.0-contrib/
#%%setup -q -T -D -a 2 -n %%{srcroot}


%build
# This section starts us in directory {_builddir}/{srcroot}
#curl https://sh.rustup.rs -sSf | sh; source $HOME/.cargo/env
cd %{srccodetree0}
RUST_BACKTRACE=1 TARGET=%{_target_platform} HOST=%{_target_platform} cargo build --release
cd ..


%install
# This section starts us in directory {_builddir}/{srcroot}

# Cheatsheet for built-in RPM macros:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
#   _builddir = {_topdir}/BUILD
#   _buildrootdir = {_topdir}/BUILDROOT
#   buildroot = {_buildrootdir}/{name}-{version}-{release}.{_arch}
#   _bindir = /usr/bin
#   _sbindir = /usr/sbin
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix or _usr = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
# This is used to quiet rpmlint who can't seem to understand that /usr/lib is
# still used for certain things.
%define _rawlib lib
%define _usr_lib /usr/%{_rawlib}
# These three are already defined in newer versions of RPM, but not in el7
%if 0%{?rhel} && 0%{?rhel} < 8
  %define _tmpfilesdir %{_usr_lib}/tmpfiles.d
  %define _unitdir %{_usr_lib}/systemd/system
  %define _metainfodir %{_datadir}/metainfo
%endif

# Create standard directories
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_localstatedir}
install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_metainfodir}
install -d -m755 -p %{buildroot}%{_bindir}
install -d -m755 -p %{buildroot}%{_libdir}/pkgconfig
install -d -m755 -p %{buildroot}%{_includedir}

# /var/lib/grin/... - grinuser's $HOME directory
install -d -m755 -p %{buildroot}%{_sharedstatedir}/grin/plugins

cp %{srccodetree0}/target/release/grin %{buildroot}%{_bindir}/

### /etc/sysconfig/grin-scripts/
##install -d %%{buildroot}%%{_sysconfdir}/sysconfig/grin-scripts

### System services
##install -D -m600 -p %%{srccontribtree}/linux/systemd/etc-sysconfig_grin %%{buildroot}%%{_sysconfdir}/sysconfig/grin
##install -D -m755 -p %%{srccontribtree}/linux/systemd/etc-sysconfig-grin-scripts_grin.send-email.sh %%{buildroot}%%{_sysconfdir}/sysconfig/grin-scripts/grin.send-email.sh
##install -D -m644 -p %%{srccontribtree}/linux/systemd/usr-lib-systemd-system_grin.service %%{buildroot}%%{_unitdir}/grin.service
##install -D -m644 -p %%{srccontribtree}/linux/systemd/usr-lib-tmpfiles.d_grin.conf %%{buildroot}%%{_tmpfilesdir}/grin.conf

### Service definition files for firewalld for full and master nodes
##install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore.xml
##install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore-testnet.xml
##install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-rpc.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore-rpc.xml
##install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet-rpc.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore-testnet-rpc.xml


%pre
# _sharedstatedir is /var/lib - /var/lib/grin is the $HOME for the grinuser user
getent group grinuser >/dev/null || groupadd -r grinuser
getent passwd grinuser >/dev/null || useradd -r -g grinuser -d %{_sharedstatedir}/grin -s /sbin/nologin -c "System user 'grinuser' to isolate GRIN execution" grinuser


%post
#%%systemd_post grin.service
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


%posttrans
#/usr/bin/systemd-tmpfiles --create
#TODO: Replace above with %%tmpfiles_create_package macro
#TODO: https://github.com/systemd/systemd/blob/master/src/core/macros.systemd.in


%preun
#%%systemd_preun grin.service


%postun
#%%systemd_preun grin.service
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


%files
%defattr(-,root,root,-)
%license %{srccodetree0}/LICENSE
%{_bindir}/grin

### Application as systemd service directory structure
##%%defattr(-,grinuser,grinuser,-)
### /var/lib/grin/... - grinuser's $HOME dir
##%%dir %%attr(750,grinuser,grinuser) %%{_sharedstatedir}/grin
### /etc/sysconfig/grin-scripts/
##%%dir %%attr(755,grinuser,grinuser) %%{_sysconfdir}/sysconfig/grin-scripts
#
##%%defattr(-,root,root,-)
##%%config(noreplace) %%attr(600,root,root) %%{_sysconfdir}/sysconfig/grin
##%%attr(755,root,root) %%{_sysconfdir}/sysconfig/grin-scripts/grin.send-email.sh
#
##%%{_unitdir}/grin.service
##%%{_usr_lib}/firewalld/services/dashcore.xml
##%%{_usr_lib}/firewalld/services/dashcore-rpc.xml
##%%{_tmpfilesdir}/grin.conf


# -----------------------------------------------------------------------------

# Grin Information
#
# Grin...
#   * Project website: https://grin-tech.org/
#   * Project repo: https://github.com/mimblewimble
#   * Project wiki: https://github.com/mimblewimble/docs/wiki
#
# Grin on Fedora...
#   * Git Repo: https://github.com/taw00/grin-rpm
%changelog
* Wed Jan 16 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.0-0.1.testing.taw
  - Initial build
