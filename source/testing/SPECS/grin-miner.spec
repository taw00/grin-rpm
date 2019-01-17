# GRIM Miner - a miner for grin, a digital currency implementing Mimblewimble
# Reference implementation
# vim:tw=0:ts=2:sw=2:et:
#
# This is the rpm spec for building a Grim client and full node.
#
# Packages built:
# * grin-miner
# * grin-miner-debuginfo (not always/often built)
# 
# Requires: grin
#
# DISCLAIMER:
# This RPM spec file is a work in progress
#
# Enjoy. -t0dd

# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

Name: grin-miner
Summary: A peer-to-peer digital currency implementing mimblewimble (miner)

%define targetIsProduction 0

# ARCHIVE QUALIFIER
# ie. if the dev team includes things like rc3 in the filename
%define archiveQualifier rc1
%define includeArchiveQualifier 0

# VERSION
%define vermajor 1.0
%define verminor 1
Version: %{vermajor}.%{verminor}

# RELEASE
# package release, and potentially extrarel
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.2
%endif

# MINORBUMP
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

# grin-miner source tarball file basename
# the archive name and directory tree can have some variances
# v1.0.0.tar.gz
%define _archivename_alt1 v%{version}
# grin-miner-1.0.0.tar.gz
%define _archivename_alt2 %{name}-%{version}
# mainnet-release.tar.gz
%define _archivename_alt3 mainnet-release
# grin-miner-mainnet-release.tar.gz
%define _archivename_alt4 %{name}-mainnet-release

# our selection for this build - edit this
%define _archivename %{_archivename_alt2}
%define _srccodetree %{_archivename_alt2}

%if %{includeArchiveQualifier}
  %define archivename %{_archivename}-%{archiveQualifier}
  %define srccodetree %{_srccodetree}-%{archiveQualifier}
%else
  %define archivename %{_archivename}
  %define srccodetree %{_srccodetree}
%endif

# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               grin-miner-1.0
#      \_srccodetree        \_grin-miner-1.0.0
#      \_srccontribtree     \_grin-miner-1.0-contrib
%define srcroot %{name}-%{vermajor}
%define srccontribtree %{name}-%{vermajor}-contrib
# srccodetree defined earlier

# Note, that ...
# https://github.com/mimblewimble/grin-miner/archive/v1.0.0.tar.gz
# ...is the same as...
# https://github.com/mimblewimble/grin-miner/archive/v1.0.0/grin-miner-1.0.0.tar.gz
%if %{includeArchiveQualifier}
Source0: https://github.com/mimblewimble/grin-miner/archive/v%{version}-%{archiveQualifier}/%{archivename}.tar.gz
%else
Source0: https://github.com/mimblewimble/grin-miner/archive/v%{version}/%{archivename}.tar.gz
%endif
#Source1: https://github.com/taw00/grin-rpm/blob/master/source/testing/SOURCES/%%{srccontribtree}.tar.gz
Patch0: https://github.com/taw00/grin-rpm/blob/master/source/testing/SOURCES/grin-miner-%{version}-git-submodule-update-init-2019-01-16.patch

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
# https://github.com/mimblewimble/grin-miner/blob/master/doc/build.md
BuildRequires: patch sed
BuildRequires: rust >= 1.31 cargo
BuildRequires: pkgconf-pkg-config
BuildRequires: clang zlib-devel llvm
BuildRequires: openssl-devel
BuildRequires: cmake >= 3.11.0
BuildRequires: ncurses-devel ncurses-libs
# Needed to build ocl_cuckaroo.cuckooplugin
BuildRequires: ocl-icd-devel
Requires: grin >= %{vermajor}

# tree, vim-enhanced, and less for mock build environment introspection
%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils curl wget
%endif


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
# grin-miner
# {_builddir}/grin-miner-1.0.0/grin-miner-mainnet-release/
# ..or something like..
# {_builddir}/grin-miner-1.0.0/grin-miner-testnet4-release/
%setup -q -T -D -a 0 -n %{srcroot}
# contributions
# {_builddir}/grin-miner-1.0.0/grin-miner-1.0-contrib/
#%%setup -q -T -D -a 1 -n %%{srcroot}
# patches
cd %{srccodetree}
%patch0 -p1
cd ..


