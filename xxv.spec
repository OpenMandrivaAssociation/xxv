Summary:	Xtreme eXtension for VDR
Name:		xxv
Version:	1.6.1
Release:	6
Group:		Video
License:	LGPL
URL:		http://xpix.dieserver.de/
Source:		http://xpix.dieserver.de/downloads/xxv/%name-%version.tgz
Source2:	xxv.service
Source3:	xxv.sysconfig
Source4:	xxv.logrotate
# (Anssi 02/2008) In initscript we precreate empty pidfile so that vdr user
# has the rights to write there:
Patch0:		xxv-1.2-ignore-empty-pidfile.patch
BuildArch:	noarch
# for macros:
BuildRequires:	vdr-devel
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires:	vdr-common
Suggests:	mysql
#Requires:	vdr2jpeg
Requires:	fonts-ttf-bitstream-vera
# most 'use' statements are 'eval'ed, so we have to add requires manually;
# external versions of bundled libraries
Requires:	perl(Locale::Maketext::Extract)
Requires:	perl(Locale::Maketext::Lexicon)
Requires:	perl(Mail::SendEasy)
Requires:	perl(Module::Reload)
Requires:	perl(MP3::Icecast)
Requires:	perl(Net::IP::Match::Regexp)
Requires:	perl(Term::ReadLine::Perl)
Requires:	perl(Text::ASCIITable)
# list of requirements from install.sh
# sed -nr 's,^.*checkPerlModule (.*)$,Requires:\tperl(\1),p' install.sh
Requires:	perl(CGI)
Requires:	perl(Compress::Zlib)
Requires:	perl(Config::Tiny)
Requires:	perl(Data::Dumper)
Requires:	perl(Date::Manip)
Requires:	perl(DBD::mysql)
Requires:	perl(DBI)
Requires:	perl(Digest::MD5)
Requires:	perl(Digest::HMAC_MD5)
Requires:	perl(Encode)
Requires:	perl(Event)
Requires:	perl(Font::TTF::Font)
Requires:	perl(GD)
Requires:	perl(Getopt::Long)
Requires:	perl(HTML::TextToHTML)
Requires:	perl(HTML::TreeBuilder)
Requires:	perl(JSON)
# mdv bug #52269
Requires:	perl-JSON
Requires:	perl(Linux::Inotify2)
Requires:	perl(LWP::Simple)
Requires:	perl(LWP::UserAgent)
Requires:	perl(Locale::gettext)
Requires:	perl(MIME::Base64)
Requires:	perl(MP3::Info)
Requires:	perl(Net::Amazon)
Requires:	perl(Net::Amazon::Request::Artist)
Requires:	perl(Net::XMPP)
Requires:	perl(Proc::Killfam)
Requires:	perl(Proc::ProcessTable)
Requires:	perl(SOAP::Lite)
Requires:	perl(SOAP::Transport::HTTP)
Requires:	perl(Template)
Requires:	perl(Time::Local)
Requires:	perl(Time::HiRes)
Requires:	perl(URI::Escape)
Requires:	perl(XML::RSS)
Requires:	perl(XML::Simple)

%define __noautoreq 'perl\\(Tools\\)|perl\\(SOAP::Transport::HTTP::Event\\)|perl\\(Data::COW.*|perl\\(MediaLibParser.*|perl\\(XXV.*'
%define __noautoprov 'perl\\(Tools\\)|perl\\(SOAP::Transport::HTTP::Event\\)|perl\\(Data::COW.*|perl\\(MediaLibParser.*'

%description
XXV means "Xtreme eXtension for VDR" and is a central service is for
the administration of the VDR and its environment, with which
different of haven are open and these different services can serve.

An additional haven over a Plugin to construct should be just as
simple, to make available as also a certain service. The letter of a
Plugins goes very fast, there the input (Vdr, Database etc.) as well
as the output (telnet, HTTP...) generically was realized. It should
be e.g. possible thus to register with a telnet CONSOLE,
HttpBrowser, Wapphone, etc. an autotimer. This should substantially
faster the EPG data to scan be able (MySQL data base) and over an
interface the VDR the new timer communicate. Naturally also is
considered to the single mode of the SVdrP and only one instruction
is mailed. Afterwards the haven is again closed immediately, so that
other programs can access again svdrp.

%prep
%setup -q
%patch0 -p1

