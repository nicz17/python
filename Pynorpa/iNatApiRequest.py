"""
Module for sending requests to the iNat API.

Request examples:
Find the iNat taxon id for a taxon name.
Find the ancestor taxa for a taxon id.
"""

import logging
import requests


class INatTaxon():
    """Small container for iNat taxon info."""
    log = logging.getLogger('iNatTaxon')

    def __init__(self, id: int, name: str, rank: str, commonName: str):
        self.id = id
        self.name = name
        self.rank = rank
        self.commonName = commonName

    def __str__(self):
        return f'INatTaxon {self.id} {self.rank} {self.name} ({self.commonName})'

class INatApiRequest():
    """Class to send taxon info requests to the iNaturalist API."""
    log = logging.getLogger('iNatApiRequest')

    # Query examples:
    #url = f"https://api.inaturalist.org/v1/observations?user_id={me_id}&quality_grade=needs_id&rank=genus"
    #url = "https://api.inaturalist.org/v1/taxa?q=Polyommatus%20bellargus&only_id=true"

    def __init__(self):
        self.baseUrl = 'https://api.inaturalist.org/v1/taxa'

    def getIdFromName(self, name: str) -> int:
        """Get iNat taxon id from taxon name."""
        data = self.sendRequestByName(name)
        id = self.findId(data, name)
        self.log.info(f'Found id {id} for {name}')
        return id
    
    def getTaxonFromName(self, name: str) -> INatTaxon:
        """Get iNat taxon from taxon name."""
        data = self.sendRequestByName(name)
        self.log.info('Total results: %d', data['total_results'])
        for result in data['results']:
            if result['name'] == name:
                if result['rank'] == 'section':
                    self.log.info(f'Skipping SECTION {name}')
                    continue
                commonName = result['preferred_common_name'] if 'preferred_common_name' in result else None
                taxon = INatTaxon(result['id'], result['name'], result['rank'], commonName)
                return taxon
        return None
    
    def getAncestors(self, id: int) -> list[INatTaxon]:
        """Get list of ancestor taxa from taxon id."""
        if id:
            data = self.sendRequestById(id)
            return self.readAncestors(data)    
        else:
            self.log.error('Invalid taxon id')
            return None

    def sendRequestByName(self, name: str):
        """Request taxon data from taxon name."""
        # https://api.inaturalist.org/v1/taxa?q=Polyommatus%20bellargus
        url = f'{self.baseUrl}?q={name}'
        self.log.info('Sending request for name %s to %s', name, url)
        response = requests.get(url)
        data = response.json()
        #self.log.info(data)
        #self.readResponse(data)
        return data

    def sendRequestById(self, id: int):
        """Request taxon data from taxon id."""
        # https://api.inaturalist.org/v1/taxa/231137
        url = f'{self.baseUrl}/{id}'
        self.log.info('Sending request for id %s to %s', id, url)
        response = requests.get(url)
        data = response.json()
        #self.log.info(data)
        return data

    def findId(self, data, name: str):
        """Extract id corresponding to name from data."""
        self.log.info('Total results: %d', data['total_results'])
        for result in data['results']:
            if result['name'] == name:
                self.log.info('Name: %s rank: %s, id: %d', result['name'], result['rank'], result['id'])
                return result['id']

    def readResponse(self, data):
        """Dump results."""
        self.log.info('Total results: %d', data['total_results'])
        for result in data['results']:
            self.log.info('Name: %s rank: %s, id: %d', result['name'], result['rank'], result['id'])

    def readAncestors(self, data):
        """Extract selected ancestor taxa from data."""
        taxa = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']
        ancestors = []
        self.log.info('Total results: %d', data['total_results'])
        for result in data['results']:
            self.log.info('Name: %s rank: %s, id: %d', result['name'], result['rank'], result['id'])
            for taxon in result['ancestors']:
                if taxon['rank'] in taxa:
                    #self.log.info('  Name: %s rank: %s, id: %d', taxon['name'], taxon['rank'], taxon['id'])
                    commonName = taxon['preferred_common_name'] if 'preferred_common_name' in taxon else None
                    ancestor = INatTaxon(taxon['id'], taxon['name'], taxon['rank'], commonName)
                    ancestors.append(ancestor)
        return ancestors

def testRequest():
    req = INatApiRequest()
    name = 'Polyommatus bellargus'
    name = 'Harpocera thoracica'
    name = 'Blastit notfound'
    name = 'Solorina saccata'
    taxon = req.getTaxonFromName(name)
    req.log.info(f'Found {taxon} for name {name}')
    # id = req.getIdFromName(name)
    # if id:
    #     ancestors = req.getAncestors(id)
    #     if ancestors:
    #         for ancestor in ancestors:
    #             req.log.info(ancestor)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testRequest()