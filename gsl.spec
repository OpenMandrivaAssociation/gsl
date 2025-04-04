%define major 28
%define blas_major 0
%define libname %mklibname %{name}
%define libcblas %mklibname %{name}cblas
%define devname %mklibname %{name} -d
%define oldlibname %mklibname %{name} 27
%define oldlibcblas %mklibname %{name}cblas 0

%define _disable_ld_no_undefined 1

%global optflags %{optflags} -O3

# (tpg) enable PGO build, fails on i686 on sprcfunc test
%ifnarch %{ix86}
%bcond_without pgo
# FIXME:
%bcond_with tests
%else
%bcond_with pgo
%bcond_with tests
%endif

Summary:	The GNU Scientific Library for numerical analysis
Name:		gsl
Version:	2.8
Release:	1
License:	GPLv2+
Group:		Sciences/Mathematics
Url:		https://www.gnu.org/software/gsl/
Source0:	https://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz
Patch0:		gsl-2.7.1-fix_undefined_symbols.patch

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
%rename %{oldlibname}

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

%package -n %{libcblas}
Summary:	Shared libraries for Scientific Library
Group:		System/Libraries
Conflicts:	%{_lib}gsl0 < 1.15-5
%rename %{oldlibcblas}

%description -n %{libcblas}
This package contains a shared library for %{name}.


%package -n %{devname}
Summary:	Development files for Scientific Library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcblas} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

%prep
%autosetup -p1
%config_update

%build
%if %{with pgo}
export LD_LIBRARY_PATH="$(pwd)/cblas/.libs:$(pwd)/.libs"
CFLAGS="%{optflags} -flto -fprofile-generate" \
CXXFLAGS="%{optflags} -flto -fprofile-generate" \
LDFLAGS="%{build_ldflags} -flto -fprofile-generate" \
%configure
%make_build

%if %{with tests}
make check
%endif

unset LD_LIBRARY_PATH
llvm-profdata merge --output=%{name}-llvm.profdata $(find . -type f -name "*.profraw")
PROFDATA="$(realpath %{name}-llvm.profdata)"

make clean

CFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
CXXFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
LDFLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
%endif

%configure
%make_build


%check
%if %{with tests}
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH make check
%endif

%install
%make_install

%files progs
%{_bindir}/gsl-histogram
%{_bindir}/gsl-randist
%doc %{_mandir}/man1/gsl-histogram*
%doc %{_mandir}/man1/gsl-randist*

%files doc
%doc BUGS ChangeLog TODO doc/examples/
%doc AUTHORS NEWS README THANKS
%{_infodir}/*info*

%files -n %{libname}
%{_libdir}/libgsl.so.%{major}*

%files -n %{libcblas}
%{_libdir}/libgslcblas.so.%{blas_major}*

%files -n %{devname}
%{_bindir}/gsl-config
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%doc %{_mandir}/man3/*
%doc %{_mandir}/man1/gsl-config.*

