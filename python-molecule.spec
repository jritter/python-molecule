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
Version: 2.16
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

BuildRequires:  python2-anyconfig
BuildRequires:  python2-click
BuildRequires:  python2-colorama
BuildRequires:  python2-devel
BuildRequires:  python2-jinja2
BuildRequires:  python2-marshmallow
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  python2-sh
BuildRequires:  python2-sphinx
BuildRequires:  python2-tree-format
BuildRequires:  PyYAML
BuildRequires:  yamllint

%if %{with python3}
BuildRequires:  python3-anyconfig
BuildRequires:  python3-click
BuildRequires:  python3-colorama
BuildRequires:  python3-devel
BuildRequires:  python3-jinja2
BuildRequires:  python3-marshmallow
BuildRequires:  python3-PyYAML
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-sh
BuildRequires:  python3-sphinx
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
Recommends: python2-docker
%if %{with python3}
Requires: python3-molecule
%endif
Requires: ansible
Requires: python2-anyconfig
Requires: python2-cerberus
Requires: python2-click
Requires: python2-click-completion
Requires: python2-colorama
Requires: python2-cookiecutter
Requires: python2-flake8
Requires: python2-future
Requires: python2-jinja2
Requires: python2-marshmallow
Requires: python2-pbr
Requires: python2-pexpect
Requires: python2-poyo
Requires: python2-requests
Requires: python2-sh
Requires: python2-tabulate
Requires: python2-testinfra
Requires: python2-tree-format
Requires: PyYAML
Requires: yamllint
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
Recommends: python2-docker
Requires: ansible-python3
Requires: python3-anyconfig
Requires: python3-cerberus
Requires: python3-click
Requires: python3-click-completion
Requires: python3-colorama
Requires: python3-cookiecutter
Requires: python3-flake8
Requires: python3-future
Requires: python3-jinja2
Requires: python3-marshmallow
Requires: python3-PyYAML
Requires: python3-pbr
Requires: python3-pexpect
Requires: python3-poyo
Requires: python3-requests
Requires: python3-sh
Requires: python3-tabulate
Requires: python3-testinfra
Requires: python3-tree-format
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
cat <<EOF >> setup.cfg

[files]
data_files =
    %{python2_sitelib}/%{pkgname}/cookiecutter = molecule/cookiecutter/*
%if %{with python3}
    %{python3_sitelib}/%{pkgname}/cookiecutter = molecule/cookiecutter/*
%endif # with python3
EOF

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

%check
# can't do python2 tests because yamllint is only packaged for python3

# FIXME: library pathing issues causing tests to fail
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
* Tue Jul 17 2018 Brett Lentz <brett.lentz@gmail.com> - 2.16-1
- update to 2.16

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.13.1-3
- Rebuilt for Python 3.7

* Fri May 11 2018 Brett Lentz <brett.lentz@gmail.com> - 2.13.1-2
- add Recommends for default use case

* Wed May 9 2018 Brett Lentz <brett.lentz@gmail.com> - 2.13.1-1
- update to 2.13.1
- ensure all needed files are installed

* Mon Apr 30 2018 Brett Lentz <brett.lentz@gmail.com> - 2.13-1
- update to 2.13

* Mon Apr 2 2018 Brett Lentz <brett.lentz@gmail.com> - 2.12.1-2
- update to 2.12.1

* Thu Mar 29 2018 Brett Lentz <brett.lentz@gmail.com> - 2.11-1
- update to 2.11

* Wed Mar 14 2018 Brett Lentz <brett.lentz@gmail.com> - 2.10.1-3
- fix package deps

* Mon Mar 12 2018 Brett Lentz <brett.lentz@gmail.com> - 2.10.1-1
- update to 2.10.1

* Mon Mar 5 2018 Brett Lentz <brett.lentz@gmail.com> - 2.9-1
- update to 2.9

* Tue Jan 23 2018 Brett Lentz <brett.lentz@gmail.com> - 2.7-1
- initial package
