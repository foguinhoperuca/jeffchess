"""
Util module to concetrate all reusable code.

This modules support all other classes/modules with usefull source code that doesn't belong to any other entity.
"""

import configparser
from datetime import datetime
import logging
from pathlib import Path

from termcolor import colored


class Util:
    """Helper class used to provide configuration, defaults and so on."""
    config = configparser.ConfigParser()
    LOG_FORMAT_FULL = colored('[%(asctime)s][%(process)d:%(processName)s]', 'green', attrs=['bold', 'dark']) + colored('[%(filename)s#%(funcName)s:%(lineno)d]', 'white', attrs=['bold', 'dark']) + colored('[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s'
    LOG_FORMAT_DEBUG = colored('[%(filename)s#%(funcName)s:%(lineno)d]', 'white', attrs=['bold', 'dark']) + colored('[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s'
    LOG_FORMAT_SIMPLE = colored('[%(levelname)s]', 'magenta', attrs=['bold', 'dark']) + ' %(message)s'

    # FIXME Why I need instantiate Util class?!?! Make all methods statics wouldn't be enough?!?
    def __init__(self):
        """Grab all configuration in setup.cfg"""
        setup_cfg_path = [
            "/etc/jeffchess/setup.cfg",
            "/usr/local/etc/jeffchess/setup.cfg",
            "/usr/etc/jeffchess/setup.cfg",
            str(Path.home().joinpath(".jeffchess", "setup.cfg"))
        ]

        file_found = False
        for f in setup_cfg_path:
            sf = Path(f)
            if sf.is_file():
                self.config.read(f)
                file_found = True
                # FIXME why can't work with logging.debug ?!?!
                # logging.debug(colored("file found was..: {p}".format(p = f), 'grey', attrs=['reverse', 'bold', 'underline']))
                break
        if not file_found:
            raise Exception("Couldn't find in setup.cfg file in any common path! Please, install it anywhere in {a}".format(a = setup_cfg_path))

        self.DEFAULT_PLAYER = self.config['app_init']['default_player']

    # TODO implement it!
    @staticmethod
    def get_app_file(filename = None):
        default_install_dir = "jeffchess"
        file_found = False

        if filename is None:
            raise ValueError("Couldn't find {f} file in any path!".format(f = filename))

        setup_path = [
            Path("/etc").joinpath(default_install_dir, filename),
            Path("/usr/local/etc").joinpath(default_install_dir, filename),
            Path("/usr/etc").joinpath(default_install_dir, filename),
            Path.home().joinpath(".jeffchess", filename)
        ]

        for f in setup_path:
            if f.is_file():
                logging.debug(colored("file found was..: {p}".format(p = f), 'grey', attrs=['reverse', 'bold', 'underline']))
                return f
        if not file_found:
            raise Exception("Couldn't find {f} file in any common path!".format(f=filename))

    def show_methods(obj):
        """Helper to discovery API of an object."""
        logging.basicConfig(level=logging.DEBUG, format=Util.LOG_FORMAT_DEBUG)
        logging.debug(colored("_______________________________________________________", 'cyan'))
        logging.debug(colored("type(obj)..: {t}".format(t=type(obj)), 'cyan'))
        logging.debug(colored("vars(obj)..: {v}".format(v=vars(obj)), 'cyan'))
        logging.debug(colored("dir(obj)...: {d}".format(d=dir(obj)), 'cyan'))
        for method in [method_name for method_name in dir(obj) if callable(getattr(obj, method_name))]:
            print(method)
        help(obj)
        logging.debug(colored("_______________________________________________________", 'cyan'))

    def info(msg):
        """This function standardize the message and simplified the use to standard output."""
        return colored(msg, 'blue')

    def warning(msg):
        """This function standardize the message and simplified the use to standard output."""
        return colored(msg, 'yellow', attrs=['bold'])

    def error(msg):
        """This function standardize the message and simplified the use to standard output."""
        return colored(msg, 'red', attrs=['bold', 'underline'])

    def debug(msg):
        """This function standardize the message and simplified the use to standard output."""
        return colored(msg, 'white', attrs=['reverse', 'bold', 'underline'])

    def white_piece(value):
        return colored(value, 'white', attrs=['reverse', 'bold', 'underline'])

    def black_piece(value):
        # return colored(value, 'blue', attrs=['reverse', 'bold', 'underline'])
        return value

    def emphasys(value):
        return colored(value, 'yellow', attrs=['reverse', 'bold', 'underline'])

    def player_named_by(value):
        return colored(value, 'red', attrs=['reverse', 'bold', 'underline'])

    @staticmethod
    def init_logger(log_type='normal', use_file_handler=False):
        if log_type == 'quiet':
            level = logging.WARN
            logformat = Util.LOG_FORMAT_SIMPLE
        elif log_type == 'normal':
            level = logging.INFO
            logformat = Util.LOG_FORMAT_INFO
        else:
            level = logging.DEBUG
            logformat = Util.LOG_FORMAT_FULL

        bot_logger = logging.getLogger(Util.DEFAULT_LOGGER_NAME)
        bot_logger.setLevel(level)

        c_handler = logging.StreamHandler()
        c_handler.setFormatter(logging.Formatter(logformat))
        c_handler.setLevel(level)
        bot_logger.addHandler(c_handler)

        if use_file_handler:
            f_handler = logging.FileHandler(f'tmp/logs/jeffchess_{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.log')
            f_handler.setFormatter(logging.Formatter(Util.LOG_FORMAT_FULL))
            f_handler.setLevel(logging.DEBUG)
            bot_logger.addHandler(f_handler)

        return bot_logger
