%define major 0
%define libname %mklibname %{name} %major
%define develname %mklibname %{name} -d

Summary:	The GNU Scientific Library for numerical analysis
Name:		gsl
Version:	1.15
Release:	%mkrel 1
License:	GPLv2+
Group:		Sciences/Mathematics
URL:		http://www.gnu.org/software/gsl/
Source0:	ftp://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
Patch0:		%{name}-1.14-undefined-symbols.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Obsoletes:	%mklibname %{name} 0 -d
Provides:	%mklibname %{name} 0 -d

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/gsl-config

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post doc
%_install_info gsl-ref.info

%postun doc
%_remove_install_info gsl-ref.info

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files progs
%defattr(-,root,root)
%doc AUTHORS NEWS README THANKS
%{_bindir}/gsl-histogram
%{_bindir}/gsl-randist
%{_mandir}/man1/gsl-histogram*
%{_mandir}/man1/gsl-randist*

%files doc
%defattr(-,root,root)
%{_infodir}/*info*

%files -n %{libname}
%defattr(-,root,root) 
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root) 
%doc BUGS ChangeLog TODO doc/examples/
%{_bindir}/gsl-config
%{multiarch_bindir}/gsl-config
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_mandir}/man3/*
%{_mandir}/man1/gsl-config.*
