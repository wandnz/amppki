from pyramid.config import Configurator

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
