Name:           duoauthproxy
Version:        2.4.20
Release:        1%{?dist}
Summary:        Duo Authentication Proxy

Group:          System Environment/Daemons
License:        Commercial
URL:            https://www.duosecurity.com/docs/ldap
Source0:        https://dl.duosecurity.com/duoauthproxy-%{version}-src.tgz
Source1:        duoauthproxy.service

%define svc_user duoauthproxy
%define install_dir /usr/lib/%{name}
%global debug_package %{nil}

BuildRequires: python-devel
BuildRequires: openssl-devel
BuildRequires: perl

# Needed by the init script
Requires: initscripts
Requires: chkconfig

# required so that build files don't become requirements
AutoReqProv: no

%description
Proxies RADIUS or LDAP authentication attempts and adds Duo authentication

%prep
%setup -q -n %{name}-%{version}-src

# Sample config
# cp -p %{SOURCE1} conf

# Set username in authproxyctl
perl -p -i -e "s/^USER_DEFAULT = None$/USER_DEFAULT = '%{svc_user}'/g" pkgs/duoauthproxy/scripts/authproxyctl

%build
make

%install
rm -rf %{buildroot}

# The included installer doesn't work with buildroots, so we install manually
#duoauthproxy-build/install

########################################################
# Extract the RHEL init script from the python installer
mv duoauthproxy-build/install install.py

cat > get_init.py << EOF
import install
params = {'service_user': '%{svc_user}',
          'install_dir':  '%{install_dir}' }

print install.INITSCRIPT_REDHAT_TMPL % params
EOF
python get_init.py > init
install -D init %{buildroot}/%{_initddir}/%{name}

########################################################
# Install the application
mkdir -p %{buildroot}/%{install_dir}
cp -a duoauthproxy-build/* %{buildroot}/%{install_dir}

mkdir -p %{buildroot}/%{_initddir}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/duoauthproxy.service


%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then # Final removal
    /sbin/service %{name} stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}
fi

%files
%defattr(-,root,root,-)
%{install_dir}/bin
%config %{install_dir}/conf/ca-bundle.crt
%config(noreplace) %attr(640,%{svc_user},%{svc_user}) %{install_dir}/conf/authproxy.cfg
%{install_dir}/doc
%{install_dir}/include
%{install_dir}/lib
%{install_dir}/lib64
%attr(750,%{svc_user},%{svc_user}) %{install_dir}/log
%attr(750,%{svc_user},%{svc_user}) %{install_dir}/run
%{_initddir}/%{name}
%{_unitdir}/duoauthproxy.service

%changelog
* Mon Mar 20 2017 @anotherbhav
- added Source1 as a systemd startup file
* Mon Feb 27 2017 @anotherBhav <> 2.4.20
- removed patch0 and patch1 installs - they don't work with 2.4.20
- added additional required packages for compilation
- added "AutoReqProv: no" - it kept adding build files as requirements
- added username: duoauthproxy
- changed install dir to: /usr/lib
* Fri Oct 16 2015 John Thiltges <> 2.4.12-1
- Initial package
