#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# test action

%define		module	werkzeug
Summary:	The Swiss Army knife of Python web development
Summary(pl.UTF-8):	Scyzoryk szwajcarski programisty aplikacji WWW
Name:		python3-%{module}
Version:	2.2.3
Release:	3
License:	BSD
Group:		Development/Languages/Python
# pypi release misses docs/_themes directory
##Source0Download: https://pypi.org/simple/Werkzeug
#Source0:	https://files.pythonhosted.org/packages/source/W/Werkzeug/Werkzeug-%{version}.tar.gz
#Source0Download: https://github.com/pallets/werkzeug/releases
Source0:	https://github.com/pallets/werkzeug/archive/%{version}/werkzeug-%{version}.tar.gz
# Source0-md5:	3da84b7479521f8e8c2003cc4006b439
URL:		https://werkzeug.palletsprojects.com/
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-cryptography
BuildRequires:	python3-ephemeral_port_reserve
BuildRequires:	python3-greenlet
BuildRequires:	python3-markupsafe >= 2.1.1
BuildRequires:	python3-pyOpenSSL
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-timeout
BuildRequires:	python3-pytest-xprocess
BuildRequires:	python3-requests
# optional
#BuildRequires:	python3-watchdog
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-pallets-sphinx-themes
BuildRequires:	python3-sphinx_issues
BuildRequires:	python3-sphinxcontrib-log-cabinet
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility
modules. It includes a powerful debugger, full featured request and
response objects, HTTP utilities to handle entity tags, cache control
headers, HTTP dates, cookie handling, file uploads, a powerful URL
routing system and a bunch of community contributed addon modules.

%description -l pl.UTF-8
Werkzeug początkowo był prostym zbiorem różnych narzędzi dla aplikacji
WSGI, a stał się jednym z najbardziej zaawansowanych modułów
narzędziowych WSGI. Zawiera potężny debugger, obiekty żądania i
odpowiedzi z pełną funkcjonalnością, narzędzia HTTP do obsługi
znaczników encji, nagłówki sterujące buforowaniem, daty HTTP, obsługę
ciasteczek, przesyłanie plików, potężny system trasowania URL oraz
wiele dodatkowych modułów udostępnionych przez społeczność.

%package apidocs
Summary:	Documentation for Python Werkzeug package
Summary(pl.UTF-8):	Dokumentacja do pakietu Pythona Werkzeug
Group:		Documentation

%description apidocs
Documentation for Python Werkzeug package.

%description apidocs -l pl.UTF-8
Dokumentacja do pakietu Pythona Werkzeug.

%prep
%setup -q -n werkzeug-%{version}

%build
%py3_build

%if %{with tests}
LC_ALL=C.UTF-8 \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_timeout,xprocess.pytest_xprocess \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -m 'not dev_server' -k 'not test_exclude_patterns'
# dev_server tests fail with connection refused(?)
# test_exclude_patterns seems to fail with sys.prefix == sys.base_prefix (?)
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%{py3_sitescriptdir}/werkzeug
%{py3_sitescriptdir}/Werkzeug-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,deployment,middleware,*.html,*.js}
%endif
