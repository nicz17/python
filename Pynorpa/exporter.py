"""Module Exporter"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.1"

import config
import json
import logging
import re
import DateTools
import TextTools
import Timer

from HtmlPage import *
from pynorpaHtml import PynorpaHtmlPage
from picture import Picture, PictureCache
from taxon import Taxon, TaxonRank, TaxonCache
from expedition import Expedition, ExpeditionCache
from LocationCache import LocationCache, Location
from taxonUrlProvider import TaxonUrlProvider

class Exporter():
    """Class Exporter"""
    log = logging.getLogger("Exporter")

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        PynorpaHtmlPage.version = __version__

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
            TaxonUrlProvider('Pyrgus', 'http://www.pyrgus.de/', 'pyrgus.de',
                TaxonRank.ORDER, ['Lepidoptera', 'Orthoptera'], TaxonUrlProvider.formatPyrgus),
            TaxonUrlProvider('Libellenschutz', 'https://libellenschutz.ch/arten/item/', 'libellenschutz.ch',
                TaxonRank.ORDER, ['Odonata'], TaxonUrlProvider.formatLibellenschutz),
            TaxonUrlProvider('Oiseaux de Suisse', 'https://www.vogelwarte.ch/fr/oiseaux/les-oiseaux-de-suisse/',
                'Vogelwarte', TaxonRank.CLASS, ['Aves'], TaxonUrlProvider.formatVogelwarte),
            TaxonUrlProvider('InfoFlora', 'https://www.infoflora.ch/fr/flore/', 'InfoFlora',
                TaxonRank.PHYLUM, ["Lycopodiophyta", "Pteridophyta", "Pinophyta", "Magnoliophyta"],
                TaxonUrlProvider.formatInfoFlora),
            TaxonUrlProvider('MycoDB', 'https://www.mycodb.fr/fiche.php?genre=', 'MycoDB', TaxonRank.PHYLUM,
                ["Ascomycota", "Basidiomycota"]),
            TaxonUrlProvider('Swiss bryophytes', 'https://www.swissbryophytes.ch/index.php/fr/', 'swissbryophytes.ch',
                TaxonRank.PHYLUM, ['Bryophyta'], TaxonUrlProvider.formatEmpty),
            TaxonUrlProvider('Fishipedia', 'https://www.fishipedia.fr/fr/poissons/', 'fishipedia.fr',
                TaxonRank.CLASS, ['Actinopterygii'], TaxonUrlProvider.formatLibellenschutz)
        ]
    def initCaches(self):
        """Init database caches."""
        self.picCache = PictureCache()
        self.taxCache = TaxonCache()
        self.locCache = LocationCache()
        self.excCache = ExpeditionCache()

    def getTaxonUrlProviders(self) -> list[TaxonUrlProvider]:
        return self.taxonUrlProviders

    def buildBasePages(self):
        """Build base html pages."""
        timer = Timer.Timer()
        self.initCaches()

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
        page = PynorpaHtmlPage('Nature - Accueil')
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
            link = LinkHtmlTag(self.getPictureLink(pic), None, False, pic.getTaxonName())
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
        ul.addItem(LinkHtmlTag("Bryophyta.html", "Mousses", False, "Mousses"))
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
        page = PynorpaHtmlPage('Nature - Liens')
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
        page = PynorpaHtmlPage('Nature - Dernières photos')
        page.addHeading(1, 'Dernières photos')
        table = TableHtmlTag(None).addAttr('class', 'table-thumbs')
        aPics = self.picCache.getLatest(12)
        for pic in aPics:
            self.addThumbLink(pic, table.getNextCell())
        page.add(table)
        page.save(f'{config.dirWebExport}latest.html')

    def buildLocations(self):
        """Build the Locations page."""
        page = PynorpaHtmlPage('Nature - Lieux')
        page.addOpenLayerHeaders()
        page.addHeading(1, 'Lieux')

        # Location map
        divMap = page.addTag(DivHtmlTag('ol-map', 'ol-map'))
        divMap.addTag(DivHtmlTag('ol-popup'))
        script = ScriptHtmlTag()
        script.addLine('var oVectorSource, oIconStyle;')
        script.addLine(f'renderMap(6.3902, 46.5377, 9);')
        page.add(script)

        # Locations table
        table = TableHtmlTag(None).addAttr("width", "1000px").addAttr('class', 'align-top')
        page.add(table)
        ul = ListHtmlTag([])
        table.getNextCell().addTag(ul)
        for index, loc in enumerate(self.locCache.getLocations()):
            if index == int(self.locCache.size()/2)+1:
                ul = ListHtmlTag([])
                table.getNextCell().addTag(ul)
            npics = f'&#013;{len(loc.getPictures())} photos'
            title = f'{loc.getName()}&#013;{loc.getRegion()}, {loc.getState()}&#013;{loc.getAltitude()}m{npics}'
            ul.addItem().addTag(LinkHtmlTag(f'lieu{loc.getIdx()}.html', loc.getName(), False, title))
            script.addLine(f'addMapMarker({loc.lon}, {loc.lat}, "{loc.getName()}");')
        page.save(f'{config.dirWebExport}locations.html')

        # Build individual location pages
        for loc in self.locCache.getLocations():
            self.buildLocation(loc)

    def buildLocation(self, loc: Location):
        """Build a single Location page."""
        page = PynorpaHtmlPage('Nature - Lieux')
        page.addOpenLayerHeaders()
        page.addHeading(1, loc.getName())
        tableTop = TableHtmlTag([], 2).addAttr("width", "1440px").addAttr('class', 'align-top')
        page.add(tableTop)

        # Location map
        divMap = DivHtmlTag('ol-map', 'ol-map')
        divMap.addTag(DivHtmlTag('ol-popup'))
        tableTop.getNextCell().addTag(divMap)
        script = ScriptHtmlTag()
        script.addLine('var oVectorSource, oIconStyle;')
        script.addLine(f'renderMap({loc.lon}, {loc.lat}, {loc.zoom});')
        script.addLine(f'addMapMarker({loc.lon}, {loc.lat}, "{loc.getName()}");')
        page.add(script)

        # Location details
        tdRight = tableTop.getNextCell()
        divDetails = MyBoxHtmlTag('Description')
        tdRight.addTag(divDetails)
        divDetails.addTag(HtmlTag('p', loc.getDesc()))
        divDetails.addTag(HtmlTag('p', f'Altitude moyenne {loc.getAltitude()}m'))
        divDetails.addTag(HtmlTag('p', f'{loc.getRegion()}, {loc.getState()}'))

        # Excursions
        if len(loc.getExcursions()) > 0:
            divExcursions = MyBoxHtmlTag('Excursions')
            tdRight.addTag(divExcursions)
            ul = ListHtmlTag([])
            divExcursions.addTag(ul)
            exc: Expedition
            for exc in loc.getExcursions():
                li = ul.addItem()
                li.addTag(LinkHtmlTag(f'excursion{exc.getIdx()}.html', exc.getName()))
                li.addTag(GrayFontHtmlTag(DateTools.datetimeToPrettyStringFr(exc.getFrom())))

        # Add nearby locations
        closest = self.locCache.getClosestListCached(loc)
        if len(closest) > 0:
            divClosest = MyBoxHtmlTag('Lieux à proximité')
            tdRight.addTag(divClosest)
            ul = ListHtmlTag([])
            divClosest.addTag(ul)
            for pair in closest:
                locClose = pair[0]
                dist = pair[1]
                sDist = f'à {dist:.0f} m' if dist < 1000 else f'à {(dist/1000.0):.1f} km'
                li = ul.addItem()
                li.addTag(LinkHtmlTag(f'lieu{locClose.getIdx()}.html', locClose.getName()))
                li.addTag(GrayFontHtmlTag(sDist))

        # Add map links
        parLinks = HtmlTag('p', 'Liens ').addAttr('style', 'padding-top: 10px;')
        tdRight.addTag(parLinks)
        parLinks.addTag(LinkHtmlTag(f'https://www.openstreetmap.org/#map=15/{loc.lat:.5f}/{loc.lon:.5f}', 'OpenStreetMap ', True))
        parLinks.addTag(LinkHtmlTag(f'https://macrostrat.org/map/#x={loc.lon:.5f}&y={loc.lat:.5f}&z=15', 'MacroStrat  ', True))
        parLinks.addTag(LinkHtmlTag(f'https://www.google.com/maps/@{loc.lat:.5f},{loc.lon:.5f},15z', 'Google Maps', True))

        # Location pictures
        page.addHeading(2, 'Photos')
        table = TableHtmlTag(None).addAttr('class', 'table-thumbs')
        for pic in loc.getPictures():
            self.addThumbLinkExcursion(pic, table.getNextCell())
        page.add(table)

        page.save(f'{config.dirWebExport}lieu{loc.getIdx()}.html')

    def buildExcursions(self):
        """Build excursions pages"""
        page = PynorpaHtmlPage('Nature - Excursions')
        page.addHeading(1, 'Excursions')
        page.menu.addTag(HtmlTag('h2', 'Excursions'))
        tableMenu = TableHtmlTag([], 2).addAttr('width', '120px')
        page.menu.addTag(tableMenu)
        year = None
        ul = None
        for exc in self.excCache.getExpeditions():
            if year != exc.getFrom().year:
                year = exc.getFrom().year
                anchor = AnchorHtmlTag(str(year))
                anchor.addTag(HtmlTag('h2', str(year)))
                page.add(anchor)
                tableMenu.getNextCell().addTag(LinkHtmlTag(f'#{year}', str(year)))
                ul = ListHtmlTag([])
                page.add(ul)
            li = ul.addItem()
            li.addTag(LinkHtmlTag(f'excursion{exc.getIdx()}.html', exc.getName()))
            li.addTag(GrayFontHtmlTag(DateTools.datetimeToPrettyStringFr(exc.getFrom())))
        page.save(f'{config.dirWebExport}expeditions.html')

        for excursion in self.excCache.getExpeditions():
            self.buildExcursion(excursion)

    def buildExcursion(self, excursion: Expedition):
        """Build a single excursion page."""
        page = PynorpaHtmlPage('Nature - Excursions')
        page.addOpenLayerHeaders()
        page.addHeading(1, excursion.getName())
        tableTop = TableHtmlTag([], 2).addAttr("width", "1440px").addAttr('class', 'align-top')
        page.add(tableTop)

        # Excursion map
        loc = excursion.getLocation()
        divMap = DivHtmlTag('ol-map', 'ol-map')
        divMap.addTag(DivHtmlTag('ol-popup'))
        tableTop.getNextCell().addTag(divMap)
        script = ScriptHtmlTag()
        page.addTag(script)
        script.addLine('var oVectorSource, oIconStyle;')
        script.addLine(f'renderMap({loc.lon}, {loc.lat}, {loc.zoom});')
        script.addLine(f'addMapMarker({loc.lon}, {loc.lat}, "{loc.getName()}");')
        if excursion.getTrack():
            script.addLine(f'addMapTrack("geotrack/{excursion.getTrack()}.gpx");')

        # Excursion details
        divDetails = MyBoxHtmlTag('Excursion')
        tableTop.getNextCell().addTag(divDetails)
        pdate = DateTools.datetimeToPrettyStringFr(excursion.getFrom())
        par = HtmlTag('p')
        par.addTag(LinkHtmlTag(self.getLocationLink(loc), loc.getName()))
        divDetails.addTag(par)
        par = HtmlTag('p')
        par.addTag(GrayFontHtmlTag(f'{pdate} &mdash; {len(excursion.getPictures())} photos'))
        divDetails.addTag(par)
        divDetails.addTag(HtmlTag('p', excursion.getDesc()))
        divDetails.addTag(HtmlTag('p', f'Durée {TextTools.durationToString(excursion.getDuration())}'))

        # Excursion pictures
        page.addHeading(2, 'Photos')
        table = TableHtmlTag(None).addAttr('class', 'table-thumbs')
        for pic in excursion.getPictures():
            self.addThumbLinkExcursion(pic, table.getNextCell())
            self.addPicMarker(script, pic)
        page.add(table)
        page.save(f'{config.dirWebExport}excursion{excursion.getIdx()}.html')

    def buildAlpha(self):
        """Build names index page"""
        page = PynorpaHtmlPage('Nature - Noms latins')
        page.addHeading(1, 'Noms latins')
        page.menu.addTag(HtmlTag('h2', 'Noms latins'))
        tableMenu = TableHtmlTag([], 4).addAttr('width', '120px')
        page.menu.addTag(tableMenu)

        letter = None
        ul = None
        species = self.taxCache.getForRank(TaxonRank.SPECIES)
        for tax in species:
            letterTax = tax.getName()[:1].upper()
            if letterTax != letter:
                letter = letterTax
                tableMenu.getNextCell().addTag(LinkHtmlTag(f'#{letter}', letter))
                anchor = AnchorHtmlTag(letter)
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
        page = PynorpaHtmlPage('Nature - Noms communs')
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
                    anchor = AnchorHtmlTag(letter)
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
        self.buildClassification()
        for taxon in self.taxCache.getForRank(TaxonRank.PHYLUM):
            self.buildPhylum(taxon)
        for taxon in self.taxCache.getForRank(TaxonRank.ORDER):
            self.buildOrder(taxon)
        for taxon in self.taxCache.getForRank(TaxonRank.SPECIES):
            self.buildTaxon(taxon)
        self.buildTaxaJson()

    def buildTaxaJson(self):
        """Generate the taxa.json file for the classification tree."""
        self.log.info('Building taxa.json for classification tree')
        data = []
        for taxon in self.taxCache.getTopLevelTaxa():
            self.taxonToTreeJson(taxon, data)
        with open(f'{config.dirWebExport}taxa.json', 'w') as file:
            file.write(json.dumps(data))

    def taxonToTreeJson(self, taxon: Taxon, data: list):
        """Export the taxon and its children for the classification tree."""
        link = None
        pic: Picture
        pic = taxon.getTypicalPicture()
        if pic is None:
            self.log.warning(f'No picture found for {taxon}, skipping')
            return
        else:
            link = pic.getFilename().removesuffix('.jpg')
        item = {
            'id': taxon.idx,
            'parent': taxon.idxParent if taxon.idxParent and taxon.idxParent > 0 else '#',
            'icon': f'rank{taxon.rank.value+1}.svg',
            'text': taxon.getName(),
            'a_attr': {
                'link': link,
                'href': self.getTaxonTreeLink(taxon),
                'title': taxon.getNameFr(),
                'pics': taxon.countAllPictures()
            }
        }
        if taxon.rank == TaxonRank.KINGDOM:
            item['state'] = {'opened': True}
        data.append(item)

        for child in taxon.getChildren():
            self.taxonToTreeJson(child, data)

    def buildClassification(self):
        """Build main classification page."""
        page = PynorpaHtmlPage(f'Nature - Classification')
        page.menu.addTag(HtmlTag('h2', 'Classification'))
        page.addHeading(1, 'Classification')

        for kingdom in self.taxCache.getTopLevelTaxa():
            page.addTag(AnchorHtmlTag(kingdom.getName()))
            page.addHeading(2, f'{kingdom.getName()} &mdash; {kingdom.getNameFr()}')
            menuLink = HtmlTag('h3')
            menuLink.addTag(LinkHtmlTag(f'#{kingdom.getName()}', kingdom.getName()))
            page.menu.addTag(menuLink)
            tablePhyla = TableHtmlTag([]).addAttr('class', 'table-thumbs')
            page.addTag(tablePhyla)
            for phylum in kingdom.getChildren():
                pic: Picture
                pic = phylum.getTypicalPicture()
                link = LinkHtmlTag(f'{phylum.getName()}.html', None)
                link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', phylum.getNameFr(), phylum.getName()))
                link.addTag(HtmlTag('span', f'<br>{phylum.getName()} ({len(phylum.getChildren())})'))
                td = tablePhyla.getNextCell()
                td.addTag(AnchorHtmlTag(f'#{phylum.getName()}'))
                td.addTag(link)
        page.save(f'{config.dirWebExport}classification.html')

    def buildPhylum(self, taxon: Taxon):
        """Build a Phylum classification page."""
        page = PynorpaHtmlPage(f'Nature - {taxon.getName()}')
        page.menu.addTag(HtmlTag('h2', 'Classification'))
        page.addHeading(1, f'{taxon.getName()} &mdash; {taxon.getRankFr()} {taxon.getNameFr()}')

        for child in taxon.getChildren():
            page.addTag(AnchorHtmlTag(child.getName()))
            page.addHeading(2, f'{child.getName()} &mdash; {child.getRankFr()} {child.getNameFr()}')
            menuLink = HtmlTag('h3')
            menuLink.addTag(LinkHtmlTag(f'#{child.getName()}', child.getName()))
            page.menu.addTag(menuLink)
            tableThumbs = TableHtmlTag([]).addAttr('class', 'table-thumbs')
            page.addTag(tableThumbs)
            for subchild in child.getChildren():
                pic: Picture
                pic = subchild.getTypicalPicture()
                if not pic:
                    self.log.error('No typical picture found for %s', subchild)
                    continue
                link = LinkHtmlTag(f'{subchild.getName()}.html', None)
                link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', subchild.getNameFr(), subchild.getName()))
                link.addTag(HtmlTag('span', f'<br>{subchild.getName()} ({len(subchild.getChildren())})'))
                td = tableThumbs.getNextCell()
                td.addTag(AnchorHtmlTag(f'#{subchild.getName()}'))
                td.addTag(link)
        page.save(f'{config.dirWebExport}{taxon.getName()}.html')

    def buildOrder(self, taxon: Taxon):
        """Build an Order classification page with its families and species."""
        page = PynorpaHtmlPage(f'Nature - {taxon.getName()}')
        page.menu.addTag(HtmlTag('h2', 'Classification'))
        page.addHeading(1, f'{taxon.getName()} &mdash; {taxon.getRankFr()} {taxon.getNameFr()}')

        for family in taxon.getChildren():
            page.addTag(AnchorHtmlTag(family.getName()))
            page.addHeading(2, f'{family.getName()} &mdash; {family.getRankFr()} {family.getNameFr()}')
            menuLink = HtmlTag('h3')
            menuLink.addTag(LinkHtmlTag(f'#{family.getName()}', family.getName()))
            page.menu.addTag(menuLink)
            tableThumbs = TableHtmlTag([]).addAttr('class', 'table-thumbs')
            page.addTag(tableThumbs)
            # Observation of unknown Genus
            pic: Picture
            if len(family.getPictures()) > 0:
                pic = family.getPictures()[0]
                link = LinkHtmlTag(self.getTaxonLink(family), None)
                link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', family.getNameFr(), family.getName()))
                link.addTag(HtmlTag('span', f'<br>{family.getName()} indéterminés'))
                td = tableThumbs.getNextCell()
                td.addTag(link)
                self.buildTaxon(family)
            for genus in family.getChildren():
                # Observations of unknown species
                if len(genus.getPictures()) > 0:
                    pic = genus.getPictures()[0]
                    link = LinkHtmlTag(self.getTaxonLink(genus), None)
                    link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', genus.getNameFr(), genus.getName()))
                    link.addTag(HtmlTag('i', f'<br>{genus.getName()} sp.'))
                    td = tableThumbs.getNextCell()
                    td.addTag(link)
                    self.buildTaxon(genus)
                for species in genus.getChildren():
                    pic = species.getBestPicture()
                    if not pic:
                        self.log.error('No picture for %s', species)
                        continue
                    link = LinkHtmlTag(self.getTaxonLink(species), None)
                    link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', species.getNameFr(), species.getName()))
                    link.addTag(HtmlTag('i', f'<br>{species.getName()}'))
                    td = tableThumbs.getNextCell()
                    td.addTag(AnchorHtmlTag(f"#{species.getName().replace(' ', '-')}"))
                    td.addTag(link)
                    if species.getNameFr() != species.getName():
                        td.addTag(HtmlTag('span', f'<br>{species.getNameFr()}'))
        page.save(f'{config.dirWebExport}{taxon.getName()}.html')

    def buildTaxon(self, taxon: Taxon):
        """Build the page for the taxon: genus or species."""
        page = PynorpaHtmlPage(f'Nature - {taxon.getName()}', '../')
        page.menu.addTag(HtmlTag('h2', 'Classification'))
        title = taxon.getName()
        if taxon.getNameFr() != taxon.getName():
            title += f' &mdash; {taxon.getNameFr()}'
        page.addHeading(1, title)

        # Pictures table
        tablePics = TableHtmlTag([], 2)
        tablePics.addAttr('width', '1040px').addAttr('class', 'table-medium')
        page.add(tablePics)
        pic: Picture
        for pic in taxon.getPictures():
            td = tablePics.getNextCell()
            td.addTag(AnchorHtmlTag(pic.getFilename().removesuffix('.jpg')))
            picLink = LinkHtmlTag(f'../photos/{pic.getFilename()}', None)
            picLink.addTag(ImageHtmlTag(f'../medium/{pic.getFilename()}', taxon.getName(), taxon.getName()))
            td.addTag(picLink)
            loc = pic.getLocation()
            locToolTip = f'{loc.getName()}, {loc.getRegion()}, {loc.getState()} ({loc.getAltitude()}m)'
            legend = HtmlTag('p')
            legend.addTag(LinkHtmlTag(self.getLocationLink(loc, '../'), loc.getName(), False, locToolTip))
            legend.addTag(GrayFontHtmlTag(DateTools.datetimeToPrettyStringFr(pic.getShotAt())))
            td.addTag(legend)
            if (pic.getRemarks()):
                td.addTag(HtmlTag('p', self.replaceRemarkLinks(pic)))
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
            if ancestor:
                td = tableClassif.getNextCell(ImageHtmlTag(f'rank{rank.value+1}.svg', rank.getNameFr(), rank.getNameFr()))
                td.addTag(InlineHtmlTag(rank.getNameFr(), [], ''))
                link = self.getTaxonClassif(ancestor)
                tableClassif.getNextCell(link)
                tableClassif.getNextCell(ancestor.getNameFr())
                if rank != TaxonRank.GENUS:
                    menuLink = HtmlTag('h3')
                    menuLink.addTag(link)
                    page.menu.addTag(menuLink)

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
        page = PynorpaHtmlPage('Test')
        page.addHeading(1, 'Test')
        page.addHeading(2, 'Bibliographie')
        page.save(f'{config.dirWebExport}test.html')

    def addThumbLink(self, pic: Picture, parent: HtmlTag):
        """Add a preview and description of the specified picture."""
        sShotAt = DateTools.datetimeToPrettyStringFr(pic.getShotAt())
        link = LinkHtmlTag(self.getTaxonLink(pic.taxon), None)
        link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', pic.getTaxonName(), pic.getTaxonName()))
        link.addTag(HtmlTag('i', f'<br>{pic.getTaxonName()}<br>'))
        parent.addTag(link)
        parent.addTag(LinkHtmlTag(f'lieu{pic.getIdxLocation()}.html', pic.getLocationName()))
        parent.addTag(GrayFontHtmlTag(f'<br>{sShotAt}'))

    def addThumbLinkExcursion(self, pic: Picture, parent: HtmlTag):
        """Add a preview and description of the specified picture."""
        taxon: Taxon
        taxon = pic.getTaxon()
        link = LinkHtmlTag(self.getTaxonLink(taxon), None)
        link.addTag(ImageHtmlTag(f'thumbs/{pic.getFilename()}', pic.getTaxonName(), pic.getTaxonName()))
        link.addTag(HtmlTag('i', f'<br>{pic.getTaxonName()}<br>'))
        parent.addTag(link)
        parent.addTag(HtmlTag('span', taxon.getNameFr()))
        parent.addTag(HtmlTag('span', f'<br>{taxon.getAncestor(TaxonRank.FAMILY).getName()}'))

    def addPicMarker(self, script: ScriptHtmlTag, pic: Picture):
        """Add JS code for a map marker."""
        photoInfo = pic.getPhotoInfo()
        if photoInfo and photoInfo.hasGPSData():
            coords = f'{photoInfo.lon:.6f}, {photoInfo.lat:.6f}'
            img = f'"<img src=\'thumbs/{pic.getFilename()}\'>"'
            link = f'"{self.getTaxonLink(pic.getTaxon())}#{pic.getFilename().replace(".jpg", "")}"'
            script.addLine(f'addPicMarker({coords}, {img}, {link});')

    def getLocationLink(self, loc: Location, path=''):
        return f'{path}lieu{loc.getIdx()}.html'

    def getTaxonLink(self, taxon: Taxon, rel='pages/') -> str:
        """Get the relative link to the specified taxon page."""
        match taxon.getRank():
            case TaxonRank.SPECIES:
                return f"{rel}{taxon.getName().replace(' ', '-').lower()}.html"
            case TaxonRank.GENUS | TaxonRank.FAMILY:
                return f'{rel}{taxon.getName().lower()}.html'
        return 'not-implemented.html'

    def getTaxonTreeLink(self, taxon: Taxon) -> str:
        """Get the home-relative link to the specified taxon page."""
        match taxon.getRank():
            case TaxonRank.SPECIES:
                return f"pages/{taxon.getName().replace(' ', '-').lower()}.html"
            case TaxonRank.GENUS:
                return self.getTaxonTreeLink(taxon.getParent())
            case TaxonRank.CLASS | TaxonRank.FAMILY:
                return f'{taxon.getParent().getName()}.html#{taxon.getName()}'
            case TaxonRank.PHYLUM | TaxonRank.ORDER:
                return f'{taxon.getName()}.html'
            case TaxonRank.KINGDOM:
                return f'classification.html#{taxon.getName()}'

    def getPictureLink(self, pic: Picture, rel='pages/') -> str:
        """Get the home-relative link to the specified taxon page."""
        taxon: Taxon
        taxon = pic.getTaxon()
        anchor = f"#{pic.getFilename().removesuffix('.jpg')}"
        match taxon.getRank():
            case TaxonRank.SPECIES:
                return f"{rel}{taxon.getName().replace(' ', '-').lower()}.html{anchor}"
            case TaxonRank.GENUS | TaxonRank.FAMILY:
                return f'{rel}{taxon.getName().lower()}.html{anchor}'
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
    
    def replaceRemarkLinks(self, pic: Picture) -> str:
        """Replace species references in the specified remark with a link to that species."""
        remark = pic.getRemarks()
        pat = re.compile(".+\\[\\[(.+)\\]\\].*")
        match = pat.match(remark)
        if match:
            taxName = match.group(1)
            repl = f'<i>{taxName}</i>'
            tax = self.taxCache.findByName(taxName)
            if tax:
                link = LinkHtmlTag(self.getTaxonLink(tax, ''), f'<i>{tax.getName()}</i>', False, tax.getNameFr())
                repl = link.getHtml(0, True)
            else:
                self.log.warning('Failed to find taxon %s in remark of %s', taxName, pic)
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
    exporter.initCaches()
    #exporter.buildTest()
    #exporter.buildBasePages()
    exporter.buildTaxaJson()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testExporter()