# Setup default config
perl -pi -e 's,file=/video/channels.conf,file=%{_vdr_cfgdir}/channels.conf,' etc/xxvd.cfg.example
#perl -pi -e 's,epgfile=/video/epg.data,epgfile=%{_vdr_videodir}/epg.data,' etc/xxvd.cfg.example
perl -pi -e 's,epgimages=/var/cache/xxv/epgimages,epgimages=%{_vdr_videodir}/epgimages,' etc/xxvd.cfg.example
perl -pi -e 's,Language=de_DE,Language=en_US,' etc/xxvd.cfg.example
#perl -pi -e 's,initscript=/etc/init.d/xxvd,initscript=%{_unitdir}/xxv,' etc/xxvd.cfg.example
perl -pi -e 's,commandfile=/video/reccmds.conf,file=%{_vdr_cfgdir}/reccmds.conf,' etc/xxvd.cfg.example
perl -pi -e 's,videodir=/video,videodir=%{_vdr_videodir},' etc/xxvd.cfg.example
perl -pi -e 's,commands=/video/commands.conf,commands=%{_vdr_cfgdir}/commands.conf,' etc/xxvd.cfg.example
#perl -pi -e 's,file=/video/timers.conf,file=%{_vdr_cfgdir}/timers.conf,' etc/xxvd.cfg.example
perl -pi -e 's,tempimages=/var/cache/xxv/temp,tempimages=%{_var}/cache/%{name}/temp,' etc/xxvd.cfg.example
perl -pi -e 's,dir=/vtx,dir=%{_vdr_plugin_cachedir}/osdteletext,' etc/xxvd.cfg.example

perl -pi -e 's,"\$RealBin/../lib","%{_datadir}/%{name}",' bin/xxvd
perl -pi -e 's,"/var/log/xxvd.log","%{_logdir}/%{name}/xxvd.log",' bin/xxvd
perl -pi -e 's,"\$RealBin/../locale","%{_datadir}/locale",' bin/xxvd
perl -pi -e 's,"\$RealBin/../lib/XXV,"%{_datadir}/%{name}/XXV,' bin/xxvd
perl -pi -e 's,"\$RealBin/../etc/xxvd.cfg","%{_localstatedir}/lib/%{name}/xxvd.cfg",' bin/xxvd
perl -pi -e 's,"\$RealBin/../doc","%{_localstatedir}/lib/%{name}/doc",' bin/xxvd
sed -i '/HTMLDIR/s,"\$RealBin/../","%{_datadir}/%{name}/skins",' bin/xxvd
perl -pi -e 's,"\$RealBin/../share/fonts/ttf-bitstream-vera,"%{_datadir}/fonts/TTF,' bin/xxvd
perl -pi -e 's,"\$RealBin/../share/,"%{_datadir}/%{name}/,' bin/xxvd
perl -pi -e 's,"\$RealBin/../contrib","%{_datadir}/%{name}/contrib",' bin/xxvd

perl -pi -e "s,upgrade='upgrade-xxv-db.sql',upgrade='%{_datadir}/%{name}/contrib/upgrade-xxv-db.sql'," contrib/update-xxv

cat > README.install.urpmi <<EOF
You must create the database "xxv" on your mysql server, create a
mysql user for xxv and enter the correct USR and PWD in the
[General] section of %{_localstatedir}/lib/%{name}/xxvd.cfg.

You can create the database with default password with the following
command:
mysql -u root < %{_datadir}/%{name}/contrib/create-database.sql
No xxvd.cfg editing is then necessary.

Alternatively, here are the example commands for creating a new
database with different credentials:
mysql -u root -e "create database xxv;"
mysql -u root -e "grant all privileges on xxv.* to username@localhost IDENTIFIED BY 'password';"
mysql -u root -e "flush privileges;"

If you wish to later change the username and/or password, you must
change both the xxvd.cfg entry and the one of mysql.

By default the web interface is on port 8080 with username "xxv"
and password "xxv". You can change these from the web interface.
Please go through the configuration options carefully and disable
the modules you do not need.
EOF

cat > README.1.4.upgrade.urpmi <<EOF
In order to update to the new XXV database version, you need to manually
run update-xxv command. XXV must be stopped when updating the database.
See "update-xxv -h" for the proper parameters that may be needed.
EOF

%install
install -d -m755 %{buildroot}%{_bindir}
install -m755 bin/xxvd %{buildroot}%{_bindir}

install -d -m755 %{buildroot}%{_sysconfdir}
install -d -m755 %{buildroot}%{_localstatedir}/lib/%{name}
install -m644 etc/xxvd.cfg.example %{buildroot}%{_localstatedir}/lib/%{name}/xxvd.cfg
ln -s %{_localstatedir}/lib/%{name} %{buildroot}%{_sysconfdir}/%{name}

