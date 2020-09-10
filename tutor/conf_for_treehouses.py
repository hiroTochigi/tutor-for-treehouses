import click
import subprocess
import re

from . import config as tutor_config
from . import env
from . import exceptions
from . import fmt
from .__about__ import __version__


# 7-bit C1 ANSI sequences
ansi_escape = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE)
escape_second = re.compile(r'OC')

process = subprocess.run(["sudo","treehouses", "tor"],
                          stdout=subprocess.PIPE
                        )
print(process.stdout[8:-10])
print(process.stdout.decode("utf-8"))
address = bytes(process.stdout.decode('unicode-escape'), 'ascii')
onionAddress = address[8:-10]
ONION_ADDRESS = onionAddress.decode('utf-8')
print(ONION_ADDRESS)

_ansi_re = re.compile(r"\033\[[;?0-9]*[a-zA-Z]")
ansi_one = re.compile(r"/\\b")
ansi_two = re.compile(r"\\n\\e\[\?12;25")

def update(root, interactive=True):
    """
    Load and save the configuration.
    """
    prelms = f"{ONION_ADDRESS}"
    cms = f"studio.{ONION_ADDRESS}"
    email = f"contact@{ONION_ADDRESS}"
    print(prelms)
    nextlms = ansi_escape.sub("", prelms)
    print(nextlms)
    belms = ansi_one.sub("", nextlms)
    print(belms)
    lms = ansi_two.sub("", belms)
    print(lms)

    config, defaults = tutor_config.load_all(root)
    config["LMS_HOST"] = lms
    config["CMS_HOST"] = "studio.uq4vski2iets4dhbvlcoojd57s3qyfanuejies3fouinubughjsw72qd.onion"
    config["PLATFORM_NAME"] = "OpenEdx"
    config["CONTACT_EMAIL"] = email
    config["LANGUAGE_CODE"] = "en"
    config["ACTIVATE_HTTPS"] = False
    tutor_config.save_config_file(root, config)
    tutor_config.merge(config, defaults)
    return config
