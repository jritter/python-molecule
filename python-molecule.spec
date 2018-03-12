# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global pkgname molecule
%global setup_flags SKIP_PIP_INSTALL=1 PBR_VERSION=%{version}

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name: python-molecule
Version: 2.10.1
Release: 1%{?dist}
Summary: Molecule is designed to aid in the development and testing of Ansible roles

# Most of the package is MIT licensed.
#
# There are two files in the archive that are licensed with ASL 2.0:
# - molecule-2.7/molecule/interpolation.py
# - molecule-2.7/test/unit/test_interpolation.py
License: MIT and ASL 2.0

URL: https://github.com/metacloud/molecule
Source0: https://github.com/metacloud/molecule/archive/%{version}.tar.gz

BuildArch: noarch

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx

# doc & testing requirements
BuildRequires:  python2-sh
BuildRequires:  python2-anyconfig
BuildRequires:  python2-colorama
BuildRequires:  python2-jinja2
BuildRequires:  python2-marshmallow
BuildRequires:  PyYAML
BuildRequires:  python2-click
BuildRequires:  python2-tree-format

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx

# # doc & testing requirements
BuildRequires:  python3-sh
BuildRequires:  python3-anyconfig
BuildRequires:  python3-colorama
BuildRequires:  python3-jinja2
BuildRequires:  python3-marshmallow
BuildRequires:  python3-PyYAML
BuildRequires:  ansible
BuildRequires:  python3-click
BuildRequires:  yamllint
BuildRequires:  python3-tree-format
%endif # with python3

%description
Molecule is designed to aid in the development and testing of Ansible roles.
Molecule provides support for testing with multiple instances, operating
systems and distributions, virtualization providers, test frameworks and
testing scenarios. Molecule is opinionated in order to encourage an approach
that results in consistently developed roles that are well-written, easily
understood and maintained. Molecule uses Ansible playbooks to exercise the role
and its associated tests. Molecule supports any provider that Ansible supports.

%package     -n python2-molecule
Summary: %summary
Recommends: python-molecule-doc
%{?python_provide:%python_provide python2-%{pkgname}}
%description -n python2-molecule
Molecule is designed to aid in the development and testing of Ansible roles.
Molecule provides support for testing with multiple instances, operating
systems and distributions, virtualization providers, test frameworks and
testing scenarios. Molecule is opinionated in order to encourage an approach
that results in consistently developed roles that are well-written, easily
understood and maintained. Molecule uses Ansible playbooks to exercise the role
and its associated tests. Molecule supports any provider that Ansible supports.

%package     -n python-molecule-doc
Summary: %summary
%description -n python-molecule-doc
Documentation for python-molecule

%if %{with python3}
%package     -n python3-molecule
Summary: %summary
Recommends: python-molecule-doc
%{?python_provide:%python_provide python3-%{pkgname}}
%description -n python3-molecule
Molecule is designed to aid in the development and testing of Ansible roles.
Molecule provides support for testing with multiple instances, operating
systems and distributions, virtualization providers, test frameworks and
testing scenarios. Molecule is opinionated in order to encourage an approach
that results in consistently developed roles that are well-written, easily
understood and maintained. Molecule uses Ansible playbooks to exercise the role
and its associated tests. Molecule supports any provider that Ansible supports.

%endif # with python3

%prep
%autosetup -n %{pkgname}-%{version}

%build
%{setup_flags} %{py2_build}

%if %{with python3}
%{setup_flags} %{py3_build}
%endif # with python3

# generate html docs
PYTHONPATH=. sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{setup_flags} %{py2_install}

%if %{with python3}
%{setup_flags} %{py3_install}
%endif # with python3

# Xcheck
# Xif X{with python3}
# X{setup_flags} X{__python3} setup.py test
# Xendif # with python3

%files -n python2-molecule
%license LICENSE
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-molecule
%license LICENSE
%{python3_sitelib}/*
%endif # with python3
%{_bindir}/%{pkgname}

%files -n python-molecule-doc
%license LICENSE
%doc doc
%doc *.rst
%doc *-requirements.txt

%changelog
* Mon Mar 12 2018 Brett Lentz <brett.lentz@gmail.com> - 2.10.1-1
- update to 2.10.1

* Mon Mar 5 2018 Brett Lentz <brett.lentz@gmail.com> - 2.9-1
- update to 2.9

* Tue Jan 23 2018 Brett Lentz <brett.lentz@gmail.com> - 2.7-1
- initial package
