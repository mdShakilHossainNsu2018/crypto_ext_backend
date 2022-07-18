from celery import shared_task
import requests
from top_gainer_losser.models import TopStockGainers, TopStockLosers, TopCryptoGainer, TopCryptoLoser
from bs4 import BeautifulSoup
import cloudscraper

API_KEY = "60b10dc3385cdcbb8689ecb1a8fb893f"


@shared_task
def get_and_save_gainer_losser_object():
    stock_gainer()
    stock_losser()


@shared_task
def get_and_save_crypto_top_gainer_loser():
    scraper = cloudscraper.create_scraper()
    # res = requests.get("https://www.coingecko.com/en/crypto-gainers-losers")
    soup = BeautifulSoup(scraper.get("https://www.coingecko.com/en/crypto-gainers-losers").text, 'html.parser')
    table = soup.find_all('table', {'id': 'gecko-table-all'})

    save_crypto_gainer(table[0])

    save_crypto_loser(table[1])


def save_crypto_gainer(table):
    try:
        TopCryptoGainer.objects.all().delete()
    except Exception as e:
        print(e)

    for row in table.tbody.findAll("tr"):
        try:
            coin_img = row.td.find_all('img')[0]['src']
            coin_name = row.td.find_all('span', {'class': ['tw-hidden', 'd-lg-block', 'font-bold']})[1].text
            symbol = row.td.find_all('span', {'class': ['tw-hidden', 'd-lg-block', 'font-bold']})[0].text
            volume = row.find_all('span', {'class': 'no-wrap'})[0].text.split("$")[1].replace(',', '')
            price = row.find_all('span', {'class': 'no-wrap'})[1].text.split("$")[1].replace(',', '')
            percentage_change = row.find_all('span', {'class': 'badge'})[0].text.split("%")[0]
            TopCryptoGainer.objects.create(coin_img=coin_img,
                                           coin_name=coin_name,
                                           symbol=symbol,
                                           volume=volume,
                                           price=price,
                                           percentage_change=percentage_change
                                           )

        except Exception as e:
            print(e)


def save_crypto_loser(table):
    try:
        TopCryptoLoser.objects.all().delete()
    except Exception as e:
        print(e)

    for row in table.tbody.findAll("tr"):
        try:
            coin_img = row.td.find_all('img')[0]['src']
            coin_name = row.td.find_all('span', {'class': ['tw-hidden', 'd-lg-block', 'font-bold']})[1].text
            symbol = row.td.find_all('span', {'class': ['tw-hidden', 'd-lg-block', 'font-bold']})[0].text
            volume = row.find_all('span', {'class': 'no-wrap'})[0].text.split("$")[1].replace(',', '')
            price = row.find_all('span', {'class': 'no-wrap'})[1].text.split("$")[1].replace(',', '')
            percentage_change = row.find_all('span', {'class': 'badge'})[0].text.split("%")[0]
            TopCryptoLoser.objects.create(coin_img=coin_img,
                                           coin_name=coin_name,
                                           symbol=symbol,
                                           volume=volume,
                                           price=price,
                                           percentage_change=percentage_change
                                           )

        except Exception as e:
            print(e)



def stock_gainer():
    url = "https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey=" + API_KEY
    res = requests.get(url)
    res_json = res.json()

    try:
        TopStockGainers.objects.all().delete()
    except Exception as e:
        print(e)

    for item in res_json:
        try:
            TopStockGainers.objects.create(symbol=item['symbol'],
                                           name=item['name'],
                                           price=item['price'],
                                           change=item['change'],
                                           changes_percentage=item['changesPercentage'])
        except Exception as e:
            print(e)


def stock_losser():
    url = "https://financialmodelingprep.com/api/v3/stock_market/losers?apikey=" + API_KEY
    res = requests.get(url)
    res_json = res.json()
    try:
        TopStockLosers.objects.all().delete()
    except Exception as e:
        print(e)

    for item in res_json:
        try:
            TopStockLosers.objects.create(symbol=item['symbol'],
                                          name=item['name'],
                                          price=item['price'],
                                          change=item['change'],
                                          changes_percentage=item['changesPercentage'])
        except Exception as e:
            print(e)
