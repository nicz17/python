"""
 Copy JPG images from Nikon D800 camera.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import glob
import os
import config
import logging
import DateTools
from PhotoInfo import *
from Timer import *


class CopyFromCamera:
    """Copy JPG images from Nikon D800 camera."""
    log = logging.getLogger('CopyFromCamera')

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.images = []  # Photos found on camera card
        self.copied = []  # Images copied to disk
        self.sourceDir = None
        self.targetDir = None
        self.statusMsg = 'Init'

    def loadImages(self):
        """Load the list of images to copy."""

        # Find source and target directories
        self.getCurrentTarget()
        self.getCameraDir()
        if not self.isCameraMounted():
            self.log.error('Camera is not mounted, aborting!')
            return
        else:
            self.log.info('Camera is mounted at %s', self.sourceDir)
        self.createNatureDirs(self.targetDir)

        # Glob images
        self.images = sorted(glob.glob(self.sourceDir + '*.JPG'))
        self.log.info('Found %d images', len(self.images))
        self.statusMsg = f'Chargé {len(self.images)} photos de {self.sourceDir}'

    def copyImages(self, cbkProgress = None):
        """Copy JPG images from the mounted camera."""
        if len(self.images) == 0:
            return
        timer = Timer()
        self.log.info('Copying images from %s to %s', self.sourceDir, self.targetDir)
        for img in self.images:
            photo = PhotoInfo(img)
            photo.identify()
            self.log.info('Copying %s', photo)
            self.statusMsg = f'Copie de {photo.filename}'
            destDir = f'{self.targetDir}orig/'
            destFile = destDir + os.path.basename(img)
            if os.path.exists(destFile):
                self.log.info('Photo %s already copied, skipping', )
            else:
                cmd = 'cp ' + img.replace(" ", "\\ ") + ' ' + destDir
                self.log.debug(cmd)
                os.system(cmd)
                self.copied.append(destFile)
            if cbkProgress:
                cbkProgress()
        timer.stop()
        self.log.info('Copied %d photos in %s', len(self.copied), timer.getElapsed())
        self.statusMsg = f'Copié {len(self.copied)} photos vers {self.targetDir} en {timer.getElapsed()}'

    def createThumbs(self, cbkProgress = None):
        """Create thumbnail images if needed."""
        dirThumbs = f'{self.targetDir}thumbs/'

        if not os.path.exists(dirThumbs):
            os.makedirs(dirThumbs)

        copied = sorted(glob.glob(self.targetDir + 'orig/*.JPG'))
        for sImg in copied:
            sThumb = dirThumbs + os.path.basename(sImg)
            self.statusMsg = f'Creating thumbnail {sThumb}'
            if not os.path.exists(sThumb):
                self.log.info('Creating thumbnail image %s', sThumb)
                sCmd = f'convert {sImg} -resize 500x500 {sThumb}'
                os.system(sCmd)
                if cbkProgress:
                    cbkProgress()
        self.statusMsg = f'Created {len(self.images)} thumbnails'

    def isCameraMounted(self):
        """Check if the camera is mounted."""
        if self.sourceDir is None:
            self.log.error('Camera dir is undefined!')
            return False
        return os.path.exists(self.sourceDir)
    
    def getNumberImages(self):
        """Get the number of photos to copy."""
        return len(self.images)
    
    def getCopiedImages(self):
        """Get the list of images copied on disk."""
        return self.copied

    def getCameraDir(self) -> str:
        """Get the current photo dir on the mounted camera."""
        dirBase = config.dirCameraBase
        if not os.path.exists(dirBase):
            self.log.error('Camera is not mounted at %s.', dirBase)
            return
        for nDir in range(106, 120):
            dirCamera = f'{dirBase}{nDir}ND800/'
            if os.path.exists(dirCamera):
                self.sourceDir = dirCamera
                self.log.info('Camera is mounted at %s', self.sourceDir)
                break
        if self.sourceDir is None:
            self.log.error('Camera is not mounted: no folder found in %s', dirBase)
        return self.sourceDir

    def getCurrentTarget(self) -> None:
        """Build current target image directory. Name is based on year and month."""
        yearMonth = DateTools.nowAsString('%Y-%m')
        self.targetDir = f'{config.dirPhotosBase}Nature-{yearMonth}/'
        self.log.debug('Photo destination dir is %s', self.targetDir)
    
    def createNatureDirs(self, dir):
        """Create photo directories if needed."""
        if not os.path.exists(dir):
            self.log.info('Creating dir %s', dir)
            os.makedirs(dir)
            os.makedirs(dir + 'orig')
            os.makedirs(dir + 'photos')
            os.makedirs(dir + 'thumbs')
            os.makedirs(dir + 'geotracker')
        else:
            self.log.info('Directory %s already exists', dir)

    def getStatusMessage(self):
        """Return a message about the current status."""
        return self.statusMsg
    
class CopyFromDropBox():
    """Copy JPG images from DropBox Panorpa directory."""
    log = logging.getLogger('CopyFromDropBox')

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.images = []  # Photos found on DropBox
        self.copied = []  # Images copied to disk
        self.sourceDir = config.dirDropBox
        self.statusMsg = 'Initialisation'

    def loadImages(self):
        """Load the list of images to copy."""
        self.images = sorted(glob.glob(self.sourceDir + '*.jpg'))
        self.log.info('Found %d images', len(self.images))
        self.statusMsg = f'Chargé {len(self.images)} images de {self.sourceDir}'

    def copyImages(self, cbkProgress = None):
        """Copy JPG images from the DropBox dir."""
        if len(self.images) == 0:
            return
        timer = Timer()
        for file in self.images:
            name = os.path.basename(file)
            if len(name) == 19:
                targetDir = f'{config.dirPhotosBase}Nature-{name[0:4]}-{name[4:6]}/orig/'
                targetFile = f"{targetDir}{name.replace('.jpg', '.JPG')}"
                if os.path.exists(targetFile):
                    self.log.info('Already copied %s', name)
                else:
                    self.log.info('Copying %s to %s', name, targetFile)
                    cmd = f'cp {file} {targetFile}'
                    self.log.debug(cmd)
                    os.system(cmd)
                    self.copied.append(targetFile)
                    thumb = targetFile.replace('orig/', 'thumbs/')
                    cmd = f'convert {targetFile} -resize 500x500 {thumb}'
                    os.system(cmd)
                if cbkProgress:
                    cbkProgress()
            else:
                self.log.error('Unhandled file name %s: wrong length', name)
        timer.stop()
        self.log.info('Copied %d photos in %s', len(self.copied), timer.getElapsed())
        self.statusMsg = f'Copié {len(self.copied)} photos en {timer.getElapsed()}'
    
    def getNumberImages(self):
        """Get the number of photos to copy."""
        return len(self.images)

    def getStatusMessage(self):
        """Return a message about the current status."""
        return self.statusMsg


def testCopyFromCamera():
    copier = CopyFromCamera()
    copier.getCameraDir()
    copier.getCurrentTarget()
    if copier.isCameraMounted():
        copier.loadImages()
        for img in copier.images:
            photo = PhotoInfo(img)
            #photo.identify()

def testCopyFromDropBox():
    copier = CopyFromDropBox()
    copier.loadImages()
    for img in copier.images:
        photo = PhotoInfo(img)
        photo.identify()
        copier.log.info(photo)
    copier.copyImages()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testCopyFromCamera()
    testCopyFromDropBox()