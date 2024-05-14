# scrapy runspider webscrapingIGN.py -o resultIGN.json -t json -s FEED_EXPORT_ENCODING=utf-8
#importamos scrapy y sus metodos
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

#Creamos la clase que va a alojar a las cosas que queremos scrapear

class Articulo(Item):
    #Creamos una variable para alojar los titulos heredandolos de la clase field
    titulo = Field()
    #Creamos una variable para alojar el contenido heredandolos de la clase field
    contenido = Field()

"""
PARA LA BUSQUEDA DE PS4 NO HAY REVIEWS ASI QUE NO LO VOY A HACER
class Review(Item):
    #Creamos una variable para alojar los titulos heredandolos de la clase field
    titulo = Field()
    #Creamos una variable para alojar las clasificaciones heredandolos de la clase field
    calificacion = Field()
"""
class Video(Item):
    #Creamos una variable para alojar los titulos heredandolos de la clase field
    titulo = Field()
    #Creamos una variable para alojar las fechas de publicacion heredandolos de la clase field
    fecha_de_publicacion = Field()

#Iniciamos el crawlspider y le ponemos nuestras custom settings
class IGNCrawler(CrawlSpider):
    # Le damos el nombre
    name = "ign"
    #Le damos nuestros parametros sobre el header y la cantidad de paginas a scrapear
    custom_settings = {
        #Header
        "USER_AGENT" : "Opera GX (Windows 10)",
        #Paginas a scrapear
        "CLOSESPIDER_PAGECOUNT" : 10
    }

    #Le indicamos los dominios permitidos
    allowed_domains = ["latam.ign.com"]

    #La url en donde va a empezar a hacer el scrapeo
    start_urls = ["https://latam.ign.com/se/?model=article&q=ps4"]

    # Le indicamos el delay que tiene entre las operaciones de scrapeo
    download_delay = 1

    #Asignamos las reglas
    rules = (
        #Sigue las url que contengan type
        Rule(LinkExtractor(allow=r'type='), follow=True), 
        #Sigue las url que contengan review y hace referencia al metodo parse_review
        Rule(LinkExtractor(allow=r'review'), follow=True, callback= "parse_review"),
        #Sigue las url que contengan video y hace referencia al metodo parse_video
        Rule(LinkExtractor(allow=r'video'), follow=True, callback= "parse_video"),
        #Sigue las url que contengan news y hace referencia al metodo parse_news
        Rule(LinkExtractor(allow=r'news'), follow=True, callback= "parse_news"))

    def parse_video(self, response):
        #Creamos lo que va a cargar a la variable
        item = ItemLoader(Video(), response)

        #Agregamos el item con su xpath
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('fecha_de_publicacion', '//span[@class ="publish-date"]/text()')

        #Usamos el yield para cargar la informacion
        yield item.load_item()


    def parse_news(self, response):
        #Creamos lo que va a cargar a la variable
        item = ItemLoader(Articulo(), response)

        #Agregamos el item con su xpath
        item.add_xpath('titulo', '//h1/text()')
        #en este caso como dentro del div del texto, el texto esta dividido en muchas <p> usamos //*/text()
        # para que nos extraiga todos los textos de las etiquetas hijos que contiene
        item.add_xpath('contenido', '//div[@id ="id_text"]//*/text()')

        #Usamos el yield para cargar la informacion
        yield item.load_item()
