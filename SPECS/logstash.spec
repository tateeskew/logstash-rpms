%define debug_package %{nil}_bindir}
%define base_install_dir %{_javadir}{%name}

%global bindir %{_bindir}
%global confdir %{_sysconfdir}/%{name}
%global jarpath %{_javadir}
%global lockfile %{_localstatedir}/lock/subsys/%{name}
%global logdir %{_localstatedir}/log/%{name}
%global piddir %{_localstatedir}/run/%{name}
%global plugindir %{_datadir}/%{name}
%global sysconfigdir %{_sysconfdir}/sysconfig

Name:           logstash
Version:        1.1.9
Release:        1%{?dist}
Summary:        A tool for managing events and logs

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://logstash.net
Source0:        https://logstash.objects.dreamhost.com/release/%{name}-%{version}-monolithic.jar
Source1:        logstash.wrapper
Source2:        logstash.logrotate
Source3:        logstash.init
Source4:        logstash.sysconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       jre
Requires:       jpackage-utils

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

%description
A tool for managing events and logs.

%prep
%build

%install
rm -rf $RPM_BUILD_ROOT

# JAR file
%{__mkdir} -p %{buildroot}%{_javadir}
%{__install} -p -m 644 %{SOURCE0} %{buildroot}%{jarpath}/%{name}.jar

# Config
%{__mkdir} -p %{buildroot}%{confdir}

# Plugin dir
%{__mkdir} -p %{buildroot}%{plugindir}/inputs
%{__mkdir} -p %{buildroot}%{plugindir}/filters
%{__mkdir} -p %{buildroot}%{plugindir}/outputs

# Wrapper script
%{__mkdir} -p %{buildroot}%{_bindir}
%{__install} -m 755 %{SOURCE1} %{buildroot}%{bindir}/%{name}

%{__sed} -i \
   -e "s|@@@NAME@@@|%{name}|g" \
   -e "s|@@@JARPATH@@@|%{jarpath}|g" \
   %{buildroot}%{bindir}/%{name}

# Logs
%{__mkdir} -p %{buildroot}%{logdir}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Misc
%{__mkdir} -p %{buildroot}%{piddir}

# sysconfig and init
%{__mkdir} -p %{buildroot}%{_initddir}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 755 %{SOURCE3} %{buildroot}%{_initddir}/%{name}
%{__install} -m 644 %{SOURCE4} %{buildroot}%{sysconfigdir}/%{name}

# Using _datadir for PLUGINDIR because logstash expects a structure like logstash/{inputs,filters,outputs}
%{__sed} -i \
   -e "s|@@@NAME@@@|%{name}|g" \
   -e "s|@@@DAEMON@@@|%{bindir}|g" \
   -e "s|@@@CONFDIR@@@|%{confdir}|g" \
   -e "s|@@@LOCKFILE@@@|%{lockfile}|g" \
   -e "s|@@@LOGDIR@@@|%{logdir}|g" \
   -e "s|@@@PIDDIR@@@|%{piddir}|g" \
   -e "s|@@@PLUGINDIR@@@|%{_datadir}|g" \
   %{buildroot}%{_initddir}/%{name}

%{__sed} -i \
   -e "s|@@@NAME@@@|%{name}|g" \
   -e "s|@@@CONFDIR@@@|%{confdir}|g" \
   -e "s|@@@LOGDIR@@@|%{logdir}|g" \
   -e "s|@@@PLUGINDIR@@@|%{_datadir}|g" \
   %{buildroot}%{sysconfigdir}/%{name}

%pre
# create logstash group
if ! getent group logstash >/dev/null; then
        groupadd -r logstash
fi

# create logstash user
if ! getent passwd logstash >/dev/null; then
        useradd -r -g logstash -d %{_javadir}/%{name} \
            -s /sbin/nologin -c "You know, for search" logstash
fi

%post
/sbin/chkconfig --add logstash

%preun
if [ $1 -eq 0 ]; then
  /sbin/service logstash stop >/dev/null 2>&1
  /sbin/chkconfig --del logstash
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
# JAR file
%{_javadir}/%{name}.jar

# Config
%config(noreplace) %{confdir}/

# Plugin dir
%dir %{plugindir}/inputs
%dir %{plugindir}/filters
%dir %{plugindir}/outputs

# Wrapper script
%{bindir}/*


# Logrotate
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

# Sysconfig and init
%{_initddir}/%{name}
%config(noreplace) %{sysconfigdir}/*

%defattr(-,%{name},%{name},-)
%dir %{logdir}/
%dir %{piddir}/

%changelog
* Tue Jan 22 2013 dmaher@mozilla.com 1.1.9-1
- Add chkconfig block to init
- Update logstash version to 1.1.9
* Tue Jan 11 2013 lars.francke@gmail.com 1.1.5-1
- Initial version
