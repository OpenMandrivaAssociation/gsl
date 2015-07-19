%define major 0
%define libname %mklibname %{name} %{major}
%define libcblas %mklibname %{name}cblas %{major}
%define devname %mklibname %{name} -d

Summary:	The GNU Scientific Library for numerical analysis
Name:		gsl
Version:	1.16
Release:	5
License:	GPLv2+
Group:		Sciences/Mathematics
Url:		http://www.gnu.org/software/gsl/
Source0:	ftp://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz
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

%package -n %{libcblas}
Summary:	Shared libraries for Scientific Library
Group:		System/Libraries
Conflicts:	%{_lib}gsl0 < 1.15-5

%description -n %{libcblas}
This package contains a shared library for %{name}.


%package -n %{devname}
Summary:	Development files for Scientific Library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-static

%make

%check
%ifarch %{x86_64}
make check
%endif

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
%{_libdir}/libgsl.so.%{major}*

%files -n %{libcblas}
%{_libdir}/libgslcblas.so.%{major}*

%files -n %{devname}
%doc BUGS ChangeLog TODO doc/examples/
%{_bindir}/gsl-config
%{multiarch_bindir}/gsl-config
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_mandir}/man3/*
%{_mandir}/man1/gsl-config.*

