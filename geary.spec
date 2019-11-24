#TODO? messaging-menu >= 12.10, unity >= 5.12.0
Summary:	Geary - mail client for GNOME 3
Summary(pl.UTF-8):	Geary - klient pocztowy dla GNOME 3
Name:		geary
Version:	3.34.2
Release:	1
License:	LGPL v2.1+
Group:		X11/Applications/Mail
Source0:	http://ftp.gnome.org/pub/GNOME/sources/geary/3.34/%{name}-%{version}.tar.xz
# Source0-md5:	7917e7b784b13f34a909a5c08e8861aa
Patch0:		%{name}-meson.patch
URL:		https://wiki.gnome.org/Apps/Geary
BuildRequires:	appstream-glib-devel >= 0.7.10
BuildRequires:	desktop-file-utils
BuildRequires:	enchant2-devel >= 2.1
BuildRequires:	folks-devel >= 0.11
BuildRequires:	gcr-devel >= 3.10.1
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.54
BuildRequires:	gmime-devel >= 2.6.17
BuildRequires:	gnome-online-accounts-devel
BuildRequires:	gspell-devel
BuildRequires:	gtk+3-devel >= 3.24.7
BuildRequires:	gtk-webkit4-devel >= 2.24
BuildRequires:	iso-codes
BuildRequires:	json-glib-devel >= 1.0
BuildRequires:	libcanberra-devel >= 0.28
BuildRequires:	libgee-devel >= 0.8.5
BuildRequires:	libhandy-devel >= 0.0.9
BuildRequires:	libnotify-devel >= 0.7.5
BuildRequires:	libsecret-devel >= 0.11
BuildRequires:	libsoup-devel >= 2.48
BuildRequires:	libunwind-devel >= 1.1
BuildRequires:	libxml2-devel >= 1:2.7.8
BuildRequires:	libytnef-devel >= 1.9.3
BuildRequires:	meson >= 0.49
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sqlite3-devel >= 3.12
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 0.22.1
BuildRequires:	vala-folks >= 0.11
BuildRequires:	vala-gcr >= 3.10.1
BuildRequires:	vala-gnome-online-accounts
BuildRequires:	vala-gspell
BuildRequires:	vala-libcanberra >= 0.28
BuildRequires:	vala-libgee >= 0.8.5
BuildRequires:	vala-libhandy >= 0.0.9
BuildRequires:	vala-libsecret >= 0.11
BuildRequires:	valadoc
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.54
Requires(post,postun):	gtk-update-icon-cache
Requires:	appstream-glib >= 0.7.10
Requires:	enchant2 >= 2.1
Requires:	folks >= 0.11
Requires:	gcr >= 3.10.1
Requires:	glib2 >= 1:2.54
Requires:	gmime >= 2.6.17
Requires:	gtk+3 >= 3.24.7
Requires:	gtk-webkit4 >= 2.24
Requires:	hicolor-icon-theme
Requires:	iso-codes
Requires:	json-glib >= 1.0
Requires:	libcanberra >= 0.28
Requires:	libgee >= 0.8.5
Requires:	libhandy >= 0.0.9
Requires:	libsecret >= 0.11
Requires:	libsoup >= 2.48
Requires:	libunwind >= 1.1
Requires:	libxml2 >= 1:2.7.8
Requires:	libytnef >= 1.9.3
Requires:	sqlite3 >= 3.12
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Geary is an email application built around conversations, for the
GNOME 3 desktop. It allows you to read, find and send email with a
straightforward, modern interface.

%description -l pl.UTF-8
Geary to aplikacja do poczty elektronicznej, oparta na rozmowach,
przeznaczona dla środowiska graficznego GNOME 3. Pozwala na czytanie,
wyszukiwanie i wysyłanie wiadomości z bezpośrednim, współczesnym
interfejsem.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	-Dvaladoc=true

%ninja_build -C build

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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
%doc AUTHORS COPYING.{icons,snowball} NEWS README.md THANKS
%attr(755,root,root) %{_bindir}/geary
%dir %{_libdir}/geary
%dir %{_libdir}/geary/web-extensions
%attr(755,root,root) %{_libdir}/geary/web-extensions/libgeary-web-process.so
%{_datadir}/dbus-1/services/org.gnome.Geary.service
%{_datadir}/geary
%{_datadir}/glib-2.0/schemas/org.gnome.Geary.gschema.xml
%{_datadir}/metainfo/org.gnome.Geary.appdata.xml
%{_desktopdir}/org.gnome.Geary.desktop
%{_desktopdir}/geary-autostart.desktop
%{_iconsdir}/hicolor/scalable/actions/close-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/detach-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/edit-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/format-*-symbolic*.svg
%{_iconsdir}/hicolor/scalable/actions/mail-*-symbolic*.svg
%{_iconsdir}/hicolor/scalable/actions/marker-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/tag-symbolic*.svg
%{_iconsdir}/hicolor/scalable/actions/text-x-generic-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Geary.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Geary-symbolic.svg
