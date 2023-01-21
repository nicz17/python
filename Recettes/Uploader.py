"""
Upload generated recipe HTML files and photos
to www.tf79.ch using FTP.
"""

import logging
import config

class Uploader:
    """Upload files to website using FTP."""
    log = logging.getLogger('Uploader')

    def __init__(self) -> None:
        pass

    def upload(self):
        self.log.info('Uploading to FTP server')

