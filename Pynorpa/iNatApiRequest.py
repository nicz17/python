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

    def __init__(self):
        self.baseUrl = 'https://api.inaturalist.org/v1/taxa'

    def sendRequestByName(self, name: str):
        #url = f"https://api.inaturalist.org/v1/observations?user_id={me_id}&quality_grade=needs_id&rank=genus"
        #url = "https://api.inaturalist.org/v1/taxa?q=Polyommatus%20bellargus"
        url = f'{self.baseUrl}?q={name}'

        # Fetch data from iNaturalist
        response = requests.get(url)
        data = response.json()
        self.log.info(data)
        self.readResponse(data)

    def sendRequestById(self, id: int):
        url = f'{self.baseUrl}/{id}'
        self.log.info('Sending request %s', url)

        # Fetch data from iNaturalist
        response = requests.get(url)
        data = response.json()
        self.readAncestors(data)

    def readResponse(self, data):
        self.log.info('Total results: %d', data['total_results'])
        for result in data['results']:
            self.log.info('Name: %s rank: %s, id: %d', result['name'], result['rank'], result['id'])

    def readAncestors(self, data):
        self.log.info('Total results: %d', data['total_results'])
        for result in data['results']:
            self.log.info('Name: %s rank: %s, id: %d', result['name'], result['rank'], result['id'])
            for taxon in result['ancestors']:
                self.log.info('  Name: %s rank: %s, id: %d', taxon['name'], taxon['rank'], taxon['id'])

def testRequest():
    req = INatApiRequest()
    #req.sendRequestByName('Polyommatus bellargus')
    req.sendRequestById(154576)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testRequest()