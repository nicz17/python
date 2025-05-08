"""
Module for sending requests to the iNat API.

Request examples:
https://api.inaturalist.org/v1/taxa?q=Stenodema%20laevigata
https://api.inaturalist.org/v1/taxa/146793
"""

import logging
import requests


class INatApiRequest():
    log = logging.getLogger('iNatApiRequest')

    # Query examples:
    #url = f"https://api.inaturalist.org/v1/observations?user_id={me_id}&quality_grade=needs_id&rank=genus"
    #url = "https://api.inaturalist.org/v1/taxa?q=Polyommatus%20bellargus"
    #url = "https://api.inaturalist.org/v1/taxa?q=Polyommatus%20bellargus&only_id=true"

    def __init__(self):
        self.baseUrl = 'https://api.inaturalist.org/v1/taxa'

    def getIdFromName(self, name: str) -> int:
        data = self.sendRequestByName(name)
        id = self.findId(data, name)
        self.log.info(f'Found id {id} for {name}')
        return id

    def sendRequestByName(self, name: str):
        url = f'{self.baseUrl}?q={name}'
        self.log.info('Sending request for name %s to %s', name, url)
        response = requests.get(url)
        data = response.json()
        #self.log.info(data)
        #self.readResponse(data)
        return data

    def sendRequestById(self, id: int):
        url = f'{self.baseUrl}/{id}'
        self.log.info('Sending request for id %s to %s', id, url)
        response = requests.get(url)
        data = response.json()
        self.readAncestors(data)

    def findId(self, data, name: str):
        self.log.info('Total results: %d', data['total_results'])
        for result in data['results']:
            if result['name'] == name:
                self.log.info('Name: %s rank: %s, id: %d', result['name'], result['rank'], result['id'])
                return result['id']

    def readResponse(self, data):
        self.log.info('Total results: %d', data['total_results'])
        for result in data['results']:
            self.log.info('Name: %s rank: %s, id: %d', result['name'], result['rank'], result['id'])

    def readAncestors(self, data):
        taxa = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']
        self.log.info('Total results: %d', data['total_results'])
        for result in data['results']:
            self.log.info('Name: %s rank: %s, id: %d', result['name'], result['rank'], result['id'])
            for taxon in result['ancestors']:
                if taxon['rank'] in taxa:
                    # TODO return a list of INatTaxon ancestors
                    self.log.info('  Name: %s rank: %s, id: %d', taxon['name'], taxon['rank'], taxon['id'])

def testRequest():
    req = INatApiRequest()
    name = 'Polyommatus bellargus'
    name = 'Harpocera thoracica'
    name = 'Blastit notfound'
    name = 'Colocasia coryli'
    id = req.getIdFromName(name)
    if id:
        req.sendRequestById(id)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testRequest()