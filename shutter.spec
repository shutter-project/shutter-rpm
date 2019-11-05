Name:       shutter
Version:    0.94.3
Release:    1%{?dist}
Summary:    GTK+2-based screenshot application written in Perl
License:    GPLv3+
URL:        http://shutter-project.org
Source0:    https://launchpad.net/shutter/0.9x/%{version}/+download/%{name}-%{version}.tar.gz
BuildArch:  noarch
BuildRequires:  desktop-file-utils
%if 0%{?fedora}
BuildRequires:  perl-interpreter
%endif
BuildRequires:  perl-generators
%if 0%{?fedora} < 26
# BR gnome-web-photo too to ensure it's available for runtime dep too -- rex
BuildRequires: gnome-web-photo
Requires:   gnome-web-photo
%endif
Requires:   ImageMagick
Requires:   perl(Gtk2::ImageView)
Requires:   perl(X11::Protocol::Ext::XFIXES)
Requires:   nautilus-sendto
Requires:   hicolor-icon-theme
Requires:   perl(Gtk2::Unique)
Requires:   perl(Gtk2::AppIndicator)

Requires:   perl(Image::ExifTool)
Requires:   perl(Goo::Canvas)
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?filter_setup:
%filter_provides_in %{_datadir}/%{name}/resources/system/upload_plugins
%filter_setup
}

%description
Shutter is a GTK+ 2.x based screenshot application written in Perl.
Shutter covers all features of common command line tools like
scrot or import and adds reasonable new features combined
with a comfortable GUI using the GTK+ 2.x framework.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p 2
rm -vr share/doc/
# Remove the bundled perl(X11::Protocol::Ext::XFIXES)
rm -vr share/%{name}/resources/modules/X11
rm -vr share/%{name}/resources/modules/WebService

%build

%install
# executable and data
install -d -m 0755 -p $RPM_BUILD_ROOT%{_bindir}
install -d -m 0755 -p $RPM_BUILD_ROOT%{_datadir}
install -d -m 0755 -p $RPM_BUILD_ROOT%{perl_vendorlib}
cp -pfr bin/* $RPM_BUILD_ROOT%{_bindir}/
cp -pfr share/* $RPM_BUILD_ROOT%{_datadir}/
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/resources/modules/* \
   $RPM_BUILD_ROOT%{perl_vendorlib}
rmdir $RPM_BUILD_ROOT%{_datadir}/%{name}/resources/modules/

desktop-file-install --delete-original \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://answers.launchpad.net/shutter/+question/235216
SentUpstream: 2013-09-06
-->
<application>
  <id type="desktop">shutter.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Shutter is a feature-rich screenshot program. You can take a screenshot of a
      specific area, window, your whole screen, or even of a website - apply different
      effects to it, draw on it to highlight points, and then upload to an image
      hosting site, all within one window.
      Shutter is free, open-source, and licensed under GPL v3.
    </p>
    <p>
      Shutter allows you to capture nearly anything on your screen without losing
      control over your screenshots (tabbed interface).
      You don't need to open an external graphics editor like GIMP, because Shutter
      ships with its own built-in editor.
    </p>
  </description>
  <url type="homepage">http://shutter-project.org/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/shutter/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/shutter/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/shutter/c.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/shutter/d.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

%find_lang %{name} --all-name

%files -f %{name}.lang
%doc CHANGES README
%license COPYING
%{_bindir}/%{name}
%{perl_vendorlib}/Shutter/
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_mandir}/man1/%{name}*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/*.*
%{_datadir}/icons/HighContrast/
%{_datadir}/icons/ubuntu-mono-*/*/apps/%{name}-panel.*

