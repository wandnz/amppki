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

from pyramid.config import Configurator
from pyramid.asset import abspath_from_asset_spec
from pyramid.response import Response

def main(global_config, **settings):
    """ Main entry point for web scripts """

    config = Configurator(settings=settings)
    config.include("pyramid_chameleon")

    _robots = open(abspath_from_asset_spec('amppki:static/robots.txt')).read()
    _robots_response = Response(content_type='text/plain', body=_robots)
    config.add_view(lambda x: _robots_response, name='robots.txt')

    config.add_route("sign", "sign")
    config.add_route("cert", "cert/{ampname}/{signature}")

    config.add_route("default", "/*args")

    config.scan()
    return config.make_wsgi_app()
