"""Module Exporter"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import pynorpaHtml
from HtmlPage import *
import picture
import taxon
import DateTools

class Exporter():
    """Class Exporter"""
    log = logging.getLogger("Exporter")

    def __init__(self):
        """Constructor."""
        self.picCache = picture.PictureCache()
        self.taxCache = taxon.TaxonCache()

    def buildBasePages(self):
        """Build base html pages."""
        self.buildHome()
        self.buildLatest()
        self.buildLinks()
        self.buildLocations()
        self.buildAlpha()

    def buildHome(self):
        """Build Home page"""
        page = pynorpaHtml.PynorpaHtmlPage('Nature - Accueil')
        #page.addHeading(1, 'Photos de nature')
        tableLeftRight = TableHtmlTag(None, 2)
        page.add(tableLeftRight)
        tdLeft = tableLeftRight.getNextCell()
        tdLeft.addTag(HtmlTag('h1', 'Photos de nature'))

        # Sample pictures
        divBest = MyBoxWideHtmlTag('Quelques photos')
        aBestPics = self.picCache.getRandomBest()
        listBest = []
        for pic in aBestPics:
            listBest.append(ImageHtmlTag(f'thumbs/{pic.getFilename()}', pic.getTaxonName(), pic.getFilename()))
        divBest.addTag(TableHtmlTag(listBest).addAttr('class', 'table-thumbs'))
        tdLeft.addTag(divBest)

        # TODO Favorite taxa
        tdLeft.addTag(MyBoxWideHtmlTag('Quelques catégories'))

        # TODO About
        divAbout = MyBoxWideHtmlTag('A propos')
        tdLeft.addTag(divAbout)
        divAbout.addTag(HtmlTag('p', """Cette galerie de photos de nature me sert d'aide-mémoire 
                        pour retrouver les noms des plantes et insectes que je croise en 
                        montagne, en voyage ou autour de chez moi."""))
        divAbout.addTag(HtmlTag('p', """C'est aussi une collection de taxons qui compte actuellement 
                                4396 photos dans 1718 espèces, 1336 genres et 501 familles."""))

        # Newest species
        tdRight = tableLeftRight.getNextCell()
        divNewSpecies = MyBoxHtmlTag('Dernières espèces')
        listNewSpecies = divNewSpecies.addList()
        for (idx, tFirstObs) in self.taxCache.fetchNewestSpecies():
            taxon = self.taxCache.findById(idx)
            item = listNewSpecies.addItem()
            item.addTag(LinkHtmlTag(self.getTaxonLink(taxon), taxon.getNameFr(), False, taxon.getName()))
            item.addTag(GrayFontHtmlTag(DateTools.datetimeToPrettyStringFr(tFirstObs)))
        tdRight.addTag(divNewSpecies)

        # TODO Latest excursions
        tdRight.addTag(MyBoxHtmlTag('Excursions récentes'))

        # Photo hardware
        divHardware = MyBoxHtmlTag('Matériel photo')
        tdRight.addTag(divHardware)
        ulHardware = divHardware.addList()
        ulHardware.addItem().addTag(LinkHtmlTag("https://fr.wikipedia.org/wiki/Nikon_D300", "Nikon D300", True, "Wikipedia : Nikon D300"))
        li = ulHardware.addItem()
        li.addTag(LinkHtmlTag("https://fr.wikipedia.org/wiki/Nikon_D800", "Nikon D800", True, "Wikipedia : Nikon D800"))
        li.addTag(GrayFontHtmlTag("(depuis novembre 2017)"))
        ulHardware.addItem("AF-S Micro Nikkor 105mm 1:2.8")
        ulHardware.addItem("AF-S Nikkor 80-400mm 1:4.5-5.6")

        divLinks = MyBoxHtmlTag('Liens externes')
        tdRight.addTag(divLinks)
        aLinks = [
            LinkHtmlTag("https://www.inaturalist.org/observations/nicz", "iNaturalist", True,
		 		"Mes observations sur iNaturalist"),
            LinkHtmlTag("http://www.insecte.org/forum/", "Le monde des insectes", True,
		 		"Le monde des insectes - forum"),
            LinkHtmlTag("http://www.quelestcetanimal.com/", "Quel est cet animal ?", True,
		 		"Quel est cet animal ?"),
            LinkHtmlTag("https://www.infoflora.ch/fr/", "Infoflora", True, "Flore Suisse"),
            LinkHtmlTag("https://noc.social/@nicz", "Mastodon", True, "Mastodon @nicz@noc.social").addAttr("rel", "me")
        ]
        divLinks.addTag(ListHtmlTag(aLinks))

        page.save(f'{config.dirWebExport}index.html')

    def buildLinks(self):
        """Build Links page"""
        page = pynorpaHtml.PynorpaHtmlPage('Nature - Liens')
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
        self.addBiblioRef(biblio, "E. Sardet, C. Roesti, Y. Braud", "Orthoptères de France, Belgique, Luxembourg et Suisse", "Biotope", "2024")
        self.addBiblioRef(biblio, "V. Hugonnot, F. Pépin, J. Celle", "Mousses et hépatiques de France", "Biotope", "2022")
        self.addBiblioRef(biblio, "Collectif", "Les guides Salamandre", "Editions de la Salamandre, Neuchâtel", None)
        page.addList(biblio)

        page.save(f'{config.dirWebExport}liens.html')

    def buildLatest(self):
        """Build latest images page"""
        page = pynorpaHtml.PynorpaHtmlPage('Nature - Dernières photos')
        page.addHeading(1, 'Dernières photos')
        table = TableHtmlTag(None).addAttr('class', 'table-thumbs')
        aPics = self.picCache.getLatest(12)
        for pic in aPics:
            self.addThumbLink(pic, table.getNextCell())
        page.add(table)
        page.save(f'{config.dirWebExport}latest.html')

    def buildLocations(self):
        """Build Locations page"""
        page = pynorpaHtml.PynorpaHtmlPage('Nature - Lieux')
        page.addHeading(1, 'Lieux')
        page.addHeading(2, 'Cette page est en construction')
        page.save(f'{config.dirWebExport}locations.html')

    def buildAlpha(self):
        """Build names index page"""
        page = pynorpaHtml.PynorpaHtmlPage('Nature - Noms latins')
        page.addHeading(1, 'Noms latins')
        page.menu.addTag(HtmlTag('h2', 'Noms latins'))
        tableMenu = TableHtmlTag([], 4)
        tableMenu.addAttr('width', '120px')
        page.menu.addTag(tableMenu)

        letter = None
        ul = None
        species = self.taxCache.getForRank(taxon.TaxonRank.SPECIES)
        for tax in species:
            letterTax = tax.getName()[:1].upper()
            if letterTax != letter:
                letter = letterTax
                tableMenu.getNextCell().addTag(LinkHtmlTag(f'#{letter}', letter))
                anchor = HtmlTag('a').addAttr('name', letter)
                anchor.addTag(HtmlTag('h2', letter))
                page.add(anchor)
                ul = page.addList([])
            li = ul.addItem()
            li.addTag(LinkHtmlTag(self.getTaxonLink(tax), tax.getName()))
            family = tax.getAncestor(taxon.TaxonRank.FAMILY)
            if family:
                li.addTag(GrayFontHtmlTag(f'- {family.getName()}'))
        page.save(f'{config.dirWebExport}noms-latins.html')

        # French names
        page = pynorpaHtml.PynorpaHtmlPage('Nature - Noms communs')
        page.addHeading(1, 'Noms communs')
        page.menu.addTag(HtmlTag('h2', 'Noms communs'))
        tableMenu = TableHtmlTag([], 4)
        tableMenu.addAttr('width', '120px')
        page.menu.addTag(tableMenu)

        letter = None
        ul = None
        species = sorted(species, key=lambda tax: tax.nameFrNorm)
        for tax in species:
            if tax.getNameFr() != tax.getName():
                letterTax = tax.getNameFr()[:1].upper()
                if letterTax != letter:
                    letter = letterTax
                    tableMenu.getNextCell().addTag(LinkHtmlTag(f'#{letter}', letter))
                    anchor = HtmlTag('a').addAttr('name', letter)
                    anchor.addTag(HtmlTag('h2', letter))
                    page.add(anchor)
                    ul = page.addList([])
                li = ul.addItem()
                li.addTag(LinkHtmlTag(self.getTaxonLink(tax), tax.getNameFr()))
                family = tax.getAncestor(taxon.TaxonRank.FAMILY)
                if family:
                    li.addTag(GrayFontHtmlTag(f'- {family.getNameFr()}'))
        page.save(f'{config.dirWebExport}noms-verna.html')

    def buildTaxa(self):
        """Build taxon pages"""
        # TODO: implement
        pass

    def buildTest(self):
        """Build a simple test page."""
        page = pynorpaHtml.PynorpaHtmlPage('Test')
        page.addHeading(1, 'Test')
        page.addHeading(2, 'Bibliographie')
        page.save(f'{config.dirWebExport}test.html')
        self.buildLatest()

    def addThumbLink(self, pic: picture.Picture, parent: HtmlTag):
        """Add a preview and description of the specified picture."""
        sShotAt = DateTools.datetimeToPrettyStringFr(pic.getShotAt())
        link = LinkHtmlTag(f'pages/{pic.getFilename()}', None)
        link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', pic.getTaxonName(), pic.getTaxonName()))
        link.addTag(HtmlTag('i', f'<br>{pic.getTaxonName()}<br>'))
        parent.addTag(link)
        parent.addTag(LinkHtmlTag(f'lieu{pic.getIdxLocation()}.html', pic.getLocationName()))
        parent.addTag(GrayFontHtmlTag(f'<br>{sShotAt}'))

    def getTaxonLink(self, tax: taxon.Taxon) -> str:
        """Get the home-relative link to the specified taxon page."""
        match tax.getRank():
            case taxon.TaxonRank.SPECIES:
                return 'pages/' + tax.getName().replace(' ', '-').lower() + '.html'
        return 'not-implemented.html'

    def addBiblioRef(self, list, authors: str, title: str, editor: str, year: str):
        """Add a bibliographical reference."""
        nsyear = f', {year}' if year else '' 
        list.append(f'{authors} : <b>{title}</b>, {editor}{nsyear}')

    def __str__(self):
        return 'Exporter'


def testExporter():
    """Unit test for Exporter"""
    Exporter.log.info("Testing Exporter")
    exporter = Exporter()
    exporter.buildTest()
    exporter.buildBasePages()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testExporter()
