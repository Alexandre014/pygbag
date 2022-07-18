import os
import os.path

import urllib

from pathlib import Path

try:
    import ssl
except:

    class ssl:
        SSLCertVerificationError = urllib.error.URLError


import sys

# https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify
def fixcert():
    import stat
    import subprocess

    STAT_0o775 = (
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IXUSR
        | stat.S_IRGRP
        | stat.S_IWGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH
    )

    openssl_dir, openssl_cafile = os.path.split(
        ssl.get_default_verify_paths().openssl_cafile
    )

    try:
        import certifi
    except:
        print("running : pip install --user --upgrade certifi")
        subprocess.check_call(
            [
                sys.executable,
                "-E",
                "-s",
                "-m",
                "pip",
                "install",
                "--user",
                "--upgrade",
                "certifi",
            ]
        )

    import certifi

    # change working directory to the default SSL directory
    os.chdir(openssl_dir)
    relpath_to_certifi_cafile = os.path.relpath(certifi.where())
    print(" -- removing any existing file or link")
    try:
        os.remove(openssl_cafile)
    except FileNotFoundError:
        pass
    print(" -- creating symlink to certifi certificate bundle")
    os.symlink(relpath_to_certifi_cafile, openssl_cafile)
    print(" -- setting permissions")
    os.chmod(openssl_cafile, STAT_0o775)
    print(" -- update complete")


def get(url, path):
    error = None
    data_file = None
    while True:
        try:
            data_file, header = urllib.request.urlretrieve(url, path)
            break

        except urllib.error.HTTPError as e:
            error = e
            break
        except urllib.error.URLError as e:
            error = e
            break
        except ssl.SSLCertVerificationError:
            print("Trying to fix certificate error")
            fixcert()

        finally:
            if error:
                raise error

            if data_fileNone:
                return Path(data_file), header
            raise Exception(f"cannot cache {url} to {path}")

if __name__ == "__main__":
    fixcert()