%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	The GNU Scientific Library for numerical analysis
Name:		gsl
Version:	1.15
Release:	3
License:	GPLv2+
Group:		Sciences/Mathematics
URL:		http://www.gnu.org/software/gsl/
Source0:	ftp://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
Patch0:		%{name}-1.14-undefined-symbols.patch

%description
The GNU Scientific Library (GSL) is a numerical library for C and
C++ programmers.  It contains over 1000 mathematical routines written
in ANSI C.  The library follows modern coding conventions, and lends
itself to being used in very high level languages (VHLLs).

The library covers the following subject areas:

  Complex Numbers             Roots of Polynomials     Special Functions
  Vectors and Matrices        Permutations             Sorting
  BLAS Support                Linear Algebra           Eigensystems
  Fast Fourier Transforms     Quadrature               Random Numbers
  Quasi-Random Sequences      Random Distributions     Statistics
  Histograms                  N-Tuples                 Monte Carlo Integration
  Simulated Annealing         Differential Equations   Interpolation
  Numerical Differentiation   Chebyshev Approximation  Series Acceleration
  Discrete Hankel Transforms  Root-Finding             Minimization
  Least-Squares Fitting       Physical Constants       IEEE Floating-Point

Further information can be found in the GSL Reference Manual.

Install the gsl package if you need a library for high-level
scientific numerical analysis.

%package progs
Summary:	Programs of the Scientific Library
Group:		Sciences/Mathematics
Requires:	%{libname} = %{version}-%{release}

%description progs
Here're the GNU Scientific Library (GSL) programs:
 - gsl-histogram: computes a histogram of the data on stdin
                  using n bins from xmin to xmax.
 - gsl-randist: generates n samples from a given distribution DIST
                with given parameters

%package doc
Summary:	Documentation of the Scientific Library
Group:		Books/Computer books

%description doc
This is the documentation in info format of the GNU Scientific Library (GSL).
This doc can be viewed through info, pinfo, konqueror, gnome yelp, ...

%package -n %{libname}
Summary:	Shared libraries for Scientific Library
Group:		System/Libraries

%description -n %{libname}
The GNU Scientific Library (GSL) is a numerical library for C and
C++ programmers.  It contains over 1000 mathematical routines written
in ANSI C.  The library follows modern coding conventions, and lends
itself to being used in very high level languages (VHLLs).

 The library covers the following subject areas:

  Complex Numbers             Roots of Polynomials     Special Functions
  Vectors and Matrices        Permutations             Sorting
  BLAS Support                Linear Algebra           Eigensystems
  Fast Fourier Transforms     Quadrature               Random Numbers
  Quasi-Random Sequences      Random Distributions     Statistics
  Histograms                  N-Tuples                 Monte Carlo Integration
  Simulated Annealing         Differential Equations   Interpolation
  Numerical Differentiation   Chebyshev Approximation  Series Acceleration
  Discrete Hankel Transforms  Root-Finding             Minimization
  Least-Squares Fitting       Physical Constants       IEEE Floating-Point

Further information can be found in the GSL Reference Manual.


%package -n %{develname}
Summary:	Development files for Scientific Library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
The gsl package includes the GNU Scientific Library (GSL). The GSL is a
collection of routines for numerical analysis, written in C.
It now includes a random number suite, an FFT package, simulated annealing
and root finding.  In the future, it will include numerical and Monte Carlo
integration and special functions.
Linking against the GSL allows programs to access functions which can
handle many of the problems encountered in scientific computing.

These are the static libs and include headers for developers.

%prep
%setup -q
%patch0 -p1

%build
# (tpg) gcc-4.3.2 bug http://gcc.gnu.org/bugzilla/show_bug.cgi?id=38051
export CFLAGS="%{optflags} -fno-strict-aliasing -fPIC"
export CXXFLAGS=$CFLAGS
export CPPCLAGS=$CFLAGS
%configure2_5x

%make

%check
make check

%install
%makeinstall_std

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/gsl-config

%files progs
%doc AUTHORS NEWS README THANKS
%{_bindir}/gsl-histogram
%{_bindir}/gsl-randist
%{_mandir}/man1/gsl-histogram*
%{_mandir}/man1/gsl-randist*

%files doc
%{_infodir}/*info*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc BUGS ChangeLog TODO doc/examples/
%{_bindir}/gsl-config
%{multiarch_bindir}/gsl-config
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so
%{_mandir}/man3/*
%{_mandir}/man1/gsl-config.*


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.14-3mdv2011.0
+ Revision: 661669
- multiarch fixes

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.14-2mdv2011.0
+ Revision: 605501
- rebuild

* Sun Mar 21 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.14-1mdv2010.1
+ Revision: 526233
- update to new version 1.14
- rediff patch 0

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.13-2mdv2010.1
+ Revision: 521131
- rebuilt for 2010.1

* Thu Sep 10 2009 Frederik Himpe <fhimpe@mandriva.org> 1.13-1mdv2010.0
+ Revision: 437127
- Update to new version 1.13

  + Funda Wang <fwang@mandriva.org>
    - rebuild with fPIC (bug#45668)

* Tue Feb 17 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.12-1mdv2009.1
+ Revision: 342158
- fix tests by adjusting optflags (gcc bug #38478, should work with next upstream release)
- Patch0: rediff to meet nofuzz
- update to new version 1.12

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 Helio Chissini de Castro <helio@mandriva.com> 1.11-3mdv2009.0
+ Revision: 217543
- Fix undefined symbol cblas.

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Apr 18 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.11-1mdv2009.0
+ Revision: 195506
- new version
- do not package INSTALL file

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 16 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.10-1mdv2008.1
+ Revision: 98786
- new version

* Tue Sep 18 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.9-2mdv2008.0
+ Revision: 89853
- new devel library policy
- new license policy
- add checks
- spec file clean


* Thu Feb 22 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.9-1mdv2007.0
+ Revision: 124788
- new version

* Wed Feb 14 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.8-3mdv2007.1
+ Revision: 121136
- rebuild
- update url
- spec file clean
- Import gsl

* Sat Apr 29 2006 Olivier Blin <oblin@mandriva.com> 1.8-2mdk
- update description (thanks to Brian Gough for reminding gsl isn't in
  alpha development)

* Fri Apr 21 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.8-1mdk
- new release

* Thu Nov 03 2005 Thierry Vignaud <tvignaud@mandriva.com> 1.7-1mdk
- new release

* Sat Sep 10 2005 Olivier Blin <oblin@mandriva.com> 1.6-3mdk
- fix typo in summary

* Thu Mar 31 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.6-2mdk
- multiarch
- drop COPYING file as package is GPL (copyright is included in common-licenses)
- spec cosmetics

* Thu Feb 10 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.6-1mdk
- new release
- fix url

* Sat Jul 10 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5-1mdk
- new release
- drop patch 0 (similar fix was comited upstream)