%changelog
* Mon Nov 04 2019 Mike Heffner <mikeh@fesnel.com> - 0.94.3-1
- Update to 0.94.3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.93.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.93.1-13
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.93.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.93.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.93.1-10
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.93.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.93.1-8
- use %%license, simplify %%find_lang
- ImageMagick missing from dependencies (#1435789)
- Shutter requires retired orphaned gnome-web-photo (#1436632)
- fix perl-interpretter/gnome-web-photo deps for epel

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.93.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.93.1-6
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.93.1-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.93.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.93.1-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.93.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 17 2015 Robin Lee <cheeselee@fedoraproject.org> - 0.93.1-1
- Update to 0.93.1 (BZ#1178438, BZ#1247730)
- Requires perl(Gtk2::AppIndicator) (BZ#1228973)
- Fix xdg-email usage (BZ#1209360)
- Specfile untabified

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.93-3
- Perl 5.22 rebuild

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 0.93-2
- Add an AppData file for the software center

* Sun Oct 19 2014 Robin Lee <cheeselee@fedoraproject.org> - 0.93-1
- Update to 0.93

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.91-2
- Perl 5.20 rebuild

* Tue Jun 17 2014 Robin Lee <cheeselee@fedoraproject.org> - 0.91-1
- Update to 0.91

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 26 2013 Robin Lee <cheeselee@fedoraproject.org> - 0.90.1-1
- Update to 0.90.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.90-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.90-1
- Update to 0.90

* Mon Aug 20 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.89.1-2
- Remove the bundled perl(X11::Protocol::Ext::XFIXES)

* Thu Aug 16 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.89.1-1
- Update to 0.89.1
- Remove the patch for desktop entry file
- Filtered fake provides
- Add Perl MODULE_COMPAT requires
- Requires perl(X11::Protocol::Ext::XFIXES)
- Don't remove the executable bit of the upload plugins

* Fri Aug 10 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.89-1
- Update to 0.89 (#722700, #753423, #659378, #759686, #754880)
- License changed to GPLv3+
- Patch updated
- Perl modules moved to %%{perl_vendorlib}
- Scriptlet updated
- Other cleanup

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.87.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.87.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Sep 11 2011 Liang Suilong <liangsuilong@gmail.com> - 0.87.3-1
- Upgrade to shutter-0.87.3

* Sat Jun 4 2011 Liang Suilong <liangsuilong@gmail.com> - 0.87.2-1
- Upgrade to shutter-0.87.2
- Add BR: perl(Gtk2::Unique)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.86.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep 13 2010 Liang Suilong <liangsuilong@gmail.com> - 0.86.4-1
- Upgrade to shutter-0.86.2
- Add icons for new version

* Thu May 06 2010 Liang Suilong <liangsuilong@gmail.com> - 0.86.2-1
- Upgrade to shutter-0.86.2
- Add BR: hicolor-icon-theme

* Mon Apr 19 2010 Liang Suilong <liangsuilong@gmail.com> - 0.86.1-1
- Upgrade to shutter-0.86.1

* Tue Mar 2 2010 Liang Suilong <liangsuilong@gmail.com> - 0.85.1-2
- Remove BR:gtklp
- fix the bug of directory ownership

* Mon Dec 7 2009 Liang Suilong <liangsuilong@gmail.com> - 0.85.1-1
- Upgrade to shutter-0.85.1

* Sat Nov 21 2009 Liang Suilong <liangsuilong@gmail.com> - 0.85-1
- Upgrade to shutter-0.85

* Mon Aug 3 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80.1-1
- Updrade to shutter-0.80.1

* Mon Aug 3 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-5
- Update %%install script

* Wed Jul 29 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-4
- Update %%install script

* Mon Jul 20 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-3
- Add perl(X11::Protocol) as require

* Thu Jun 25 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-2
- Upstream to shutter-0.80 Final GA

* Thu Jun 25 2009 Liang Suilong <liangsuilong@gmail.com> - 0.80-1.ppa6
- Upstream to shutter-0.80~ppa6
- Update the SPEC file

* Thu Jun 25 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.2-3.ppa4
- Remove share/shutter/resources/pofiles/
- Remove share/shutter/resources/modules/File
- Remove share/shutter/resources/pofiles/Proc

* Wed Apr 15 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.2-2.ppa4
- Add a desktop-file-utils as BuildRequires

* Wed Apr 15 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.2-2.ppa3
- Add a desktop-file-utils as BuildRequires

* Sun Jan 18 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.2-1
- Upstream to 0.70.2

* Sun Jan 18 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70.1-1
- Upstream to 0.70.1

* Sun Jan 18 2009 Liang Suilong <liangsuilong@gmail.com> - 0.70-1
- Upstream to 0.70

* Sun Jan 18 2009 Liang Suilong <liangsuilong@gmail.com> - 0.64-2
- Add several Requires so that advanced functions can run.
- Fix the authoritie of install path.

* Fri Jan 02 2009 bbbush <bbbush.yuan@gmail.com> - 0.64-1
- update to 0.64, clean up spec

* Mon Dec 29 2008 Liang Suilong <liangsuilong@gmail.com> - 0.63-3
- Initial package for Fedora
