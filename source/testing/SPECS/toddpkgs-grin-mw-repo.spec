Name:       toddpkgs-grin-mw-repo
Version:    1.0
Summary:    Repository configuration to enable management of grin packages (grin cryptocurrency wallet, node, and miner)

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
Source0:    https://github.com/taw00/grin-rpm/raw/master/source/testing/SOURCES/toddpkgs-grin-mw-repo-1.0.tar.gz
BuildArch:  noarch
#BuildRequires:  tree


%description
Todd (aka, taw, taw00, t0dd in various communities) packages applications for
Fedora Linux and RHEL/CentOS/EPEL. This package deploys the repository
configuration file necessary to enable on-going management of the Grin
(cryptocurrency) wallet, full-node, and mininge RPM package for Fedora Linux.

Install this toddpkgs- package and then...
* sudo dnf list | grep grin-mw
* sudo dnf install grin-mw -y
  ...or...
* sudo dnf install grin-mw-miner -y

Switching between testing and stable repositories (example):
  sudo dnf config-manager --set-disabled grin-mw-testing
  sudo dnf config-manager --set-enabled grin-mw-stable

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
#  %%if %%{targetIsProduction}
#    install -D -m644 grin-mw-epel.repo %%{buildroot}%%{_sysconfdir}/yum.repos.d/grin-mw.repo
#  %%else
#    install -D -m644 grin-mw-epel.repo-enabled-testing-repo %%{buildroot}%%{_sysconfdir}/yum.repos.d/grin-mw.repo
#  %%endif
%else
  %if %{targetIsProduction}
    install -D -m644 grin-mw-fedora.repo %{buildroot}%{_sysconfdir}/yum.repos.d/grin-mw.repo
  %else
    install -D -m644 grin-mw-fedora.repo-enabled-testing-repo %{buildroot}%{_sysconfdir}/yum.repos.d/grin-mw.repo
  %endif
%endif


%files
#%%config(noreplace) %%attr(644, root,root) %%{_sysconfdir}/yum.repos.d/grin-mw.repo
%config %attr(644, root,root) %{_sysconfdir}/yum.repos.d/grin-mw.repo
%attr(644, root,root) %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public


%changelog
* Thu Jan 17 2019 Todd Warner <t0dd_at_protonmail.com> 1.0-0.1.testing.taw
  - Initial build.

