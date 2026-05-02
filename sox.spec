%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}

######################
# Hardcode PLF build
%define build_plf 0
######################

%if %{build_plf}
%define distsuffix plf
%define extrarelsuffix plf
%endif

%define major	3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	A general purpose sound file conversion tool
Name:		sox
Version:		14.7.1.2
Release:		1%{?extrarelsuffix}
License:		LGPLv2+
Group:		Sound
# Original project:
#Url:		https://sox.sourceforge.net/
#Source0:	https://downloads.sourceforge.net/project/sox/sox/%%{version}/sox-%%{version}.tar.bz2
# Fork that is still maintained:
Url:		https://codeberg.org/sox_ng/sox_ng
Source0:	https://codeberg.org/sox_ng/sox_ng/releases/download/sox_ng-%{version}/sox_ng-%{version}.tar.gz
BuildRequires:	gomp-devel
BuildRequires:	gsm-devel
BuildRequires:	ladspa-devel
%if %{build_plf}
BuildRequires:	libamrwb-devel
BuildRequires:	libamrnb-devel
%endif
BuildRequires:	libtool-devel
BuildRequires:	lpc10-devel
BuildRequires:	magic-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(lame)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(sndio)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(twolame)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(wavpack)

Requires:	%{libname} = %{version}-%{release}

BuildSystem:	autotools
BuildOption:	--with-distro=OpenMandriva
BuildOption:	--with-ffmpeg
BuildOption:	--with-ladspa-path=%{_includedir}
BuildOption: 	--with-dyn-default
BuildOption:	--enable-dl-sndfile
BuildOption:	--enable-year2038
BuildOption:	--enable-replace

#patchlist
#sox-ng-actually-find-the-plugins.patch

%description
SoX (Sound eXchange) is a sound file format converter for Linux, UNIX and DOS
PCs. The self-described 'Swiss Army knife of sound tools,' It can convert
between many different digitized sound formats and perform simple sound
manipulation functions, including sound effects.
%if %{build_plf}
This package is in Restricted as it was built with AMR encoder support,
which is in Restricted.
%endif

%files
%doc ChangeLog README AUTHORS
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/%{name}
%{_bindir}/soxi
%{_bindir}/play_ng
%{_bindir}/rec_ng
%{_bindir}/%{name}_ng
%{_bindir}/soxi_ng
%{_mandir}/man1/*.1*
%{_mandir}/man7/*.7*

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Libraries for SoX
Group:		System/Libraries

%description -n %{libname}
Libraries for SoX.

%files -n %{libname}
%{_libdir}/libsox_ng.so.%{major}*
%{_libdir}/libsox.so.%{major}*
%{_libdir}/%{name}
%{_libdir}/%{name}_ng

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development headers and libraries for SoX.

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/libsox.so
%{_libdir}/libsox_ng.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}_ng.pc
%{_mandir}/man3/libsox*.3*

#-----------------------------------------------------------------------------

%conf -p
export CFLAGS="%{optflags} -DHAVE_SYS_SOUNDCARD_H=1 -D_FILE_OFFSET_BITS=64 -fPIC -DPIC"


%install -a
# The --enable replace build option already takes care of most of the compat symlinks:
# we need to add only those
pushd %{buildroot}%{_libdir}
	ln -s sox_ng sox
	ln -s libsox_ng.so.%{major} libsox.so.%{major}
	ln -s libsox_ng.so.%{major}.0.0 libsox.so.%{major}.0.0
popd
