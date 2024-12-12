"""Module Exporter"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import re
import pynorpaHtml
from HtmlPage import *
import picture
from taxon import Taxon, TaxonRank, TaxonCache
from expedition import Expedition, ExpeditionCache
import DateTools
import TextTools
import Timer
from taxonUrlProvider import TaxonUrlProvider

class Exporter():
    """Class Exporter"""
    log = logging.getLogger("Exporter")

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')

        # Configure TaxonUrlProviders
        self.taxonUrlProviders = [
            TaxonUrlProvider('Wikipédia [fr]', 'https://fr.wikipedia.org/wiki/', 'Wikipédia en français'),
            TaxonUrlProvider('Wikipedia [en]', 'https://en.wikipedia.org/wiki/', 'Wikipedia in English'),
            TaxonUrlProvider('Wikispecies', 'https://species.wikimedia.org/wiki/', 'Wikispecies'),
            TaxonUrlProvider('iNaturalist', 'https://www.inaturalist.org/search?q=', 'inaturalist.org'),
            TaxonUrlProvider('Galerie insecte', 'https://galerie-insecte.org/galerie/', 'Galerie insecte', 
                TaxonRank.CLASS, ["Arachnida", "Chilopoda", "Crustacea", "Diplopoda", "Entognatha", "Insecta"], 
                TaxonUrlProvider.formatGalerieInsecte),
            TaxonUrlProvider('AntWiki', 'http://www.antwiki.org/wiki/', 'antwiki.org',
                TaxonRank.FAMILY, ['Formicidae'], TaxonUrlProvider.formatAntWiki),
            TaxonUrlProvider('Arages', 'https://wiki.arages.de/index.php?title=', 'arages.de',
                TaxonRank.CLASS, ["Arachnida"], TaxonUrlProvider.formatAntWiki),
            TaxonUrlProvider('Oiseaux de Suisse', 'https://www.vogelwarte.ch/fr/oiseaux/les-oiseaux-de-suisse/',
                'Vogelwarte', TaxonRank.CLASS, ['Aves'], TaxonUrlProvider.formatVogelwarte),
            TaxonUrlProvider('InfoFlora', 'https://www.infoflora.ch/fr/flore/', 'InfoFlora',
                TaxonRank.PHYLUM, ["Lycopodiophyta", "Pteridophyta", "Pinophyta", "Magnoliophyta"],
                TaxonUrlProvider.formatInfoFlora),
            TaxonUrlProvider('MycoDB', 'https://www.mycodb.fr/fiche.php?genre=', 'MycoDB', TaxonRank.PHYLUM,
                ["Ascomycota", "Basidiomycota"]),
            TaxonUrlProvider('Swiss bryophytes', 'https://www.swissbryophytes.ch/index.php/fr/', 'swissbryophytes.ch',
                TaxonRank.PHYLUM, ['Bryophyta'], TaxonUrlProvider.formatEmpty)
        ]

    def getTaxonUrlProviders(self) -> list[TaxonUrlProvider]:
        return self.taxonUrlProviders

    def buildBasePages(self):
        """Build base html pages."""
        timer = Timer.Timer()
        self.picCache = picture.PictureCache()
        self.taxCache = TaxonCache()
        self.excCache = ExpeditionCache()
        
        self.buildHome()
        self.buildLatest()
        self.buildLinks()
        self.buildLocations()
        self.buildExcursions()
        self.buildAlpha()
        self.buildTaxa()
        self.log.info('Exported in %s', timer.getElapsed())

    def buildHome(self):
        """Build Home page"""
        page = pynorpaHtml.PynorpaHtmlPage('Nature - Accueil')
        tableLeftRight = TableHtmlTag(None, 2)
        page.add(tableLeftRight)
        tdLeft = tableLeftRight.getNextCell()
        tdLeft.addTag(HtmlTag('h1', 'Photos de nature'))

        # Sample pictures
        divBest = MyBoxWideHtmlTag('Quelques photos')
        tableBestPics = TableHtmlTag([]).addAttr('class', 'table-thumbs')
        aBestPics = self.picCache.getRandomBest()
        for pic in aBestPics:
            td = tableBestPics.getNextCell()
            link = LinkHtmlTag(self.getTaxonLink(pic.taxon), None, False, pic.getTaxonName())
            link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', pic.getTaxonName(), pic.getFilename()))
            td.addTag(link)
        divBest.addTag(tableBestPics)
        tdLeft.addTag(divBest)

        # Favorite taxa
        divCategories = MyBoxWideHtmlTag('Quelques catégories')
        tdLeft.addTag(divCategories)
        tableCat = TableHtmlTag([], 5).addAttr("width", "100%")
        divCategories.addTag(tableCat)

        ul = ListHtmlTag([])
        tableCat.getNextCell().addTag(ul)
        ul.addItem(LinkHtmlTag("Pteridophyta.html", "Fougères", False, "Fougères"))
        ul.addItem(LinkHtmlTag("Pinophyta.html", "Conifères", False, "Conifères"))
        ul.addItem(LinkHtmlTag("Magnoliophyta.html#Liliopsida", "Monocots", False, "Monocotylédones"))
        ul.addItem(LinkHtmlTag("Magnoliophyta.html#Magnoliopsida", "Dicots", False, "Dicotylédones"))
		
        ul = ListHtmlTag([])
        tableCat.getNextCell().addTag(ul)
        ul.addItem(LinkHtmlTag("Malpighiales.html#Euphorbiaceae", "Euphorbes", False, "Euphorbes"))
        ul.addItem(LinkHtmlTag("Saxifragales.html#Saxifragaceae", "Saxifrages", False, "Saxifrages"))
        ul.addItem(LinkHtmlTag("Lamiales.html#Lamiaceae", "Lamiacées", False, "Lamiacées"))
        ul.addItem(LinkHtmlTag("Asterales.html#Asteraceae", "Astéracées", False, "Astéracées"))

        ul = ListHtmlTag([])
        tableCat.getNextCell().addTag(ul)
        ul.addItem(LinkHtmlTag("Chordata.html#Aves", "Oiseaux", False, "Oiseaux"))
        ul.addItem(LinkHtmlTag("Chordata.html#Mammalia", "Mammifères", False, "Mammifères"))
        ul.addItem(LinkHtmlTag("Araneae.html", "Araignées", False, "Araignées"))
        ul.addItem(LinkHtmlTag("Opiliones.html", "Opilions", False, "Opilions ou faucheux"))

        ul = ListHtmlTag([])
        tableCat.getNextCell().addTag(ul)
        ul.addItem(LinkHtmlTag("Arthropoda.html#Insecta", "Insectes", False, "Insectes"))
        ul.addItem(LinkHtmlTag("Diptera.html", "Diptères", False, "Mouches, syrphes, tipules"))
        ul.addItem(LinkHtmlTag("Hymenoptera.html", "Hyménoptères", False, "Abeilles, fourmis, guêpes"))
        ul.addItem(LinkHtmlTag("Lepidoptera.html", "Papillons", False, "Papillons"))

        ul = ListHtmlTag([])
        tableCat.getNextCell().addTag(ul)
        ul.addItem(LinkHtmlTag("Odonata.html", "Libellules", False, "Libellules et demoiselles"))
        ul.addItem(LinkHtmlTag("Coleoptera.html", "Coléoptères", False, "Coléoptères"))
        ul.addItem(LinkHtmlTag("Hemiptera.html", "Punaises", False, "Punaises"))
        ul.addItem(LinkHtmlTag("Squamata.html", "Reptiles", False, "Reptiles"))

        # About
        divAbout = MyBoxWideHtmlTag('A propos')
        tdLeft.addTag(divAbout)
        divAbout.addTag(HtmlTag('p', """Cette galerie de photos de nature me sert d'aide-mémoire 
                        pour retrouver les noms des plantes et insectes que je croise en 
                        montagne, en voyage ou autour de chez moi."""))
        nPics = len(self.picCache.getPictures())
        nSpecies = len(self.taxCache.getForRank(TaxonRank.SPECIES))
        nGenera  = len(self.taxCache.getForRank(TaxonRank.GENUS))
        nFamilia = len(self.taxCache.getForRank(TaxonRank.FAMILY))
        divAbout.addTag(HtmlTag('p', f"""C'est aussi une collection de taxons qui compte actuellement 
                                <b>{nPics}</b> photos dans <b>{nSpecies}</b> espèces, 
                                <b>{nGenera}</b> genres et <b>{nFamilia}</b> familles."""))

        # Newest species
        tdRight = tableLeftRight.getNextCell()
        divNewSpecies = MyBoxHtmlTag('Dernières espèces')
        listNewSpecies = divNewSpecies.addList()
        for (idx, tFirstObs) in self.taxCache.fetchNewestSpecies():
            tax = self.taxCache.findById(idx)
            item = listNewSpecies.addItem()
            item.addTag(LinkHtmlTag(self.getTaxonLink(tax), tax.getNameFr(), False, tax.getName()))
            item.addTag(GrayFontHtmlTag(DateTools.datetimeToPrettyStringFr(tFirstObs)))
        tdRight.addTag(divNewSpecies)

        # Latest excursions
        divExcursions = MyBoxHtmlTag('Excursions récentes')
        tdRight.addTag(divExcursions)
        ul = divExcursions.addList()
        excursions = self.excCache.getExpeditions()[:6]
        for excursion in excursions:
            li = ul.addItem()
            li.addTag(LinkHtmlTag(f'excursion{excursion.getIdx()}.html', excursion.getName()))
            li.addTag(GrayFontHtmlTag(DateTools.datetimeToPrettyStringFr(excursion.getFrom())))

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

    def buildExcursions(self):
        """Build excursions pages"""
        page = pynorpaHtml.PynorpaHtmlPage('Nature - Excursions')
        page.addHeading(1, 'Excursions')
        page.addHeading(2, 'Cette page est en construction')

        for excursion in self.excCache.getExpeditions():
            self.buildExcursion(excursion)

        page.save(f'{config.dirWebExport}expeditions.html')

    def buildExcursion(self, excursion: Expedition):
        """Build a single excursion page."""
        page = pynorpaHtml.PynorpaHtmlPage('Nature - Excursions')
        page.addHeading(1, excursion.getName())

        # Excursion details
        divDetails = MyBoxHtmlTag('Excursion')
        page.add(divDetails)
        loc = excursion.getLocation()
        pdate = DateTools.datetimeToPrettyStringFr(excursion.getFrom())
        par = HtmlTag('p')
        par.addTag(LinkHtmlTag(f'lieu{loc.getIdx()}.html', loc.getName()))
        divDetails.addTag(par)
        par = HtmlTag('p')
        par.addTag(GrayFontHtmlTag(f'{pdate} &mdash; {len(excursion.getPictures())} photos'))
        divDetails.addTag(par)
        divDetails.addTag(HtmlTag('p', excursion.getDesc()))
        #divDetails.addTag(HtmlTag('p', TextTools.durationToString(excursion.getTo() - excursion.getFrom())))

        # Excursion pictures
        page.addHeading(2, 'Photos')
        table = TableHtmlTag(None).addAttr('class', 'table-thumbs')
        for pic in excursion.getPictures():
            self.addThumbLinkExcursion(pic, table.getNextCell())
        page.add(table)
        page.save(f'{config.dirWebExport}excursion{excursion.getIdx()}.html')


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
        species = self.taxCache.getForRank(TaxonRank.SPECIES)
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
            family = tax.getAncestor(TaxonRank.FAMILY)
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
                family = tax.getAncestor(TaxonRank.FAMILY)
                if family:
                    li.addTag(GrayFontHtmlTag(f'- {family.getNameFr()}'))
        page.save(f'{config.dirWebExport}noms-verna.html')

    def buildTaxa(self):
        """Build taxon pages"""
        species = self.taxCache.getForRank(TaxonRank.SPECIES)
        for tax in species:
            self.buildSpecies(tax)

    def buildSpecies(self, taxon: Taxon):
        """Build the page for the species."""
        page = pynorpaHtml.PynorpaHtmlPage(f'Nature - {taxon.getName()}')
        title = taxon.getName()
        if taxon.getNameFr() != taxon.getName():
            title += f' &mdash; {taxon.getNameFr()}'
        page.addHeading(1, title)

        # Pictures table
        tablePics = TableHtmlTag([], 2)
        tablePics.addAttr('width', '1040px').addAttr('class', 'table-medium')
        page.add(tablePics)
        pic: picture.Picture
        for pic in taxon.getPictures():
            td = tablePics.getNextCell()
            td.addTag(ImageHtmlTag(f'../medium/{pic.getFilename()}', taxon.getName(), taxon.getName()))
            loc = pic.getLocation()
            locToolTip = f'{loc.getName()}, {loc.getRegion()}, {loc.getState()} ({loc.getAltitude()}m)'
            legend = HtmlTag('p')
            legend.addTag(LinkHtmlTag('#', loc.getName(), False, locToolTip))
            legend.addTag(GrayFontHtmlTag(DateTools.datetimeToPrettyStringFr(pic.getShotAt())))
            td.addTag(legend)
            if (pic.getRemarks()):
                td.addTag(HtmlTag('p', self.replaceRemarkLinks(pic.getRemarks())))
        if len(taxon.getPictures()) % 2 == 1:
            tablePics.getNextCell() # fill the last table row

        # Classification and links table
        divClassif = MyBoxHtmlTag('Classification')
        divLinks   = MyBoxHtmlTag("Plus d'informations")
        tableLinks = TableHtmlTag([divClassif, divLinks], 2)
        tableLinks.addAttr('width', '1040px').addAttr('class', 'align-top')
        page.add(tableLinks)

        # Classification
        tableClassif = TableHtmlTag([], 3).addAttr('width', '500px')
        divClassif.addTag(tableClassif)
        for rank in TaxonRank:
            ancestor = taxon.getAncestor(rank)
            td = tableClassif.getNextCell(ImageHtmlTag(f'rank{rank.value+1}.svg', rank.getNameFr(), rank.getNameFr()))
            td.addTag(InlineHtmlTag(rank.getNameFr(), [], ''))
            tableClassif.getNextCell(self.getTaxonClassif(ancestor))
            tableClassif.getNextCell(ancestor.getNameFr())

        # External links
        ul = ListHtmlTag([])
        divLinks.addTag(ul)
        for provider in self.getTaxonUrlProviders():
            link = provider.getLink(taxon)
            if link:
                ul.addItem(link)
        
        page.save(f'{config.dirWebExport}{self.getTaxonLink(taxon)}')

    def buildTest(self):
        """Build a simple test page."""
        page = pynorpaHtml.PynorpaHtmlPage('Test')
        page.addHeading(1, 'Test')
        page.addHeading(2, 'Bibliographie')
        page.save(f'{config.dirWebExport}test.html')

    def addThumbLink(self, pic: picture.Picture, parent: HtmlTag):
        """Add a preview and description of the specified picture."""
        sShotAt = DateTools.datetimeToPrettyStringFr(pic.getShotAt())
        link = LinkHtmlTag(self.getTaxonLink(pic.taxon), None)
        link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', pic.getTaxonName(), pic.getTaxonName()))
        link.addTag(HtmlTag('i', f'<br>{pic.getTaxonName()}<br>'))
        parent.addTag(link)
        parent.addTag(LinkHtmlTag(f'lieu{pic.getIdxLocation()}.html', pic.getLocationName()))
        parent.addTag(GrayFontHtmlTag(f'<br>{sShotAt}'))

    def addThumbLinkExcursion(self, pic: picture.Picture, parent: HtmlTag):
        """Add a preview and description of the specified picture."""
        taxon: Taxon
        taxon = pic.getTaxon()
        link = LinkHtmlTag(self.getTaxonLink(taxon), None)
        link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', pic.getTaxonName(), pic.getTaxonName()))
        link.addTag(HtmlTag('i', f'<br>{pic.getTaxonName()}<br>'))
        parent.addTag(link)
        parent.addTag(HtmlTag('span', taxon.getNameFr()))
        parent.addTag(HtmlTag('span', f'<br>{taxon.getAncestor(TaxonRank.FAMILY).getName()}'))

    def getTaxonLink(self, taxon: Taxon, rel='pages/') -> str:
        """Get the home-relative link to the specified taxon page."""
        match taxon.getRank():
            case TaxonRank.SPECIES:
                return f"{rel}{taxon.getName().replace(' ', '-').lower()}.html"
            case TaxonRank.GENUS:
                return f'{rel}{taxon.getName().lower()}.html'
        return 'not-implemented.html'

    def getTaxonClassif(self, taxon: Taxon) -> HtmlTag:
        """Get the specified taxon classification table code."""
        match taxon.getRank():
            case TaxonRank.KINGDOM:
                return LinkHtmlTag(f'../classification.html#{taxon.getName()}', taxon.getName(), False, taxon.getNameFr())
            case TaxonRank.PHYLUM | TaxonRank.ORDER:
                return LinkHtmlTag(f'../{taxon.getName()}.html', taxon.getName(), False, taxon.getNameFr())
            case TaxonRank.CLASS | TaxonRank.FAMILY:
                return LinkHtmlTag(f'../{taxon.getParent().getName()}.html#{taxon.getName()}', taxon.getName(), False, taxon.getNameFr())
            case TaxonRank.SPECIES:
                if len(taxon.getName()) > 20:
                    return HtmlTag('i', taxon.getNameShort())
                return HtmlTag('i', taxon.getName())
            case TaxonRank.GENUS:
                return HtmlTag('i', taxon.getName())
    
    def replaceRemarkLinks(self, remark: str) -> str:
        """Replace species references in the specified remark with a link to that species."""
        pat = re.compile(".+\\[\\[(.+)\\]\\].*")
        match = pat.match(remark)
        if match:
            taxName = match.group(1)
            repl = taxName
            tax = self.taxCache.findByName(taxName)
            if tax:
                link = LinkHtmlTag(self.getTaxonLink(tax, ''), tax.getName(), False, tax.getNameFr())
                repl = link.getHtml(0, True)
            else:
                self.log.error('Failed to find taxon %s', taxName)
            remark = remark.replace(f'[[{taxName}]]', repl)
        return remark

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
