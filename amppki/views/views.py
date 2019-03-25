# This file is part of amppki.
#
# Copyright (C) 2015-2019 The University of Waikato, Hamilton, New Zealand.
#
# Authors: Brendon Jones
#
# All rights reserved.
#
# This code has been developed by the WAND Network Research Group at the
# University of Waikato. For further information please see
# http://www.wand.net.nz/
#
# amppki is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# amppki is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with amppki; if not, write to the Free Software Foundation, Inc.
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Please report any bugs, questions or comments to contact@wand.net.nz
#

""" Routes used to accept requests and distribute signed certificates """

from base64 import urlsafe_b64decode
from os import listdir
from os.path import isfile, basename
import re
from ssl import PEM_cert_to_DER_cert

from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import DerSequence
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from OpenSSL import crypto
from amppki.config import CERT_DIR, CSR_DIR
from amppki.common import verify_common_name
from pyramid.view import view_config
from pyramid.httpexceptions import *
from pyramid.response import Response

@view_config(route_name="default", renderer="string")
def default(request):
    """ Debug function for dumping information about unknown requests """
    print "unknown request,", request.method, request.url
    print request.matchdict
    return


# XXX merge this with /cert and do different things on POST vs GET?
@view_config(route_name="sign", renderer="string")
def sign(request):
    """ Accept a certificate signing request """

    # TODO can we make sure this is done over SSL? don't accept this otherwise
    print "accepting cert signing request"

    if len(request.body) <= 0:
        print "no csr in message"
        return Response(status_code=400)

    # this is already url decoded for us, so use it as is
    csrstr = request.body

    try:
        # make sure this is a valid request before we do anything with it
        csr = crypto.load_certificate_request(crypto.FILETYPE_PEM, csrstr)
        if verify_common_name(csr.get_subject().commonName) is False:
            print "invalid characters in common name"
            return Response(status_code=400)
    except crypto.Error as e:
        print "invalid csr: %s" % e
        return Response(status_code=400)

    # We use the sha256 hash as the unique filename for this request. Using
    # something like hostname/commonname can easily lead to collisions
    shahash = SHA256.new(csrstr).hexdigest()

    if not isfile(shahash):
        # if there isn't one we've prepared earlier, check if we can auto-sign
        # this one right now (maybe it matches a known host config).
        # otherwise we add it to the queue and wait for a human to check it and
        # decide if it should be signed or not
        try:
            open("%s/%s" % (CSR_DIR, shahash), "w").write(csrstr)
        except IOError:
            # XXX is this giving away any useful information?
            print "error saving csr"
            return Response(status_code=500)

    return Response(status_code=202)


@view_config(route_name="cert", renderer="string")
def cert(request):
    """ Provide a certificate (if available) for the specified host """

    # TODO can we make sure this is done over SSL? don't accept this otherwise
    # check that the named cert exists
    print request.matchdict

    # XXX how much validation of the ampname do we need? Coming through the
    # pyramid route it already can't contain slashes, which basename (perhaps
    # redundantly) confirms. Also, to get sent a file, the file will have to
    # look like a certificate containing the public key that will verify the
    # signature.
    ampname = basename(request.matchdict["ampname"])
    try:
        signature = urlsafe_b64decode(str(request.matchdict["signature"]))
    except TypeError as e:
        # in this case we'll give the user a slightly more useful response
        # code - they messed up their signature, nothing of ours is exposed
        print "failed to base64 decode, invalid data"
        return Response(status_code=400)

    print "got request for cert", ampname

    # check that the certificate exists on disk
    try:
        # TODO can we accidentally expose other files by doing it this way?
        # TODO don't serve expired or revoked certificates

        # try to limit the files we get with a regex, though there are still
        # plenty of ways names can break this.
        pattern = re.compile("%s.[0-9A-F]{2,6}.pem" % ampname)
        matches = [x for x in listdir(CERT_DIR) if re.match(pattern, x)]

        if len(matches) > 1:
            # TODO do we just want to check the newest one?
            # look at the matching certificate with the latest serial number
            #print "WARNING: Multiple certificate matches for %s" % ampname
            matches = sorted(matches,
                    key=lambda match: int(match.split(".")[-2], 16))
        if len(matches) > 0:
            certstr = open("%s/%s" % (CERT_DIR, matches[-1])).read()
        else:
            return Response(status_code=403)
    except (IOError, IndexError) as e:
        # the user doesn't need to know what went wrong, just tell them that
        # they can't get whatever cert they asked for
        print "failed to open certificate:", e
        #return HTTPForbidden()
        return Response(status_code=403)

    # Crypto.RSA.importKey() doesn't like X509 certificates, so we have to
    # extract the public key from the certificate before we can use it
    # http://stackoverflow.com/questions/12911373/
    der = PEM_cert_to_DER_cert(certstr)
    certificate = DerSequence()
    certificate.decode(der)
    tbsCertificate = DerSequence()
    tbsCertificate.decode(certificate[0])

    try:
        # the TBSCertificate is a sequence and the 7th element is the
        # subjectPublicKeyInfo, so we should be able to jump straight to it
        # https://tools.ietf.org/html/rfc5280#section-4.1
        key = RSA.importKey(tbsCertificate[6])
    except (ValueError, IndexError, TypeError) as e:
        print "importing key failed:", e
        #return HTTPForbidden()
        return Response(status_code=403)

    if key is None:
        print "key is none"
        #return HTTPForbidden()
        return Response(status_code=403)

    #print key.exportKey()

    # verify the signature using the public key in the cert
    # https://www.dlitz.net/software/pycrypto/api/2.6/Crypto.PublicKey.RSA._RSAobj-class.html#verify
    shahash = SHA256.new(ampname)
    #print shahash.hexdigest()
    verifier = PKCS1_v1_5.new(key)
    if not verifier.verify(shahash, signature):
        print "verification failed"
        #return HTTPForbidden()
        return Response(status_code=403)

    # return the signed cert
    print "all ok"
    return certstr
