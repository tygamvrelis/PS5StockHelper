# Application utilities
# Author: Tyler Gamvrelis

import os
import sys
import argparse
import logging

def get_script_path():
    """Gets the path where the script is running."""
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def str2bool(v):
    # https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def check_positive(value):
    # https://stackoverflow.com/questions/14117415/in-python-using-argparse-allow-only-positive-integers
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError('%s is an invalid positive int value' % value)
    return ivalue

def parse_args():
    """Parses command-line arguments."""
    os.chdir(get_script_path())    
    parser = argparse.ArgumentParser(description='PS5 stock helper')
    parser.add_argument('--period', help='How often to check for stock, in seconds. Positive integer', type=check_positive, default=5)
    parser.add_argument('--log', help='Set log level', default='info')
    parser.add_argument('--mute', help='Toggles audio notification', type=str2bool, default=False)
    return vars(parser.parse_args())
