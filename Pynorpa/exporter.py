"""Module Exporter"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import pynorpaHtml
from HtmlPage import *

class Exporter():
    """Class Exporter"""
    log = logging.getLogger("Exporter")

    def __init__(self):
        """Constructor."""
        self.cache = None

    def buildBasePages(self):
        """Build base html pages."""
        self.buildHome()
        self.buildLinks()
        self.buildLocations()

    def buildHome(self):
        """Build Home page"""
        page = pynorpaHtml.PynorpaHtmlPage('Accueil')
        page.addHeading(1, 'Photos de nature')
        page.addHeading(2, 'Cette page est en construction')
        page.add(MyBoxHtmlTag('Quelques photos'))
        page.add(MyBoxHtmlTag('Quelques catégories'))
        page.save('export/index.html')

    def buildLinks(self):
        """Build Links page"""
        page = pynorpaHtml.PynorpaHtmlPage('Liens')
        page.addHeading(1, 'Liens')
		
        page.addHeading(2, "Insectes")
        links = []
        links.append(LinkHtmlTag("http://www.insecte.org/forum/", "Le monde des insectes - forum", True))
        links.append(LinkHtmlTag("http://www.galerie-insecte.org/galerie/fichier.php", 
                "Le monde des insectes - galerie", True))
        links.append(LinkHtmlTag("http://www.galerie-insecte.org/galerie/auteur.php?aut=6169", 
                "Le monde des insectes - mes photos", True))
        links.append(LinkHtmlTag("http://www.quelestcetanimal.com/", "Quel est cet animal ?", True))
        links.append(LinkHtmlTag("http://lepus.unine.ch/carto/", "InfoFauna UniNe", True))
        links.append(LinkHtmlTag("http://www.lepido.ch/", "Papillons diurnes de Suisse", True))
        links.append(LinkHtmlTag("http://cle.fourmis.free.fr/castes-fourmis.html", "Fourmis de France", True))
        links.append(LinkHtmlTag("http://home.hccnet.nl/mp.van.veen/conopidae/ConGenera.html", "Clé des Conopidae", True))
        page.addList(links)

        page.addHeading(2, "Plantes")
        links = []
        links.append(LinkHtmlTag("http://www.visoflora.com/", "Visoflora", True))
        links.append(LinkHtmlTag("https://www.infoflora.ch/fr/", "Infoflora - flore de Suisse", True))
        links.append(LinkHtmlTag("http://www.tela-botanica.org/bdtfx-nn-60585-synthese", "Tela botanica", True))
        page.addList(links)

        page.addHeading(2, "Autres")
        links = []
        links.append(LinkHtmlTag("http://www.inaturalist.org/observations/nicz", "iNaturalist", True))
        links.append(LinkHtmlTag("http://www.salamandre.net/", "La Salamandre - la revue des curieux de nature", True))
        links.append(LinkHtmlTag("http://www.pronatura-vd.ch/nos_reserves", "Réserves Pro Natura Vaud", True))
        links.append(LinkHtmlTag("http://www.arocha.ch/fr/projects/aide-entretien-pps/", "A Rocha - entretien de prairies sèches", True))
        links.append(LinkHtmlTag("http://www.ornitho.ch/index.php?m_id=1", "Plate-forme ornithologique suisse", True))
        links.append(LinkHtmlTag("https://www.thunderforest.com/", "Cartes par Thunderforest et OpenLayers", True))
        page.addList(links)

        page.addHeading(1, 'Bibliographie')
        biblio = []
        self.addBiblioRef(biblio, "P. Leraut, P. Blanchot", "Le guide entomologique", "Delachaux et Niestlé", "2012")
        self.addBiblioRef(biblio, "R. Dajoz", "Dictionnaire d'entomologie", "Lavoisier", "2010")
        self.addBiblioRef(biblio, "D. Martiré", "Guide des plus beaux coléoptères", "Belin", "2017")
        self.addBiblioRef(biblio, "K. Dijkstra", "Guide des libellules", "Delachaux et Niestlé", "2015")
        self.addBiblioRef(biblio, "T. Haahtela <i>et al</i>", "Guide photo des papillons d'Europe", "Delachaux et Niestlé", "2017")
        self.addBiblioRef(biblio, "R. Garrouste", "Hémiptères de France", "Delachaux et Niestlé", "2015")
        self.addBiblioRef(biblio, "A. Canard, C. Rollard", "A la découverte des araignées", "Dunod", "2015")
        self.addBiblioRef(biblio, "K. Lauber, G. Wagner, A. Gygax", "Flora Helvetica", "4e édition, Haupt", "2012")
        self.addBiblioRef(biblio, "E. Gerber, G. Kozlowski, A.-S. Mariéthoz", "La flore des Préalpes", "Rossolis", "2010")
        self.addBiblioRef(biblio, "F. Dupont, J.-L. Guignard", "Botanique, les familles de plantes", "15e édition, Elsevier Masson", "2012")
        self.addBiblioRef(biblio, "Collectif", "Les guides Salamandre", "Editions de la Salamandre, Neuchâtel", None)
        self.addBiblioRef(biblio, "E. Sardet, C. Roesti, Y. Braud", "Orthoptères de France, Belgique, Luxembourg et Suisse", "Biotope", "2024")
        self.addBiblioRef(biblio, "V. Hugonnot, F. Pépin, J. Celle", "Mousses et hépatiques de France", "Biotope", "2022")
        page.addList(biblio)

        page.save('export/links.html')

    def buildLocations(self):
        """BuildLocations"""
        page = pynorpaHtml.PynorpaHtmlPage('Lieux')
        page.addHeading(1, 'Lieux')
        page.addHeading(2, 'Cette page est en construction')
        page.save('export/locations.html')

    def buildTaxa(self):
        """BuildTaxa"""
        # TODO: implement
        pass

    def buildTest(self):
        """Build a simple test page."""
        page = pynorpaHtml.PynorpaHtmlPage('Test')
        page.addHeading(1, 'Test')
        page.addHeading(2, 'Bibliographie')
        page.save('export/test.html')

    def addBiblioRef(self, list, authors: str, title: str, editor: str, year: str):
        """Add a bibliographical reference."""
        nsyear = f', {year}' if year else '' 
        list.append(f'{authors} : <b>{title}</b>, {editor}{nsyear}')

    def __str__(self):
        return 'Exporter'


def testExporter():
    """Unit test for Exporter"""
    Exporter.log.info("Testing Exporter")
    obj = Exporter()
    obj.buildTest()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testExporter()
