# TODO: rename to  python-werkzeug
#
# Conditional build:
# %bcond_without  doc             # don't build doc
%bcond_with  tests   # do not perform "make test"
%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module

%define 	module	werkzeug
Summary:	The Swiss Army knife of Python web development
Name:		python-%{module}
Version:	0.9.6
Release:	5
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/W/Werkzeug/Werkzeug-%{version}.tar.gz
# Source0-md5:	f7afcadc03b0f2267bdc156c34586043
URL:		http://werkzeug.pocoo.org/
%if %{with python2}
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
Requires:	python-modules
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
Requires:	python3-modules
%endif


BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility
modules. It includes a powerful debugger, full featured request and
response objects, HTTP utilities to handle entity tags, cache control
headers, HTTP dates, cookie handling, file uploads, a powerful URL
routing system and a bunch of community contributed addon modules.

%package -n python3-%{module}
Summary:	The Swiss Army knife of Python web development
Summary(pl.UTF-8):	Zbiór narzędzi dla rozwouju aplikacji sieciowych dla Pythona
Group:		Libraries/Python

%description -n python3-%{module}
Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility
modules. It includes a powerful debugger, full featured request and
response objects, HTTP utilities to handle entity tags, cache control
headers, HTTP dates, cookie handling, file uploads, a powerful URL
routing system and a bunch of community contributed addon modules.

# %description -n python3-%{module} -l pl.UTF-8

%prep
%setup -q -n Werkzeug-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif


%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
        | xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES
%{py_sitescriptdir}/werkzeug
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/Werkzeug-%{version}-py*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/Werkzeug-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif
