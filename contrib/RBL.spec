%global systemd (0%{?fedora} >= 18) || (0%{?rhel} >= 7)
%global upname rbl
%global bigname RBL

Summary: A complete, more than an RBL Management System.
Name: rblmanager
Version: 2.4.4
Release: 1%{?dist}
Group: System Environment/Daemons
License: Apache-2.0
URL: https://falon.github.io/%{bigname}/
Source0: https://github.com/falon/%{bigname}/archive/master.zip
BuildArch:	noarch

# Required for all versions
Requires: httpd >= 2.4.6
Requires: mod_ssl >= 2.4.6
Requires: php >= 7.1
Requires: php-imap >= 7.1
Requires: php-json >= 7.1
Requires: php-ldap >= 7.1
Requires: php-mysqlnd >= 7.1
Requires: php-gmp >= 7.1
Requires: php-xml >= 7.1
BuildRequires: composer >= 1.5.2
#Requires: remi-release >= 7.3


%if %systemd
# Required for systemd
%{?systemd_requires}
BuildRequires: systemd
%endif

%description
%{upname} (RBL Manager)
provides an open source Blocklist Management System of various types.
RBLDNS lists, MySQL lists for Postfix or for Amavis too. You can
manage lists of ips, networks, domains, emails or account names.
Every entry has an expiration time. You can manage the entries
manually, or by authomated process from Spam Learning system or
Splunk alert.

%package mailClassifier
Summary: A complete view on authentication and spam classification of your mails.
Group: System Environment/Web
Requires: dspam-client >= 3.10.2
Requires: rblmanager = 2.4.4-1%{?dist}

%description mailClassifier
Show how your mail are authenticated by DKIM, SPF and DMARC.
View the Spam Classification by Spamassassin and DSPAM. Optionally,
learn your mails using DSPAM Client.


%clean
rm -rf %{buildroot}/

%prep
%autosetup -n %{bigname}-master


%install

%if %systemd
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/rbl-amavis.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/rbl-amavis.timer %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/rbl-expire.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/rbl-expire.timer %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/rbl-ipimap.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/rbl-ipimap.timer %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/rbl-rbldns@.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/rbl-rbldns@spamip.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/rbl-rbldns@whiteip.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/status-email-sysadmin@.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/usr/bin
install -m 0755 contrib/systemd/systemd-email %{buildroot}/usr/bin
install -D -m0644 contrib/systemd/systemd-email.conf-default %{buildroot}%{_sysconfdir}/sysconfig/systemd-email.conf
sed -i 's|\/usr\/local\/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_unitdir}/*.service
%endif
rm -rf contrib/systemd contrib/RPM

# Include dir
mkdir -p %{buildroot}%{_datadir}/include
install -m0444 ajaxsbmt.js %{buildroot}%{_datadir}/include
install -m0444 pleasewait.gif %{buildroot}%{_datadir}/include
wget -qO- 'https://github.com/splunk/splunk-sdk-php/archive/1.0.1.tar.gz' | tar xvz -C %{buildroot}%{_datadir}/include
install -m0444 style.css  %{buildroot}%{_datadir}/include
rm -rf ajaxsbmt.js pleasewait.gif

# Web HTTPD conf

install -D -m0444 contrib/%{bigname}.conf-default %{buildroot}%{_sysconfdir}/httpd/conf.d/%{bigname}.conf
sed -i 's|\/var\/www\/html\/include|%{_datadir}/include|' %{buildroot}%{_sysconfdir}/httpd/conf.d/%{bigname}.conf
sed -i 's|\/var\/www\/html\/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_sysconfdir}/httpd/conf.d/%{bigname}.conf
install -D -m0444 contrib/mailClassifier/%{bigname}-mailClassifier.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/
sed -i 's|\/var\/www\/html\/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_sysconfdir}/httpd/conf.d/%{bigname}-mailClassifier.conf

# RBL manager application files
mkdir -p %{buildroot}%{_datadir}/%{bigname}
cp -a * %{buildroot}%{_datadir}/%{bigname}/
mv %{buildroot}%{_datadir}/%{bigname}/imap.conf-default %{buildroot}%{_datadir}/%{bigname}/imap.conf
sed -i 's|\/var\/www\/html\/include|%{_datadir}/include|' %{buildroot}%{_datadir}/%{bigname}/imap.conf
sed -i 's|\/var\/www\/html\/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_datadir}/%{bigname}/contrib/ipImap/getip.php
mv %{buildroot}%{_datadir}/%{bigname}/config.php-default %{buildroot}%{_datadir}/%{bigname}/config.php
mv %{buildroot}%{_datadir}/%{bigname}/notifyDomains.conf-default %{buildroot}%{_datadir}/%{bigname}/notifyDomains.conf
mv %{buildroot}%{_datadir}/%{bigname}/contrib/splunk/listEmail.conf-default %{buildroot}%{_datadir}/%{bigname}/contrib/splunk/listEmail.conf
mv %{buildroot}%{_datadir}/%{bigname}/template-default %{buildroot}%{_datadir}/%{bigname}/template
mv %{buildroot}%{_datadir}/%{bigname}/contrib/amavis/exportAmavisLdap.php-default  %{buildroot}%{_datadir}/%{bigname}/contrib/amavis/exportAmavisLdap.php
mv %{buildroot}%{_datadir}/%{bigname}/contrib/mailClassifier/imap.conf-default %{buildroot}%{_datadir}/%{bigname}/contrib/mailClassifier/imap.conf
sed -i 's|\/var\/www\/html\/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_datadir}/%{bigname}/contrib/amavis/exportAmavisLdap.php
sed -i 's|\/var\/www\/html/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_datadir}/%{bigname}/contrib/expire.php
sed -i 's|\/var\/www\/html/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_datadir}/%{bigname}/contrib/rbldns/exportdns.php
sed -i 's|\/var\/www\/html/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_datadir}/%{bigname}/contrib/splunk/webhook/readPost.php
sed -i 's|\/var\/www\/html/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_datadir}/%{bigname}/contrib/mailClassifier/index.php
sed -i 's|\/var\/www\/html/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_datadir}/%{bigname}/contrib/mailClassifier/learn.php
sed -i 's|\/var\/www\/html/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_datadir}/%{bigname}/contrib/mailClassifier/list.php
sed -i 's|\/var\/www\/html/%{bigname}|%{_datadir}/%{bigname}|' %{buildroot}%{_datadir}/%{bigname}/contrib/mailClassifier/result.php
##Composer requirement
composer --working-dir="%{buildroot}%{_datadir}/%{bigname}" require dautkom/php.ipv4
## Remove unnecessary files
rm %{buildroot}%{_datadir}/%{bigname}/_config.yml %{buildroot}%{_datadir}/%{bigname}/contrib/%{bigname}.conf-default %{buildroot}%{_datadir}/%{bigname}/contrib/mailClassifier/%{bigname}-mailClassifier.conf %{buildroot}%{_datadir}/%{bigname}/contrib/%{bigname}.spec %{buildroot}%{_datadir}/%{bigname}/vendor/dautkom/php.ipv4/.gitignore %{buildroot}%{_datadir}/%{bigname}/composer.*

##File list
find %{buildroot}%{_datadir}/%{bigname} -mindepth 1 -type f | grep -v \.conf$ | grep -v \.git | grep -v '\-default$' | grep -v ipImap/report/*\.html | grep -v config\.php | grep -v template/ | grep -v contrib/rbldns/conf\.default | grep -v contrib/mailClassifier | grep -v RBL\.spec | grep -v 'doc/' | grep -v %{bigname}/LICENSE | grep -v %{bigname}/README\.md | grep -v contrib/amavis/exportAmavisLdap\.php | sed -e "s@$RPM_BUILD_ROOT@@" > FILELIST
find %{buildroot}%{_datadir}/%{bigname}/contrib/mailClassifier -mindepth 1 -type f | grep -v \.conf$ | grep -v '\-default$' | sed -e "s@$RPM_BUILD_ROOT@@" > FLMC
mkdir %{buildroot}%{_datadir}/%{bigname}/contrib/rbldns/yourbl

%post
%if %systemd
%systemd_post rbl-expire.timer
%endif
case "$1" in
  2)
	echo -en "\n\n\e[33mRemember to check the changes in imap.conf.\e[39m\n\n"
  ;;
esac

%preun
%if %systemd
%systemd_preun %{upname}-*.service
%systemd_preun %{upname}-*.timer
%endif

%postun
%if %systemd
%systemd_postun_with_restart %{upname}-*.service
%systemd_postun_with_restart %{upname}-*.timer
%endif

%files -f FILELIST
%{_datadir}/include
%{_unitdir}
/usr/bin/systemd-email
%dir %{_datadir}/%{bigname}/contrib/rbldns/yourbl
%license %{_datadir}/%{bigname}/LICENSE
%doc %{_datadir}/%{bigname}/README.md
%doc %{_datadir}/%{bigname}/doc
%config(noreplace) %{_sysconfdir}/sysconfig/systemd-email.conf
%config(noreplace) %{_datadir}/%{bigname}/config.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{bigname}.conf
%config(noreplace) %{_datadir}/%{bigname}/imap.conf
%config(noreplace) %{_datadir}/%{bigname}/notifyDomains.conf
%config(noreplace) %{_datadir}/%{bigname}/contrib/splunk/listEmail.conf
%config(noreplace) %{_datadir}/%{bigname}/contrib/amavis/exportAmavisLdap.php
%config(noreplace) %{_datadir}/%{bigname}/template/mailWarnHeaders.eml
%config(noreplace) %{_datadir}/%{bigname}/template/mailWarn.eml
%config(noreplace) %{_datadir}/%{bigname}/contrib/rbldns/conf.default

%files mailClassifier -f FLMC
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{bigname}-mailClassifier.conf
%config(noreplace) %{_datadir}/%{bigname}/contrib/mailClassifier/imap.conf

%changelog
* Thu Apr 05 2018 Marco Favero <marco.favero@csi.it> 2.4.4-1
- systemd-email installs as a config file.

* Thu Apr 05 2018 Marco Favero <marco.favero@csi.it> 2.4.4-0
- Minor fixes on SPF Result for mailClassifier
- Added systemd email notifier to all services.

* Tue Feb 16 2018 Marco Favero <marco.favero@csi.it> 2.4.3-0
- Fixed listing domains: recursive check against NS record.

* Tue Feb 15 2018 Marco Favero <marco.favero@csi.it> 2.4.2-0
- Fixed regexp in getDomain function for Learn Tool.
- Added domains exclusion list in imap.conf

* Tue Feb 14 2018 Marco Favero <marco.favero@csi.it> 2.4.1-0
- Fixed regexp in getDomain function for Learn Tool.

* Tue Feb 13 2018 Marco Favero <marco.favero@csi.it> 2.4.0-0
- New version with ability to autolist domains with Learn Tool.

* Thu Jan 25 2018 Marco Favero <marco.favero@csi.it> 2.3.1-0
- New minor version with domain names sanity check

* Thu Dec 21 2017 Marco Favero <marco.favero@csi.it> 2.3-4
- Minor change in presentation, minor fixes

* Thu Dec 21 2017 Marco Favero <marco.favero@csi.it> 2.3-2
- New style for minor fix in mailClassifier

* Wed Dec 20 2017 Marco Favero <marco.favero@csi.it> 2.3-0
- New version with mailClassifier (no other changes)

* Thu Nov 23 2017 Marco Favero <marco.favero@csi.it> 2.2-5
- modified rbl-ipimap.service
- fixed path in getip.php

* Mon Nov 22 2017 Marco Favero <marco.favero@csi.it> - Initial version
- Build for 2.2 official version
