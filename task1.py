import httpx
from datetime import datetime


class PrivatBankAPI:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    async def fetch_exchange_rates(self, date):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}?json&date={date}")
            return response.json()


class CurrencyConverter:
    def __init__(self, data):
        self.data = data

    def convert_to_desired_format(self):
        # Отримання курсів валют та конвертація в бажаний формат
        currencies = ['EUR', 'USD']
        result = {}
        for currency in currencies:
            for rate in self.data['exchangeRate']:
                if rate['currency'] == currency:
                    result[currency] = {
                        'sale': rate['saleRateNB'],
                        'purchase': rate['purchaseRateNB']
                    }
                    break
            else:
                result[currency] = None
        return result


class ConsoleUI:
    def run(self):
        api = PrivatBankAPI()
        while True:
            date_input = input("Введіть дату (у форматі ДД.ММ.РРРР): ")
            try:
                date = datetime.strptime(
                    date_input, '%d.%m.%Y').strftime('%d.%m.%Y')
            except ValueError:
                print("Некоректний формат дати. Спробуйте ще раз.")
                continue

            data = asyncio.run(api.fetch_exchange_rates(date))
            converter = CurrencyConverter(data)
            converted_data = converter.convert_to_desired_format()
            print(converted_data)
            another_query = input("Бажаєте ввести ще одну дату? (так/ні): ")
            if another_query.lower() != 'так':
                break


if __name__ == "__main__":
    import asyncio
    asyncio.run(ConsoleUI().run())
