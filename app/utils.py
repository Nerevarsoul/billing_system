from optparse import OptionParser


def parse_args():
    parser = OptionParser()
    parser.add_option('--port', dest='port', type='int',
                      help='PORT FOR HTTP CONNECTION',
                      default=8000,
                      metavar='PORT FOR HTTP CONNECTION')
    parser.add_option('--host', dest='host',
                      help='HOST NAME',
                      default='localhost',
                      metavar='HOST NAME')
    (options, args) = parser.parse_args()

    if not options.port:
        parser.error('PORT is mandatory for running app')

    return options
