#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	Werkzeug
Summary:	The Swiss Army knife of Python web development
#Summary(pl.UTF-8):	-
Name:		python-%{module}
Version:	0.8.3
Release:	0.1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/W/Werkzeug/%{module}-%{version}.tar.gz
# Source0-md5:	12aa03e302ce49da98703938f257347a
URL:		http://werkzeug.pocoo.org/
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
#Requires:		python-libs
Requires:		python-modules
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

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%{?with_tests:%{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES
%{py_sitescriptdir}/werkzeug
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
