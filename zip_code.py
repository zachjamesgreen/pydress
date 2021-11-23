from yattag import Doc
import xml.etree.ElementTree as ET
import requests
import os



class ZipCode():
    url = "https://secure.shippingapis.com/ShippingAPI.dll?"
    # url = "http://testing.shippingapis.com/ShippingAPITest.dll?"
    userid = os.environ.get('USPS_USERID')
    

    @staticmethod
    def make_xml(zip_code):
        doc, tag, text = Doc().tagtext()
        with tag('CityStateLookupRequest', USERID=ZipCode.userid):
            with tag('ZipCode', ID=0):
                with tag('Zip5'):
                    text(zip_code)
        return doc.getvalue()

    @staticmethod
    def get_city_state(zip_code):
        xml = ZipCode.make_xml(zip_code)
        return requests.post(f'{ZipCode.url}API=CityStateLookup&XML={xml}')

    @staticmethod
    def get_info(zip_code):
        # root.find('Address/Address2').text
        data = ZipCode.get_city_state(zip_code)
        root = ET.fromstring(data.text)
        zip = root.find('ZipCode/Zip5').text
        city = root.find('ZipCode/City').text
        state_abbr = root.find('ZipCode/State').text
        return zip, city, state_abbr

    @staticmethod
    def validate_address_xml(address):
        doc, tag, text = Doc().tagtext()
        with tag('AddressValidateRequest', USERID=ZipCode.userid): 
            with tag('Revision'):
                text('1')
            with tag('Address', ID=0):
                with tag('Address1'):
                    text(address['apt_number'])
                with tag('Address2'):
                    text(address['street'])
                with tag('City'):
                    text(address['city'])
                with tag('State'):
                    text(address['state_abbr'])
                with tag('Zip5'):
                    text(address['zip_code'])
                with tag('Zip4'):
                    text('')
        xml = doc.getvalue()
        res = requests.post(f'{ZipCode.url}API=Verify&XML={xml}')
        root = ET.fromstring(res.text)
        return root