import click
import subprocess

from . import config as tutor_config
from . import env
from . import exceptions
from . import fmt
from .__about__ import __version__

process = subprocess.run(["sudo","treehouses", "tor"],
                          stdout=subprocess.PIPE
                        )
ONION_ADDRESS = process.stdout.decode('ascii')[0:-1]

def update(root, interactive=True):
    """
    Load and save the configuration.
    """
    config, defaults = tutor_config.load_all(root)
    config["LMS_HOST"] = ONION_ADDRESS
    config["CMS_HOST"] = "studio." + ONION_ADDRESS
    config["PLATFORM_NAME"] = "OpenEdx"
    config["CONTACT_EMAIL"] = "contact@" + ONION_ADDRESS
    config["LANGUAGE_CODE"] = "en"
    config["ACTIVATE_HTTPS"] = False
    tutor_config.save_config_file(root, config)
    tutor_config.merge(config, defaults)
    return config
