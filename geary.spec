Summary:	Geary is an IMAP mail client for GNOME 3
Name:		geary
Version:	0.10.0
Release:	1
License:	LGPL v2+
Group:		X11/Applications/Mail
Source0:	https://download.gnome.org/sources/geary/0.10/%{name}-%{version}.tar.xz
# Source0-md5:	c9735cb5eb53384c0c9d40ff815ed232
URL:		https://wiki.gnome.org/Apps/Geary
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gcr-devel >= 3.10.1
BuildRequires:	gettext
BuildRequires:	glib2-devel >= 1:2.34.0
BuildRequires:	gmime-devel >= 2.6.14
BuildRequires:	gtk+3-devel >= 3.12.0
BuildRequires:	gtk-webkit3-devel >= 1.10.0
BuildRequires:	intltool
BuildRequires:	libcanberra-devel >= 0.28
BuildRequires:	libgee-devel >= 0.8.5
BuildRequires:	libnotify-devel >= 0.7.5
BuildRequires:	libsecret-devel >= 0.11
BuildRequires:	libsoup-devel
BuildRequires:	libxml2-devel >= 2.7.8
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel >= 3.7.4
BuildRequires:	vala >= 0.22.1
BuildRequires:	vala-gcr >= 3.10.1
BuildRequires:	vala-libcanberra >= 0.28
BuildRequires:	vala-libgee >= 0.8.5
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.34.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Geary is an IMAP email client built for the GNOME desktop environment.
It allows you to read and send email with a simple, modern interface.
Features:
- Modern and straightforward interface
- Quick account setup
- Supports Gmail, Yahoo! Mail, Outlook.com, and popular IMAP servers
  (Dovecot, Cyrus, Zimbra, etc.)
- Mail organized by conversations
- Full-featured HTML mail composer
- Fast keyword search
- Desktop notification of new mail

%prep
%setup -q

%build
%cmake \
	-DGSETTINGS_COMPILE=OFF \
	-DGSETTINGS_COMPILE_IN_PLACE=OFF \
	-DICON_UPDATE=OFF \
	-DDESKTOP_UPDATE=OFF \
	-DDISABLE_CONTRACT=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/geary.desktop

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
%{_datadir}/appdata/geary.appdata.xml
%{_datadir}/geary
%{_desktopdir}/geary.desktop
%{_desktopdir}/geary-autostart.desktop
%{_datadir}/glib-2.0/schemas/org.yorba.geary.gschema.xml
%{_iconsdir}/hicolor/*/apps/geary.png
%{_iconsdir}/hicolor/scalable/actions/*.svg