%build
# This section starts us in directory {_builddir}/{srcroot}
#curl https://sh.rustup.rs -sSf | sh; source $HOME/.cargo/env
cd %{srccodetree}
RUST_BACKTRACE=1 TARGET=%{_target_platform} HOST=%{_target_platform} cargo build --release
. ./install_ocl_plugins.sh
cd ..


#%%check
# This section starts us in directory {_builddir}/{srcroot}
#cd %%{srccodetree}


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

cd %{srccodetree}
cp target/release/grin-miner %{buildroot}%{_bindir}/
cp target/release/plugins/* %{buildroot}%{_sharedstatedir}/grin/plugins/
#install -D -m644 grin-miner.toml %{buildroot}%{_sharedstatedir}/grin/
sed '~s~#miner_plugin_dir = "target/debug/plugins"~miner_plugin_dir = "%{_sharedstatedir}/grin/plugins/"~' grin-miner.toml > %{buildroot}%{_sharedstatedir}/grin/grin-miner.toml
cd ..

### /etc/sysconfig/grin-scripts/
##install -d %%{buildroot}%%{_sysconfdir}/sysconfig/grin-scripts

# TODO -- get systemd stuff added -- copy-catting from my dashcore builds
### System services
##install -D -m600 -p %%{srccontribtree}/linux/systemd/etc-sysconfig_grin-miner %%{buildroot}%%{_sysconfdir}/sysconfig/grin-miner
##install -D -m755 -p %%{srccontribtree}/linux/systemd/etc-sysconfig-grin-scripts_grin-miner.send-email.sh %%{buildroot}%%{_sysconfdir}/sysconfig/grin-scripts/grin-miner.send-email.sh
##install -D -m644 -p %%{srccontribtree}/linux/systemd/usr-lib-systemd-system_grin-miner.service %%{buildroot}%%{_unitdir}/grin-miner.service
##install -D -m644 -p %%{srccontribtree}/linux/systemd/usr-lib-tmpfiles.d_grin-miner.conf %%{buildroot}%%{_tmpfilesdir}/grin-miner.conf

# TODO -- get firewall stuff added -- copy-catting from my dashcore builds
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
#%%systemd_post grin-miner.service
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


%posttrans
#/usr/bin/systemd-tmpfiles --create
#TODO: Replace above with %%tmpfiles_create_package macro
#TODO: https://github.com/systemd/systemd/blob/master/src/core/macros.systemd.in


%preun
#%%systemd_preun grin-miner.service


%postun
#%%systemd_postun grin-miner.service
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


%files
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE
%{_bindir}/grin-miner

# _sharedstatedir}/grin == /var/lib/grin/... - grinuser's $HOME dir
%defattr(-,grinuser,grinuser,-)
%dir %attr(755,grinuser,grinuser) %{_sharedstatedir}/grin
%dir %attr(755,grinuser,grinuser) %{_sharedstatedir}/grin/plugins
%attr(644,grinuser,grinuser) %{_sharedstatedir}/grin/grin-miner.toml
%attr(755,grinuser,grinuser) %{_sharedstatedir}/grin/plugins/*

### /etc/sysconfig/grin-scripts/
##%%dir %%attr(755,grinuser,grinuser) %%{_sysconfdir}/sysconfig/grin-scripts
#
##%%defattr(-,root,root,-)
##%%config(noreplace) %%attr(600,root,root) %%{_sysconfdir}/sysconfig/grin-miner
##%%attr(755,root,root) %%{_sysconfdir}/sysconfig/grin-scripts/grin-miner.send-email.sh
#
##%%{_unitdir}/grin-miner.service
##%%{_usr_lib}/firewalld/services/dashcore.xml
##%%{_usr_lib}/firewalld/services/dashcore-rpc.xml
##%%{_tmpfilesdir}/grin-miner.conf


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
* Wed Jan 16 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.2.testing.taw
  - Changed the default plugins directory in the shipped grin-miner.toml file

* Wed Jan 16 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.1.testing.taw
  - Updated source tarball and fixed a lot of things in the specfile

* Wed Jan 16 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.0-0.1.testing.taw
  - Initial builds

