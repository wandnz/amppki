# amppki

amppki is a way to help manage certificates used by measurement clients
as part of the [AMP active measurement system](http://amp.wand.net.nz).
It allows signing certificates of new clients and creating RabbitMQ
accounts for them as they come online and connect to the collector for
the first time. It is also optional - you can manage certificates and
accounts however you like (e.g. create your own and deploy with
ansible/puppet/etc).

The other components of the AMP system are:
- [amplet2](https://github.com/wanduow/amplet2) - Client that performs tests and reports measurements.
- [ampy](https://github.com/wanduow/ampy) - Interface between the display front-end and the data storage back-end
- [ampweb](https://github.com/wanduow/amp-web) - Front-end web interface.
- [nntsc](https://github.com/wanduow/nntsc) - Data storage back-end.

For more information please email contact@wand.net.nz.


## Installing amppki

You should install amppki on the AMP collector server so that it can update
RabbitMQ as certificates are signed. If you haven't already, add the official
AMP repositories and install the amppki package:

    $ wget -O- https://bintray.com/user/downloadSubjectPublicKey?username=wand | sudo apt-key add -
    $ echo "deb https://dl.bintray.com/wand/amp `lsb_release -c -s` main" | sudo tee /etc/apt/sources.list.d/bintray.amplet2.list
    $ sudo apt-get install apt-transport-https
    $ sudo apt-get update
    $ sudo apt-get install amppki


## Running amppki

AMP clients will try to connect to amppki on TCP port 7655, present a
certificate signing request, and wait for the certificate to be signed.
Use `/usr/sbin/ampca` to list, sign or deny the requests.

To list the currently outstanding certificate signing requests:

    sudo ampca list

To sign a request and create the related RabbitMQ user:

    sudo ampca sign <identifier>

To deny a signing request:

    sudo ampca deny <identifier>

See the man page for further details of the commands available.

----

This code has been developed by the
[University of Waikato](http://www.waikato.ac.nz)
[WAND network research group](http://www.wand.net.nz).
It is licensed under the GNU General Public License (GPL) version 2. Please
see the included file COPYING for details of this license.

Copyright (c) 2015-2019 The University of Waikato, Hamilton, New Zealand.
All rights reserved.
