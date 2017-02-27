# duoauthproxy-rpm

- RPM spec for Duo authentication proxy (https://duo.com/docs/authproxy_reference)
- modified for releases that are relevant to me
- Assuming a build environment is available to you, this should compile with the PAN version listed


# Notes

- changed install dir from /opt/ to /usr/lib/
  -  remember this when referencing duo guides because they will all have /opt/
- need "duoauthproxy" user to to run rather than root


#  Acknowledgements

- original spec: https://github.com/jthiltges/duoauthproxy-rpm. Thanks!
- DUO Security (https://duo.com/) for providing a file that can be packaged.
