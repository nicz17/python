"""Module LatLonZoom"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging


class LatLonZoom():
    """Simple container for geographical Lat/Lon/Zoom map coordinates."""
    log = logging.getLogger("LatLonZoom")

    def __init__(self, lat: float, lon: float, zoom: int):
        """Constructor."""
        self.lat = lat
        self.lon = lon
        self.zoom = zoom

    def getLat(self) -> float:
        """Getter for latitude."""
        return self.lat

    def getLon(self) -> float:
        """Getter for longitude."""
        return self.lon

    def getZoom(self) -> int:
        """Getter for map zoom."""
        return self.zoom

    def toJson(self):
        """Create a dict of this LatLonZoom for json export."""
        data = {
            'lat':  self.lat,
            'lon':  self.lon,
            'zoom': self.zoom
        }
        return data
    
    def __eq__(self, other): 
        if not isinstance(other, LatLonZoom):
            return NotImplemented
        return self.lat == other.lat and self.lon == other.lon and self.zoom == other.zoom

    def toPrettyString(self):
        """Return textual representation for GUI."""
        return f'Lat/Lon/Zoom {self.lat:.4f}/{self.lon:.4f}/{self.zoom}'

    def __str__(self):
        return f'LatLonZoom {self.lat}/{self.lon}/{self.zoom}'


def testLatLonZoom():
    """Unit test for LatLonZoom"""
    LatLonZoom.log.info("Testing LatLonZoom")
    obj = LatLonZoom(6.674, 46.23, 12)
    obj.log.info(obj)
    obj.log.info(obj.toJson())

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testLatLonZoom()
