#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	json
Summary:	Support for serialising Haskell to and from JSON
Summary(pl.UTF-8):	Obsługa serializacji Haskella do i z formatu JSON
Name:		ghc-%{pkgname}
Version:	0.10
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/json
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	a30006f2e673b29852be7c001cfc2bfa
URL:		http://hackage.haskell.org/package/json
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-containers
BuildRequires:	ghc-mtl
BuildRequires:	ghc-text
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-mtl-prof
BuildRequires:	ghc-text-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-array
Requires:	ghc-base >= 3
Requires:	ghc-bytestring
Requires:	ghc-containers
Requires:	ghc-mtl
Requires:	ghc-text
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library provides a parser and pretty printer for converting
between Haskell values and JSON.

%description -l pl.UTF-8
Ta biblioteka udostępnia parser oraz funkcję wypisującą (pretty
printer) do konwersji między wartościami Haskella a formatem JSON.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-base-prof >= 3
Requires:	ghc-bytestring-prof
Requires:	ghc-containers-prof
Requires:	ghc-mtl-prof
Requires:	ghc-text-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGES %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSjson-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSjson-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSjson-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/JSON
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/JSON/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/JSON/*.dyn_hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSjson-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/JSON/*.p_hi
