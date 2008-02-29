
%define name	xxv
%define version	1.2
%define rel	1

Summary:	Xtreme eXtension for VDR
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	LGPL
URL:		http://xpix.dieserver.de/
Source:		http://xpix.dieserver.de/downloads/xxv/%name-%version.tgz
Source2:	xxv.init
Source3:	xxv.sysconfig
Source4:	xxv.logrotate
# (Anssi 02/2008) In initscript we precreate empty pidfile so that vdr user
# has the rights to write there:
Patch0:		xxv-1.2-ignore-empty-pidfile.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch
# for macros:
BuildRequires:	vdr-devel
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires:	vdr-common
Requires:	mysql
Requires:	vdr2jpeg
# find-requires fails to add:
Requires:	perl(Config::Tiny)
Requires:	perl(Net::IP::Match::Regexp)
Requires:	perl(Term::ReadLine::Perl)
Requires:	perl(Module::Reload)
Requires:	perl(Mail::SendEasy)
Requires:	perl(Net::XMPP)
Requires:	perl(MP3::Icecast)
Requires:	perl(Net::Amazon::Request::Artist)
Requires:	perl(Proc::Killfam)

%define _provides_exceptions perl(HTML::TextToHTML)\\|perl(SOAPService)\\|perl(SOAP::Transport::HTTP::Event)\\|perl(Tools)
%define _requires_exceptions perl(HTML::TextToHTML)\\|perl(SOAPService)\\|perl(SOAP::Transport::HTTP::Event)\\|perl(Tools)

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

# Corruption?
perl -pi -e 's/^.*package XXV::OUTPUT::Wml;$/package XXV::OUTPUT::Wml;/' lib/XXV/OUTPUT/Wml.pm

# Setup default config
perl -pi -e 's,file=/video/channels.conf,file=%{_vdr_cfgdir}/channels.conf,' etc/xxvd.cfg.example
#perl -pi -e 's,epgfile=/video/epg.data,epgfile=%{_vdr_videodir}/epg.data,' etc/xxvd.cfg.example
perl -pi -e 's,epgimages=/var/cache/xxv/epgimages,epgimages=%{_vdr_videodir}/epgimages,' etc/xxvd.cfg.example
perl -pi -e 's,Language=de_DE,Language=en_US,' etc/xxvd.cfg.example
perl -pi -e 's,initscript=/etc/init.d/xxvd,initscript=%{_initrddir}/xxvd,' etc/xxvd.cfg.example
perl -pi -e 's,commandfile=/video/reccmds.conf,file=%{_vdr_cfgdir}/reccmds.conf,' etc/xxvd.cfg.example
perl -pi -e 's,videodir=/video,videodir=%{_vdr_videodir},' etc/xxvd.cfg.example
perl -pi -e 's,commands=/video/commands.conf,commands=%{_vdr_cfgdir}/commands.conf,' etc/xxvd.cfg.example
perl -pi -e 's,file=/video/timers.conf,file=%{_vdr_cfgdir}/timers.conf,' etc/xxvd.cfg.example
perl -pi -e 's,tempimages=/var/cache/xxv/temp,tempimages=%{_var}/cache/%{name}/temp,' etc/xxvd.cfg.example
perl -pi -e 's,dir=/vtx,dir=%{_vdr_plugin_cachedir}/osdteletext,' etc/xxvd.cfg.example

perl -pi -e 's,"\$RealBin/../lib","%{_datadir}/%{name}",' bin/xxvd
perl -pi -e 's,"/var/log/xxvd.log","%{_logdir}/%{name}/xxvd.log",' bin/xxvd
perl -pi -e 's,"\$RealBin/../locale","%{_datadir}/locale",' bin/xxvd
perl -pi -e 's,"\$RealBin/../lib/XXV,"%{_datadir}/%{name}/XXV,' bin/xxvd
perl -pi -e 's,"\$RealBin/../etc/xxvd.cfg","%{_localstatedir}/%{name}/xxvd.cfg",' bin/xxvd
perl -pi -e 's,"\$RealBin/../doc","%{_localstatedir}/%{name}/doc",' bin/xxvd
sed -i '/HTMLDIR/s,"\$RealBin/../","%{_datadir}/%{name}/skins",' bin/xxvd
perl -pi -e 's,"\$RealBin/../share/,"%{_datadir}/%{name}/,' bin/xxvd
perl -pi -e 's,"\$RealBin/../contrib","%{_datadir}/%{name}/contrib",' bin/xxvd

