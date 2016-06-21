Name:          cassandra-java-driver
Version:       3.0.0
Release:       2%{?dist}
Summary:       DataStax Java Driver for Apache Cassandra
License:       ASL 2.0
URL:           https://github.com/datastax/java-driver
Source0:       https://github.com/datastax/java-driver/archive/%{version}.tar.gz

BuildRequires: maven-local
%if %{?fedora} <= 23
BuildRequires: mvn(com.codahale.metrics:metrics-core)
%else
BuildRequires: mvn(io.dropwizard.metrics:metrics-core)
%endif
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(io.netty:netty-handler)
BuildRequires: mvn(io.netty:netty-tcnative)
BuildRequires: mvn(io.netty:netty-transport-native-epoll)
BuildRequires: mvn(javax.json:javax.json-api)
BuildRequires: mvn(joda-time:joda-time)
BuildRequires: mvn(log4j:log4j:1.2.17)
BuildRequires: mvn(net.jpountz.lz4:lz4)
BuildRequires: mvn(org.apache.commons:commons-exec)
BuildRequires: mvn(org.assertj:assertj-core)
BuildRequires: mvn(org.glassfish:javax.json)
BuildRequires: mvn(org.hdrhistogram:HdrHistogram)
BuildRequires: mvn(org.mockito:mockito-all)
BuildRequires: mvn(org.ow2.asm:asm-all)
BuildRequires: mvn(org.slf4j:slf4j-log4j12)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires: mvn(org.testng:testng)
BuildRequires: mvn(org.xerial.snappy:snappy-java)
# fedora 25
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)

BuildArch:     noarch

%description
A driver for Apache Cassandra 1.2+ that works exclusively with the
Cassandra Query Language version 3 (CQL3) and Cassandra's binary protocol.

%package extras
Summary:       DataStax Java Driver for Apache Cassandra - Extras

%description extras
Extended functionality for the Java driver.

%package mapping
Summary:       DataStax Java Driver for Apache Cassandra - Object Mapping

%description mapping
Object mapper for the DataStax CQL Java Driver.

%package parent
Summary:       DataStax Java Driver for Apache Cassandra - Parent POM

%description parent
Parent POM for the DataStax Java Driver.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -qn java-driver-%{version}

# Unneeded features
%pom_disable_module driver-dist
%pom_disable_module driver-examples
# Unavailable plugins
%pom_remove_plugin -r :animal-sniffer-maven-plugin:
%pom_remove_plugin -r :clirr-maven-plugin
%pom_remove_plugin -r :license-maven-plugin
# kr.motd.maven:os-maven-plugin:1.4.1.Final
%pom_xpath_remove -r "pom:build/pom:extensions"
# Unwanted tasks
%pom_remove_plugin -r :maven-source-plugin
%pom_remove_plugin -r :maven-release-plugin
%pom_xpath_remove "pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions/pom:execution/pom:goals"
# Disable shaded copy of netty artifacts
%pom_remove_plugin -r :maven-shade-plugin driver-core

%if %{?fedora} <= 23
%pom_change_dep io.dropwizard.metrics: com.codahale.metrics:  driver-core
%endif

# remove hidden files from documentation
rm manual/statements/.nav
rm manual/object_mapper/.nav

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

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Tue Jun 21 2016 Tomas Repik <trepik@redhat.com> - 3.0.0-2
- Added maven-bundle-plugin as a dependency

* Thu Apr 07 2016 Tomas Repik <trepik@redhat.com> - 3.0.0-1
- Initial RPM release

