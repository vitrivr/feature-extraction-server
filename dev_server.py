import sys
sys.path.append('./feature_extraction_server-core/') 
import os

for dir in os.listdir('./plugins/'):
    sys.path.append(f'./plugins/{dir}/')



from feature_extraction_server.services.fast_api_app import run_app



import logging

if __name__ == '__main__':
    run_app()