cat > README.install.urpmi <<EOF
You must create the database "xxv" on your mysql server, create a
mysql user for xxv and enter the correct USR and PWD in the
[General] section of %{_localstatedir}/%{name}/xxvd.cfg.

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

%install
rm -rf %{buildroot}

install -d -m755 %{buildroot}%{_bindir}
install -m755 bin/xxvd %{buildroot}%{_bindir}

install -d -m755 %{buildroot}%{_sysconfdir}
install -d -m755 %{buildroot}%{_localstatedir}/%{name}
install -m644 etc/xxvd.cfg.example %{buildroot}%{_localstatedir}/%{name}/xxvd.cfg
ln -s %{_localstatedir}/%{name} %{buildroot}%{_sysconfdir}/%{name}

install -d -m755 %{buildroot}%{_var}/cache/%{name}

install -d -m755 %{buildroot}%{_datadir}/%{name}/contrib
install -m644 contrib/*.sql %{buildroot}%{_datadir}/%{name}/contrib
install -m755 contrib/update-xxv %{buildroot}%{_datadir}/%{name}/contrib

install -d -m755 %{buildroot}%{_localstatedir}/%{name}/doc
install -m644 doc/* %{buildroot}%{_localstatedir}/%{name}/doc

install -d -m755 %{buildroot}%{_sysconfdir}/logrotate.d
install -m644 %SOURCE4 %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -d -m755 %{buildroot}%{_datadir}/%{name}/skins
cp -a wml html %{buildroot}%{_datadir}/%{name}/skins
ln -s html %{buildroot}%{_datadir}/%{name}/skins/default

cp -a lib/Tools.pm lib/XXV lib/SOAP share/* %{buildroot}%{_datadir}/%{name}

for f in locale/*/; do
	install -d -m755 \
		%{buildroot}%{_datadir}/locale/$(basename $f)/LC_MESSAGES
	install -m644 $f/LC_MESSAGES/xxv.mo \
		%{buildroot}%{_datadir}/locale/$(basename $f)/LC_MESSAGES
done

install -d -m755 %{buildroot}%{_logdir}/%{name}

install -d -m755 %{buildroot}%{_sysconfdir}/sysconfig
install -m644 %SOURCE3 %{buildroot}%{_sysconfdir}/sysconfig/xxv

install -d -m755 %{buildroot}%{_initrddir}
install -m755 %SOURCE2 %{buildroot}%{_initrddir}/xxv

install -d -m755 %{buildroot}%{_logdir}/xxv

install -d -m755 %{buildroot}%{_mandir}/man1
install -m644 doc/*.1  %{buildroot}%{_mandir}/man1

%find_lang xxv

%clean
rm -rf %{buildroot}

%post
%_post_service %name

%preun
%_preun_service %name

%files -f xxv.lang
%defattr(-,root,root)
%doc doc/{CHANGELOG,HISTORY,LIESMICH,NEWS,README,TUTORIAL*} README.install.urpmi
%attr(-,vdr,vdr) %dir %{_localstatedir}/xxv
%attr(-,vdr,vdr) %dir %{_logdir}/xxv
%attr(0640,vdr,vdr) %config(noreplace) %{_localstatedir}/xxv/xxvd.cfg
%attr(-,vdr,vdr) %{_var}/cache/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/xxv
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,vdr,vdr) %dir %{_localstatedir}/xxv/doc
%attr(-,vdr,vdr) %{_localstatedir}/xxv/doc/*
%{_sysconfdir}/xxv
%{_initrddir}/xxv
%{_bindir}/xxvd
%{_datadir}/%{name}
%{_mandir}/man1/xxvd.1*
