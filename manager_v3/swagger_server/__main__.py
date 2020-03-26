#!/usr/bin/env python3

import connexion

from swagger_server import encoder
import atexit



#defining function to run on shutdown
@atexit.register
def close_running_threads():
    print("Threads complete, ready to finish")
#Register the function to be called on exit
        

#atexit.register(close_running_threads)

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'MONITORING MANAGER'})
    app.debug = True
    app.run(port=8888)


if __name__ == '__main__':
    main()
