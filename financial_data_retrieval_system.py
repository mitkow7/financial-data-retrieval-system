import requests
import yfinance as yf


class FinancialDataRetrievalSystem:
    def __init__(self, currency_api_key, share_and_crypto_api_key):
        # Initialize attributes
        self.currency_api_key = currency_api_key
        self.share_and_crypto_api_key = share_and_crypto_api_key

    def get_currency_exchange_rate(self, base_currency, target_currency):
        # Retrieve the current exchange rate between two currencies using the currency API

        url = f'https://v6.exchangerate-api.com/v6/{self.currency_api_key}/pair/{base_currency}/{target_currency}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            exchange_rate = round(data['conversion_rate'], 2)

            return f'💸 The exchange rate for {base_currency} to {target_currency} is {exchange_rate:.2f} 💸'
        else:
            return '❌ERROR!❌\nPlease try again.'

    def get_currency_conversion(self, amount, base_currency, target_currency):
        # Convert the given amount from one currency to another

        url = f'https://v6.exchangerate-api.com/v6/{self.currency_api_key}/pair/{base_currency}/{target_currency}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        else:
            return 'ERROR!\nPlease try again.'

        exchange_rate = data['conversion_rate']
        converted_amount = round(exchange_rate * amount, 2)

        return converted_amount

    def get_top_gainers(self):
        # Retrieve the top gaining companies from the share API

        url = f'https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey={self.share_and_crypto_api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
        else:
            return '❌ERROR!❌\nPlease try again.'

        return data

    def get_top_losers(self):
        # Retrieve the top losing companies from the share API

        url = f'https://financialmodelingprep.com/api/v3/stock_market/losers?apikey={self.share_and_crypto_api_key}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        else:
            return 'ERROR!\nPlease try again.'

        return data

    def get_crypto_info(self, crypto_currency):
        # Retrieve additional information about a crypto (e.g., name, price) using the share_crypto API

        url = f'https://financialmodelingprep.com/api/v3/quote/{crypto_currency}?apikey={self.share_and_crypto_api_key}'

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        else:
            return '❌ERROR!❌\nPlease try again.'

        name = data[0]['name']
        price = round(data[0]['price'], 2)
        change_percent = round(data[0]['changesPercentage'], 2)

        return name, price, change_percent


def get_company_share_price(company_symbol):
    # Retrieve the current price of shares for a given company using the share API

    data = yf.Ticker(company_symbol)

    company_share_price = round(data.info['currentPrice'], 2)

    return company_share_price


def get_company_info(company_symbol):
    # Retrieve additional information about a company (e.g., name, sector) using the share API

    data = yf.Ticker(company_symbol)

    company_info = {'symbol': company_symbol, 'share_price': data.info['currentPrice'],
                    'country': data.info['country'],
                    'industry': data.info['industry'], 'sector': data.info['sector'],
                    'long_name': data.info['longName'], 'city': data.info['city']}

    return company_info


def display_top_five_gainers_and_losers(top_companies: dict):
    for i in range(0, len(top_companies)):
        if i == 5:
            break

        print()
        print(f"{i + 1} - Symbol: {top_companies[i]['symbol']}")
        print(f"{i + 1} - Name: {top_companies[i]['name']}")
        print(f'{i + 1} - Price: {round(top_companies[i]['price'], 2):.2f}')
        print(f'{i + 1} - Change: {round(top_companies[i]['changesPercentage'], 2):.2f}%')


def display_company_info(company_info):
    print()
    print(f"Company Symbol: {company_info['symbol']}")
    print(f"Company Share Price: {round(company_info['share_price'], 2)}")
    print(f"Company City: {company_info['city']}")
    print(f"Company Country: {company_info['country']}")
    print(f"Company Industry: {company_info['industry']}")
    print(f"Company Sector: {company_info['sector']}")
    print(f"Company Name: {company_info['long_name']}")


def display_menu():
    menu = """
     -----MENU-----
        Currency
1. Currency Exchange Rate 💵
2. Currency Conversion 💵

        Stocks
3. Company Share Price 📈
4. Company Info 📝
5. Top Gainers 📈
6. Top Losers 📉

        Crypto
7. Crypto Price 🚀
-------------
8. Quit"""
    print(menu)


def main():
    currency_api_key = 'API KEY'
    share_and_crypto_api_key = 'API KEY'

    financial_system = FinancialDataRetrievalSystem(currency_api_key, share_and_crypto_api_key)

    display_menu()

    while True:
        print()
        user_choice = input('Options: 1, 2, 3, 4, 5, 6, 7, 8: ')

        if user_choice == '1':
            base_currency = input('Base Currency: ').upper()
            target_currency = input('Target Currency: ').upper()

            exchange_rate = financial_system.get_currency_exchange_rate(base_currency, target_currency)
            print()
            print(f'{exchange_rate}')
        elif user_choice == '2':
            base_currency = input('Base Currency: ').upper()
            amount = int(input('Amount: '))
            target_currency = input('Target Currency: ').upper()

            currency_conversion = financial_system.get_currency_conversion(amount, base_currency, target_currency)
            print()
            print(f'{currency_conversion:.2f}')

        elif user_choice == '3':
            company_symbol = input('Company Symbol: ').upper()

            company_share_price = get_company_share_price(company_symbol)

            print()
            print(company_share_price)

        elif user_choice == '4':
            company_symbol = input('Company Symbol: ').upper()

            company_info = get_company_info(company_symbol)

            display_company_info(company_info)
        elif user_choice == '5':
            top_gainers = financial_system.get_top_gainers()

            print()
            print(f'Top 5 Gainers:')
            print()

            display_top_five_gainers_and_losers(top_gainers)
        elif user_choice == '6':
            top_losers = financial_system.get_top_losers()

            print()
            print(f'Top 5 Losers:')
            print()

            display_top_five_gainers_and_losers(top_losers)
        elif user_choice == '7':
            crypto_symbol = input('Crypto Symbol: ').upper() + 'USD'

            name, current_price, change_percent = financial_system.get_crypto_info(crypto_symbol)

            print()
            print(f'Crypto Full Name: {name}')
            print(f'Current Price: {current_price:.2f}')
            print(f'Change Percentage: {change_percent:.2f}%')
        elif user_choice == '8':
            print()
            print('Quiting...')
            break
        else:
            print()
            print('❌ Invalid Option! ❌\nPlease try again.')

    print()
    print('✅ Thank you for using Financial Data Retrieval System! ✅')


if __name__ == "__main__":
    main()
