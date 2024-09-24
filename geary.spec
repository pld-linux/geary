#
# Conditional build:
%bcond_with	unity	# Unity integration (messaging-menu)

Summary:	Geary - mail client for GNOME 3
Summary(pl.UTF-8):	Geary - klient pocztowy dla GNOME 3
Name:		geary
Version:	46.0
Release:	2
License:	LGPL v2.1+
Group:		X11/Applications/Mail
Source0:	https://download.gnome.org/sources/geary/46/%{name}-%{version}.tar.xz
# Source0-md5:	a76664c8b5690965e1251e92afa60a65
Patch0:		%{name}-meson.patch
URL:		https://wiki.gnome.org/Apps/Geary
BuildRequires:	appstream-glib-devel >= 0.7.10
BuildRequires:	cairo-devel
BuildRequires:	desktop-file-utils
BuildRequires:	enchant2-devel >= 2.1
BuildRequires:	folks-devel >= 0.11
BuildRequires:	gcr-devel >= 3.10.1
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.68
BuildRequires:	gmime3-devel >= 3.2.4
BuildRequires:	gnome-online-accounts-devel
BuildRequires:	gsound-devel
BuildRequires:	gspell-devel
BuildRequires:	gtk+3-devel >= 3.24.24
BuildRequires:	gtk-webkit4.1-devel >= 2.34
BuildRequires:	iso-codes
BuildRequires:	json-glib-devel >= 1.0
BuildRequires:	libcanberra-devel >= 0.28
BuildRequires:	libgee-devel >= 0.8.5
BuildRequires:	libhandy1-devel >= 1.2.1
BuildRequires:	libicu-devel >= 60
%{?with_unity:BuildRequires:	indicator-messages-devel >= 12.10}
BuildRequires:	libnotify-devel >= 0.7.5
BuildRequires:	libpeas-devel >= 1.24.0
BuildRequires:	libpeas-gtk-devel >= 1.24.0
BuildRequires:	libsecret-devel >= 0.11
BuildRequires:	libsoup3-devel >= 3.0
BuildRequires:	libstemmer-devel
BuildRequires:	libunwind-devel >= 1.1
BuildRequires:	libxml2-devel >= 1:2.7.8
BuildRequires:	libytnef-devel >= 1.9.3
BuildRequires:	meson >= 0.59
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.24
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.48.18
BuildRequires:	vala-folks >= 0.11
BuildRequires:	vala-gcr >= 3.10.1
BuildRequires:	vala-gmime3 >= 3.2.4
BuildRequires:	vala-gnome-online-accounts
BuildRequires:	vala-gsound
BuildRequires:	vala-gspell
%{?with_unity:BuildRequires:	vala-indicator-messages >= 12.10}
BuildRequires:	vala-libcanberra >= 0.28
BuildRequires:	vala-libgee >= 0.8.5
BuildRequires:	vala-libhandy1 >= 1.2.1
BuildRequires:	vala-libsecret >= 0.11
BuildRequires:	valadoc
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.68
Requires(post,postun):	gtk-update-icon-cache
Requires:	appstream-glib >= 0.7.10
Requires:	enchant2 >= 2.1
Requires:	folks >= 0.11
Requires:	gcr >= 3.10.1
Requires:	glib2 >= 1:2.68
Requires:	gmime3 >= 3.2.4
Requires:	gtk+3 >= 3.24.24
Requires:	gtk-webkit4.1 >= 2.34
Requires:	hicolor-icon-theme
%{?with_unity:Requires:	indicator-messages-libs >= 12.10}
Requires:	iso-codes
Requires:	json-glib >= 1.0
Requires:	libcanberra >= 0.28
Requires:	libgee >= 0.8.5
Requires:	libhandy1 >= 1.2.1
Requires:	libpeas >= 1.24.0
Requires:	libpeas-gtk >= 1.24.0
Requires:	libsecret >= 0.11
Requires:	libsoup3 >= 3.0
Requires:	libunwind >= 1.1
Requires:	libxml2 >= 1:2.7.8
Requires:	libytnef >= 1.9.3
Requires:	sqlite3 >= 3.24
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

%if %{without unity}
%{__sed} -i -e '/^subdir.*messaging-menu/ d' src/client/plugin/meson.build
%endif

%build
CPPFLAGS="%{rpmcppflags} -I/usr/include/libstemmer"
%meson build \
	--default-library=shared \
	-Dprofile=release \
	-Dvaladoc=enabled

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

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
%doc AUTHORS COPYING.icons NEWS README.md THANKS
%attr(755,root,root) %{_bindir}/geary
%dir %{_libdir}/geary
%attr(755,root,root) %{_libdir}/geary/libgeary-client-%{version}.so
%dir %{_libdir}/geary/web-extensions
%attr(755,root,root) %{_libdir}/geary/web-extensions/libgeary-web-process.so
%dir %{_libdir}/geary/plugins

%dir %{_libdir}/geary/plugins/desktop-notifications
%attr(755,root,root) %{_libdir}/geary/plugins/desktop-notifications/libdesktop-notifications.so
%{_libdir}/geary/plugins/desktop-notifications/desktop-notifications.plugin

%dir %{_libdir}/geary/plugins/email-templates
%attr(755,root,root) %{_libdir}/geary/plugins/email-templates/libemail-templates.so
%{_libdir}/geary/plugins/email-templates/email-templates.plugin

%dir %{_libdir}/geary/plugins/folder-highlight
%attr(755,root,root) %{_libdir}/geary/plugins/folder-highlight/libfolder-highlight.so
%{_libdir}/geary/plugins/folder-highlight/folder-highlight.plugin

%dir %{_libdir}/geary/plugins/mail-merge
%attr(755,root,root) %{_libdir}/geary/plugins/mail-merge/libmail-merge.so
%{_libdir}/geary/plugins/mail-merge/mail-merge.plugin

%dir %{_libdir}/geary/plugins/notification-badge
%attr(755,root,root) %{_libdir}/geary/plugins/notification-badge/libnotification-badge.so
%{_libdir}/geary/plugins/notification-badge/notification-badge.plugin

%dir %{_libdir}/geary/plugins/sent-sound
%attr(755,root,root) %{_libdir}/geary/plugins/sent-sound/libsent-sound.so
%{_libdir}/geary/plugins/sent-sound/sent-sound.plugin

%dir %{_libdir}/geary/plugins/special-folders
%attr(755,root,root) %{_libdir}/geary/plugins/special-folders/libspecial-folders.so
%{_libdir}/geary/plugins/special-folders/special-folders.plugin

%{_datadir}/dbus-1/services/org.gnome.Geary.service
%{_datadir}/geary
%{_datadir}/glib-2.0/schemas/org.gnome.Geary.gschema.xml
%{_datadir}/metainfo/org.gnome.Geary.appdata.xml
%{_desktopdir}/org.gnome.Geary.desktop
%{_desktopdir}/geary-autostart.desktop
%{_iconsdir}/hicolor/scalable/actions/close-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/detach-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/edit-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/font-color-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/font-size-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/format-*-symbolic*.svg
%{_iconsdir}/hicolor/scalable/actions/mail-*-symbolic*.svg
%{_iconsdir}/hicolor/scalable/actions/tag-symbolic*.svg
%{_iconsdir}/hicolor/scalable/actions/text-x-generic-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Geary.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Geary-symbolic.svg
