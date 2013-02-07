Summary:	A lightweight email program designed around conversations
Name:		geary
Version:	0.2.2
Release:	1
License:	LGPL v2+
Source0:	http://yorba.org/download/geary/stable/%{name}-%{version}.tar.xz
# Source0-md5:	9cb525a982cdcc615d5af257c14407b6
Group:		X11/Applications/Networking
URL:		http://yorba.org/geary/
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	glib2-devel >= 1:2.30.0
BuildRequires:	gmime-devel >= 2.6.0
BuildRequires:	gtk+3-devel >= 3.2.0
BuildRequires:	gtk-webkit3-devel >= 1.8.0
BuildRequires:	intltool
BuildRequires:	libcanberra-devel >= 0.28
BuildRequires:	libgee0.6-devel >= 0.6.0
BuildRequires:	libgnome-keyring-devel >= 3.2.2
BuildRequires:	libnotify-devel >= 0.7.5
BuildRequires:	libunique3-devel >= 3.0.0
BuildRequires:	sqlite3-devel >= 3.7.4
BuildRequires:	vala >= 0.17.4
Requires:	desktop-file-utils
Requires:	glib2 >= 1:2.26.0
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Geary is a new email reader for GNOME designed to let you read your
email quickly and effortlessly. Its interface is based on
conversations, so you can easily read an entire discussion without
having to click from message to message. Geary is still in early
development and has limited features today, but we're planning to add
drag-and-drop attachments, lightning-fast searching, multiple account
support and much more. Eventually we'd like Geary to have an
extensible plugin architecture so that developers will be able to add
all kinds of nifty features in a modular way.

%prep
%setup -q

%build
%cmake \
	-DGSETTINGS_COMPILE=OFF \
	-DGSETTINGS_COMPILE_IN_PLACE=OFF \
	-DICON_UPDATE=OFF \
	-DDESKTOP_UPDATE=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# see http://redmine.yorba.org/issues/5692
find $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas -type f -a \( \
  -name org.yorba.geary.gschema.xml -o -delete \)

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/geary.desktop

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ca_ES
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/el_GR
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/es_ES
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/km_KH
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/nl_NL
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ro_RO
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/tr_TR

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_desktop_database
%update_icon_cache hicolor
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS MAINTAINERS README THANKS
%attr(755,root,root) %{_bindir}/geary
%{_datadir}/geary
%{_desktopdir}/geary.desktop
%{_datadir}/glib-2.0/schemas/org.yorba.geary.gschema.xml
%{_iconsdir}/hicolor/*/apps/geary.*
