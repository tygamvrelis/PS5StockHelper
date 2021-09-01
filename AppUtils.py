# Application utilities
# Author: Tyler Gamvrelis

# Standard library imports
import argparse
import logging
import os
import sys


def get_script_path():
    """Gets the path where the script is running."""
    return os.path.dirname(os.path.realpath(sys.argv[0]))


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
    parser.add_argument('--period', help='How often to check for stock, in seconds. Positive integer',
                        type=check_positive, default=5)
    parser.add_argument('--log', help='Set log level', default='info')
    parser.add_argument('--mute', help='Disables audio notification', dest='mute', action='store_true', default=False)
    parser.add_argument('--test', help='Enables test mode', dest='test', action='store_true', default=False)
    parser.add_argument('--email', help='Enables email notifications', dest='email', action='store_true', default=False)
    return vars(parser.parse_args())


def get_logs_dir():
    app_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
    )
    logs_dir = os.path.join(app_path, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def setup_logger(log_level, fname):
    """
    Sets up the logger.
    Sources:
        - https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module
        - https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file
    Args:
        log_level : str
            String indicating the log level
        fname : str
            Name of application file setting up the logger
    """
    fname_base = os.path.basename(fname)
    fname_base = os.path.splitext(fname_base)[0]
    logs_dir = get_logs_dir()
    log_name = os.path.join(logs_dir, fname_base + '.log')
    if log_level is not None:
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        logging.basicConfig(
            filename=log_name,
            filemode='w',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=numeric_level
        )
        if numeric_level >= logging.DEBUG:
            # As long as logging is not disabled, always output INFO to stdout
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            root = logging.getLogger()
            root.addHandler(handler)
