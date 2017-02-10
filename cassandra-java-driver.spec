Name:		cassandra-java-driver
Version:	3.1.3
Release:	2%{?dist}
Summary:	DataStax Java Driver for Apache Cassandra
License:	ASL 2.0
URL:		https://github.com/datastax/java-driver
Source0:	https://github.com/datastax/java-driver/archive/%{version}.tar.gz

# added --allow-script-in-comments option to javadoc plugin
# https://bugzilla.redhat.com/show_bug.cgi?id=1417677
Patch0:		%{name}-%{version}-allow-script-in-comments.patch

BuildRequires:	maven-local
%if %{?fedora} <= 23
BuildRequires:	mvn(com.codahale.metrics:metrics-core)
%else
BuildRequires:	mvn(io.dropwizard.metrics:metrics-core)
%endif
BuildRequires:	mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:	mvn(com.google.guava:guava)
BuildRequires:	mvn(io.netty:netty-handler)
BuildRequires:	mvn(io.netty:netty-tcnative)
BuildRequires:	mvn(io.netty:netty-transport-native-epoll)
BuildRequires:	mvn(javax.json:javax.json-api)
BuildRequires:	mvn(joda-time:joda-time)
BuildRequires:	mvn(log4j:log4j:1.2.17)
BuildRequires:	mvn(net.jpountz.lz4:lz4)
BuildRequires:	mvn(org.apache.commons:commons-exec)
BuildRequires:	mvn(org.assertj:assertj-core)
BuildRequires:	mvn(org.glassfish:javax.json)
BuildRequires:	mvn(org.hdrhistogram:HdrHistogram)
BuildRequires:	mvn(org.mockito:mockito-all)
BuildRequires:	mvn(org.ow2.asm:asm-all)
BuildRequires:	mvn(org.slf4j:slf4j-log4j12)
BuildRequires:	mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:	mvn(org.testng:testng)
BuildRequires:	mvn(org.xerial.snappy:snappy-java)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(com.github.jnr:jnr-ffi)
BuildRequires:	mvn(com.github.jnr:jnr-posix)
BuildRequires:	mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-failsafe-plugin)
BuildRequires:	mvn(org.apache.felix:org.apache.felix.framework)
# driver-tests stress module dependencies
#BuildRequires:	mvn(net.sf.jopt-simple:jopt-simple)
#BuildRequires:	mvn(com.yammer.metrics:metrics-core) missing
BuildArch:	noarch

%description
A driver for Apache Cassandra 1.2+ that works exclusively with the
Cassandra Query Language version 3 (CQL3) and Cassandra's binary protocol.

%package extras
Summary:	DataStax Java Driver for Apache Cassandra - Extras
Requires:	%{name} = %{version}-%{release}

%description extras
Extended functionality for the Java driver.

%package mapping
Summary:	DataStax Java Driver for Apache Cassandra - Object Mapping
Requires:	%{name} = %{version}-%{release}

%description mapping
Object mapper for the DataStax CQL Java Driver.

%package parent
Summary:	DataStax Java Driver for Apache Cassandra - Parent POM

%description parent
Parent POM for the DataStax Java Driver.

%package tests
Summary:	DataStax Java Driver for Apache Cassandra - Tests
Requires:	%{name} = %{version}-%{release}

%description tests
Tests for the DataStax Java Driver.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -qn java-driver-%{version}

# allow-script-in-comments.patch
%patch0 -p1

# Unneeded features
%pom_disable_module driver-dist
%pom_disable_module driver-examples
# missing dependency for stress tests
%pom_disable_module stress driver-tests
# Unavailable plugins
%pom_remove_plugin -r :animal-sniffer-maven-plugin:
%pom_remove_plugin -r :clirr-maven-plugin
%pom_remove_plugin -r :license-maven-plugin
# kr.motd.maven:os-maven-plugin:1.4.1.Final
%pom_xpath_remove -r "pom:build/pom:extensions"
# Unwanted tasks
%pom_remove_plugin -r :maven-source-plugin
%pom_remove_plugin -r :maven-release-plugin
%pom_remove_plugin :gmaven-plugin driver-mapping
%pom_xpath_remove "pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions/pom:execution/pom:goals"
# Disable shaded copy of netty artifacts
%pom_remove_plugin -r :maven-shade-plugin driver-core

%if %{?fedora} <= 23
%pom_change_dep io.dropwizard.metrics: com.codahale.metrics:  driver-core
%endif

# remove hidden files from documentation
rm manual/statements/.nav
rm manual/object_mapper/.nav

%mvn_package ":cassandra-driver-tests-parent" tests
%mvn_package ":cassandra-driver-tests-osgi" tests

%build

# Unavailable test dep org.cassandra:java-client:0.11.0 
%mvn_build -fs

%install
%mvn_install

%files -f .mfiles-cassandra-driver-core
%doc README.md changelog faq manual upgrade_guide
%license LICENSE

%files extras -f .mfiles-cassandra-driver-extras
%files mapping -f .mfiles-cassandra-driver-mapping
%files parent -f .mfiles-cassandra-driver-parent
%license LICENSE

%files tests -f .mfiles-tests

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Tomas Repik <trepik@redhat.com> - 3.1.3-1
- version update

* Tue Jun 21 2016 Tomas Repik <trepik@redhat.com> - 3.0.0-2
- Added maven-bundle-plugin as a dependency

* Thu Apr 07 2016 Tomas Repik <trepik@redhat.com> - 3.0.0-1
- Initial RPM release

