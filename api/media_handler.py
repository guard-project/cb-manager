from functools import partial
from xml.parsers.expat import ExpatError

import xmltodict as xml_to_dict
import yaml
from dicttoxml import dicttoxml as dict_to_xml
from falcon.errors import HTTPBadRequest
from falcon.media import JSONHandler
from yaml import FullLoader
from yaml.parser import ParserError, ScannerError


class XMLHandler(JSONHandler):
    def __init__(self, dumps=None, loads=None):
        self.dumps = dumps or partial(
            dict_to_xml, custom_root="guard", attr_type=False)
        self.loads = loads or partial(xml_to_dict.parse, force_list="item")

    def deserialize(self, stream, content_type, content_length):
        try:
            return self.loads(stream.read().decode("utf-8"))["guard"]
        except ExpatError:
            raise HTTPBadRequest("Invalid XML")


class YAMLHandler(JSONHandler):
    def __init__(self, dumps=None, loads=None):
        self.dumps = dumps or partial(yaml.dump, sort_keys=True, indent=3)
        self.loads = loads or partial(yaml.load, Loader=FullLoader)

    def deserialize(self, stream, content_type, content_length):
        try:
            data = stream.read().decode("utf-8")
            return self.loads(data)
        except (ParserError, ScannerError):
            raise HTTPBadRequest("Invalid YAML")
