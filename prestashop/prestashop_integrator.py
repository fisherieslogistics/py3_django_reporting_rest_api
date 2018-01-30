import logging
from requests.sessions import Session
import json


class PrestashopIntegrator():
    def __init__(self):
        self.api_url = 'https://shop.test.catchhub.com/harbourfish/api'
        self.api_key = "T5R4BJVTG4445WXFEDBAV23SR13U7XAS"
        self.client = Session()
        self.client.auth = (self.api_key, '')

    def _construct_url(self, resource, resource_id):
        return "%s/%s/%s?output_format=JSON" % (self.api_url, resource, resource_id)

    def _parse_response(self, response):
        if response.status_code != 200:
            raise RuntimeError("HTTP Response %d: %s." % (response.status_code, response.content))
        return json.loads(response.content)

    def get_resource(self, resource, resource_id=''):
        response = self.client.request("GET", self._construct_url(resource, resource_id), headers={'Content-Type': 'application/json'})
        return self._parse_response(response)

    def edit_resource(self, resource, resource_id, xml):
        response = self.client.request("PUT", self._construct_url(resource, resource_id), data=xml, headers={'Content-Type': 'text/xml'})
        return self._parse_response(response)

    def update_stock(self):
        # TODO
        pass


if __name__ == "__main__":
    print("yah")

    #print(PrestashopIntegrator().get_resource("stock_availables"))
    #print(PrestashopIntegrator().get_resource("stock_availables", 60))
    xml = """<?xml version="1.0" encoding="UTF-8"?><prestashop xmlns:xlink="http://www.w3.org/1999/xlink"><stock_available>
    <id><![CDATA[60]]></id>
    <id_shop><![CDATA[2]]></id_shop>
    <quantity><![CDATA[96]]></quantity>
    <id_product><![CDATA[8]]></id_product>
    <id_product_attribute><![CDATA[0]]></id_product_attribute>
    <depends_on_stock><![CDATA[0]]></depends_on_stock>
    <out_of_stock><![CDATA[2]]></out_of_stock>
    </stock_available></prestashop>"""
    print(PrestashopIntegrator().edit_resource("stock_availables", 60, xml))
    print(PrestashopIntegrator().get_resource("stock_availables", 60))
