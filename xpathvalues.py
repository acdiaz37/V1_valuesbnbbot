import requests
import lxml.html as html

XPATH_EXT_VALUE_CONTRACT = '//div[@class="col-md-8"]/text()'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

##URL_CONTRACT='https://bscscan.com/address/0x7c8ffcfEFFf2e62A77BfA82bDba730cC0e8129CF'
##URL_CONTRACT2='https://bscscan.com/address/0x56a9602b20f100cdc990b6048760142A071EA8AB'


def getting_value(contract):
    try:
        URL_CONTRACT = f'https://bscscan.com/address/{contract}'
        response =  requests.get(URL_CONTRACT,headers=headers)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            valueContract = parsed.xpath(XPATH_EXT_VALUE_CONTRACT)
            try:
                print (valueContract[2])
                finalvalue = valueContract[2]
                return finalvalue
            except:
                return ['','','error value']
        else:
            raise ValueError(f'Error {response.status_code}')
    except ValueError as ve:
        print (ve)
        return ['','','error value']

