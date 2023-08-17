import feature_extraction_server.app as app
import feature_extraction_server.settings as settings

if __name__ == '__main__':
    
    from decouple import config
    from argparse import ArgumentParser
    
    PORT = 5000
    HOST = 'localhost'
    
    ap = ArgumentParser()
    ap.add_argument('-p', '--port', type=int, help='Port to run the server on')
    ap.add_argument('-ho', '--host', type=str, help='Host to run the server on')
    
    settings.add_args(ap)
    args = ap.parse_args()
    settings.adopt_args(args)
    
    PORT = args.port or config('PORT', default=PORT, cast=int)
    HOST = args.host or config('HOST', default=HOST)
    
    from werkzeug.serving import run_simple
    run_simple(HOST, PORT, app.entrypoint())