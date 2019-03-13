""" Common functions used by both the webscripts and the cli tools """

import sys
import os
from re import search
from time import time
from OpenSSL import crypto
from Crypto.Hash import SHA256, MD5

# XXX
sys.path.append("/usr/share/amppki/")
from amppki.config import CSR_DIR, INDEX_FILE


def verify_common_name(name):
    """ Check that only valid characters are used in this hostname """

    if search("[^a-zA-Z0-9.-]+", name) is None:
        return True
    return False


def is_expired(item):
    if int(item["expires"][:-3]) < time():
        return True
    return False


def load_index(filename=INDEX_FILE):
    index = []
    for line in open(filename).readlines():
        parts = line.split("\t")
        # TODO update the status of expired certificates to 'E'?
        index.append({
            "status": parts[0],
            "expires": parts[1],
            "revoked": parts[2] if len(parts[2]) > 0 else "",
            "serial": parts[3],
            "subject": parts[5].strip(),
            # XXX extract hostname properly?
            "host": parts[5].strip().split("/")[1][3:]
        })
    return index


def load_pending_requests(host=None):
    result = []
    # open each file in the CSR directory - any CSR here has yet to be signed
    for item in os.listdir(CSR_DIR):
        try:
            # make sure it is a CSR
            filename = "%s/%s" % (CSR_DIR, item)
            csrstr = open(filename).read()
            csr = crypto.load_certificate_request(crypto.FILETYPE_PEM, csrstr)

            # ignore it if it doesn't match the host we are interested in
            if host is not None and host != csr.get_subject().commonName:
                continue

            result.append({
                "host": csr.get_subject().commonName,
                "filename": filename,
                "subject": csr.get_subject(),
                "bits": csr.get_pubkey().bits(),
                "md5": MD5.new(csrstr).hexdigest(),
                "sha256": SHA256.new(csrstr).hexdigest(),
            })
        except crypto.Error as e:
            #print e
            pass

    # sort alphabetically by hostname
    result.sort(key=lambda x: x["host"])
    return result
