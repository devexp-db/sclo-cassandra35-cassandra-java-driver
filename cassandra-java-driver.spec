%{?scl:%scl_package cassandra-java-driver}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}cassandra-java-driver
Version:	3.1.4
Release:	2%{?dist}
Summary:	DataStax Java Driver for Apache Cassandra
License:	ASL 2.0
URL:		https://github.com/datastax/java-driver
Source0:	https://github.com/datastax/java-driver/archive/%{version}.tar.gz

# added --allow-script-in-comments option to javadoc plugin
# https://bugzilla.redhat.com/show_bug.cgi?id=1417677
Patch0:		%{pkg_name}-%{version}-allow-script-in-comments.patch

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix}metrics
BuildRequires:	%{?scl_prefix}jackson-databind
BuildRequires:	%{?scl_prefix}guava
BuildRequires:	%{?scl_prefix}netty
BuildRequires:	%{?scl_prefix}jsonp
BuildRequires:	%{?scl_prefix_maven}joda-time
BuildRequires:	%{?scl_prefix}log4j
BuildRequires:	%{?scl_prefix}lz4-java
BuildRequires:	%{?scl_prefix_maven}apache-commons-exec
BuildRequires:	%{?scl_prefix}assertj-core
BuildRequires:	%{?scl_prefix}HdrHistogram
BuildRequires:	%{?scl_prefix_maven}mockito
BuildRequires:	%{?scl_prefix_java_common}objectweb-asm%{?scl:5}
BuildRequires:	%{?scl_prefix}slf4j-log4j12
BuildRequires:	%{?scl_prefix_maven}sonatype-oss-parent
BuildRequires:	%{?scl_prefix_maven}testng
BuildRequires:	%{?scl_prefix}snappy-java
BuildRequires:	%{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:	%{?scl_prefix}jnr-ffi
BuildRequires:	%{?scl_prefix}jnr-posix
BuildRequires:	%{?scl_prefix_maven}maven-plugin-build-helper
BuildRequires:	%{?scl_prefix_maven}maven-failsafe-plugin
BuildRequires:	%{?scl_prefix_java_common}felix-framework
BuildRequires:	%{?scl_prefix}snakeyaml
# transitive dependencies
%{?scl:
BuildRequires:	%{?scl_prefix}jffi
BuildRequires:	%{?scl_prefix}jffi-native
BuildRequires:	%{?scl_prefix}jnr-x86asm
BuildRequires:	%{?scl_prefix}jnr-constants
BuildRequires:	%{?scl_prefix_java_common}javassist
BuildRequires:	%{?scl_prefix}jctools
BuildRequires:	%{?scl_prefix}disruptor
BuildRequires:	%{?scl_prefix}jackson-core
BuildRequires:	%{?scl_prefix}jackson-annotations
BuildRequires:	%{?scl_prefix}jackson-dataformat-yaml
BuildRequires:	%{?scl_prefix}jackson-dataformat-xml
BuildRequires:	%{?scl_prefix}jackson-module-jaxb-annotations
BuildRequires:	%{?scl_prefix_java_common}jansi
BuildRequires:	%{?scl_prefix}jeromq
BuildRequires:	%{?scl_prefix}apache-commons-csv
}
# driver-tests stress module dependencies
#BuildRequires:	mvn(net.sf.jopt-simple:jopt-simple)
#BuildRequires:	mvn(com.yammer.metrics:metrics-core) missing
%{?scl:Requires: %scl_runtime}
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
%{!?scl:%patch0 -p1}

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
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

%mvn_package ":cassandra-driver-tests-parent" tests
%mvn_package ":cassandra-driver-tests-osgi" tests
%{?scl:EOF}

# remove hidden files from documentation
rm manual/statements/.nav
rm manual/object_mapper/.nav

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# Unavailable test dep org.cassandra:java-client:0.11.0 
%mvn_build -fs
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

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
* Mon Apr 10 2017 Tomas Repik <trepik@redhat.com> - 3.1.4-2
- scl conversion

* Fri Apr 07 2017 Tomas Repik <trepik@redhat.com> - 3.1.4-1
- version update

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Tomas Repik <trepik@redhat.com> - 3.1.3-1
- version update

* Tue Jun 21 2016 Tomas Repik <trepik@redhat.com> - 3.0.0-2
- Added maven-bundle-plugin as a dependency

* Thu Apr 07 2016 Tomas Repik <trepik@redhat.com> - 3.0.0-1
- Initial RPM release