install -d -m755 %{buildroot}%{_var}/cache/%{name}

install -d -m755 %{buildroot}%{_datadir}/%{name}/contrib
install -m644 contrib/*.sql %{buildroot}%{_datadir}/%{name}/contrib
install -m755 contrib/update-xxv %{buildroot}%{_datadir}/%{name}/contrib
install -m755 contrib/*.pl %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/contrib/update-xxv %{buildroot}%{_bindir}/update-xxv

install -d -m755 %{buildroot}%{_localstatedir}/lib/%{name}/doc
install -m644 doc/* %{buildroot}%{_localstatedir}/lib/%{name}/doc

install -d -m755 %{buildroot}%{_sysconfdir}/logrotate.d
install -m644 %SOURCE4 %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -d -m755 %{buildroot}%{_datadir}/%{name}/skins
cp -a wml html %{buildroot}%{_datadir}/%{name}/skins
ln -s html %{buildroot}%{_datadir}/%{name}/skins/default

cp -a lib/* share/* %{buildroot}%{_datadir}/%{name}
cp -a lib/Tools.pm lib/XXV lib/Data lib/SOAP lib/MediaLibParser* share/* %{buildroot}%{_datadir}/%{name}

# remove bundled stuff we have a system version for
rm -r %{buildroot}%{_datadir}/%{name}/Locale/Maketext/Extract*
rm -r %{buildroot}%{_datadir}/%{name}/Locale/Maketext/Lexicon*
rm -r %{buildroot}%{_datadir}/%{name}/Mail/SendEasy*
rm -r %{buildroot}%{_datadir}/%{name}/Module/Reload*
rm -r %{buildroot}%{_datadir}/%{name}/MP3/Icecast*
rm -r %{buildroot}%{_datadir}/%{name}/Net/IP/Match/Regexp*
rm -r %{buildroot}%{_datadir}/%{name}/Term/ReadLine/{Perl*,readline*}
rm -r %{buildroot}%{_datadir}/%{name}/Text/ASCIITable*
rm -r %{buildroot}%{_datadir}/%{name}/fonts/ttf-bitstream-vera

# remove bundle
rm -r %{buildroot}%{_datadir}/%{name}/Bundle

for f in locale/*/; do
	install -d -m755 \
		%{buildroot}%{_datadir}/locale/$(basename $f)/LC_MESSAGES
	install -m644 $f/LC_MESSAGES/xxv.mo \
		%{buildroot}%{_datadir}/locale/$(basename $f)/LC_MESSAGES
done

install -d -m755 %{buildroot}%{_logdir}/%{name}

install -d -m755 %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/xxv

install -d -m755 %{buildroot}%{_unitdir}
install -m755 %{SOURCE2} %{buildroot}%{_unitdir}/xxv.service

install -d -m755 %{buildroot}%{_logdir}/xxv

install -d -m755 %{buildroot}%{_mandir}/man1
install -m644 doc/*.1  %{buildroot}%{_mandir}/man1

%find_lang xxv

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files -f xxv.lang
%doc doc/{CHANGELOG,README} README.install.urpmi README.*.upgrade.urpmi
%attr(-,vdr,vdr) %dir %{_localstatedir}/lib/xxv
%attr(-,vdr,vdr) %dir %{_logdir}/xxv
%attr(0640,vdr,vdr) %config(noreplace) %{_localstatedir}/lib/xxv/xxvd.cfg
%attr(-,vdr,vdr) %{_var}/cache/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/xxv
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,vdr,vdr) %dir %{_localstatedir}/lib/xxv/doc
%attr(-,vdr,vdr) %{_localstatedir}/lib/xxv/doc/*
%{_sysconfdir}/xxv
%{_unitdir}/xxv*
%{_bindir}/xxvd
%{_bindir}/at-vdradmin2xxv.pl
%{_bindir}/chronicle-remove-duplicate.pl
%{_bindir}/update-xxv
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/Data
%{_datadir}/%{name}/Data/COW.pm
%{_datadir}/%{name}/MediaLibParser*
%dir %{_datadir}/%{name}/SOAP
%dir %{_datadir}/%{name}/SOAP/Transport
%dir %{_datadir}/%{name}/SOAP/Transport/HTTP
%{_datadir}/%{name}/SOAP/Transport/HTTP/Event.pm
%{_datadir}/%{name}/Tools.pm
%{_datadir}/%{name}/XXV
%{_datadir}/%{name}/contrib
%{_datadir}/%{name}/news
%{_datadir}/%{name}/skins
%{_datadir}/%{name}/xmltv
%{_mandir}/man1/xxvd.1*
