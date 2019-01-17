Name:       toddpkgs-grin-repo
Version:    1.0
Summary:    Repository configuration to enable management of grin packages (grin cryptocurrency core wallet and node)

%define targetIsProduction 0

# RELEASE
%define _rel 0.1
%define _snapinfo testing
%define _minorbump taw
%if %{targetIsProduction}
Release:    %{_rel}%{?dist}.%{_minorbump}
%else
Release:    %{_rel}.%{_snapinfo}%{?dist}.%{_minorbump}
%endif

License:    MIT
URL:        https://github.com/taw00/grin-rpm
Source0:    https://github.com/taw00/grin-rpm/raw/master/source/testing/SOURCES/toddpkgs-grin-repo-1.0.tar.gz
BuildArch:  noarch
#BuildRequires:  tree

# CentOS/RHEL/EPEL can't do "Suggests:"
# Update: Don't use suggests. Ever.
#%%if 0%%{?fedora:1}
#Suggests: distribution-gpg-keys-copr
#%%endif


%description
Todd (aka, taw, taw00, t0dd in various communities) packages applications for
Fedora Linux and RHEL/CentOS/EPEL. This package deploys the repository
configuration file necessary to enable on-going management of the Grin
(cryptocurrency) wallet and full-node RPM package for Fedora Linux.

Install this, then...
* sudo dnf list|grep grin
* sudo dnf install grin -y --refresh

Switching between testing and stable repositories (example):
  sudo dnf config-manager --set-disabled grin-testing
  sudo dnf config-manager --set-enabled grin-stable

Notes about GPG keys:
* An RPM signing key is included. It is used to sign RPMs that I build by
  hand. Namely any *.src.rpm found in github.com/taw00/grin-rpm
* RPMs from the copr repositories are signed by fedoraproject build system
  keys.


%prep
%setup -q
# For debugging purposes...
#cd .. ; tree -df -L 1  ; cd -


%build
# no-op


%install
# Builds generically. Will need a disto specific RPM though.
#t0dd: rhel not currently supported
#install -d %%{buildroot}%%{_sysconfdir}/yum.repos.d
install -d %{buildroot}%{_sysconfdir}/pki/rpm-gpg

install -D -m644 todd-694673ED-public-2030-01-04.2016-11-07.asc %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public

%if 0%{?rhel:1}
#t0dd: rhel not currently supported
#  %%if %{targetIsProduction}
#    install -D -m644 grin-epel.repo %%{buildroot}%%{_sysconfdir}/yum.repos.d/grin.repo
#  %%else
#    install -D -m644 grin-epel.repo-enabled-testing-repo %%{buildroot}%%{_sysconfdir}/yum.repos.d/grin.repo
#  %%endif
%else
  %if %{targetIsProduction}
    install -D -m644 grin-fedora.repo %{buildroot}%{_sysconfdir}/yum.repos.d/grin.repo
  %else
    install -D -m644 grin-fedora.repo-enabled-testing-repo %{buildroot}%{_sysconfdir}/yum.repos.d/grin.repo
  %endif
%endif


%files
#%%config(noreplace) %%attr(644, root,root) %%{_sysconfdir}/yum.repos.d/grin.repo
%config %attr(644, root,root) %{_sysconfdir}/yum.repos.d/grin.repo
%attr(644, root,root) %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public


%changelog
* Wed Jan 16 2019 Todd Warner <t0dd_at_protonmail.com> 1.0-0.1.testing.taw
  - Initial build.

