logstash-rpms
=============

RPM Specs for Logstash

======================
Files to build grok/logstash RPMs for CentOS/Red Hat
Tries to follow the [Java packaging guidelines](https://fedoraproject.org/wiki/Packaging:Java) from Fedora.

* Jar: /usr/share/java/logstash.jar
* Config: /etc/logstash/
* Plugins: /usr/share/logstash/
* Script: /usr/bin/logstash
* logrotate
* init script
* Running as user logstash in group logstash

There are two scripts that can be executed in the scripts directory. One will fetch the source files needed (make sure versions are correct
in the script) and the other will execute the build.

* scripts/get_sources
* scripts/rpm

Acknowledgments
---------------

Inspiration for this came from various other projects:
* https://github.com/NumberFour/logstash-rpms
* https://github.com/mhorbul/logstash-rpm
* https://github.com/piojo/logstash-rpm
* https://github.com/lfrancke/logstash-rpm
