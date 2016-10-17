#
# Conditional build:
%bcond_with	tests		# build without tests

%define		pkgname	scssphp
%define		php_min_version 5.3.0
%include	/usr/lib/rpm/macros.php
Summary:	A compiler for SCSS written in PHP
Name:		php-%{pkgname}
Version:	0.4.0
Release:	1
License:	MIT
Group:		Development/Libraries
URL:		http://leafo.github.io/scssphp
Source0:	https://github.com/leafo/scssphp/archive/v%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	7f18d57fdfa336fc583d34899779ab1c
Source1:	autoload.php
BuildRequires:	/usr/bin/php
%if %{with tests}
BuildRequires:	php(core) >= %{php_min_version}
BuildRequires:	php(ctype)
BuildRequires:	php(date)
BuildRequires:	php(mbstring)
BuildRequires:	php(pcre)
BuildRequires:	php-symfony2-ClassLoader
BuildRequires:	phpunit
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php(ctype)
Requires:	php(date)
Requires:	php(mbstring)
Requires:	php(pcre)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# exclude PEAR deps
%define		_noautoreq_pear	.*

%description
SCSS <http://sass-lang.com/> is a CSS preprocessor that adds many
features like variables, mixins, imports, color manipulation,
functions, and tons of other powerful features.

The entire compiler comes in a single class file ready for including
in any kind of project in addition to a command line tool for running
the compiler from the terminal.

scssphp implements SCSS. It does not implement the SASS syntax, only
the SCSS syntax.

%prep
%setup -qn %{pkgname}-%{version}

: Bin
sed "/scss.inc.php/s#.*#require_once '%{php_data_dir}/Leafo/ScssPhp/autoload.php';#" \
    -i bin/pscss

: Create autoloader
cp -p %{SOURCE1} src/autoload.php

%build
%if %{with tests}
: Library version value and autoloader check
php -r '
	require_once "src/autoload.php";
	$version = ltrim(\Leafo\ScssPhp\Version::VERSION, "v");
	echo "Version $version (expected %{version})\n";
	exit(version_compare("%{version}", "$version", "=") ? 0 : 1);
'
phpunit --verbose \
	--bootstrap src/autoload.php
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{php_data_dir}/Leafo/ScssPhp}
cp -a src/* $RPM_BUILD_ROOT%{php_data_dir}/Leafo/ScssPhp
install -p bin/pscss $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md composer.json LICENSE.md
%attr(755,root,root) %{_bindir}/pscss
%dir %{php_data_dir}/Leafo
%{php_data_dir}/Leafo/ScssPhp
