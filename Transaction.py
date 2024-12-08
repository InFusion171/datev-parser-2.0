from collections import defaultdict
import re

import datetime

class Transaction:
    def __init__(self, iban: str, bic: str, wertstellungsdatum: str, buchungsdatum: str, umsatz:str, verwendungszweck:str, waerung:str):
        self.BIC = bic.replace('"', '').replace(' ', '')
        self.IBAN = iban.replace('"', '').replace(' ', '')
        self.waerung = waerung.replace('"', '')
        self.wertstellungsdatum = wertstellungsdatum.replace('"', '')
        self.buchungsdatum = buchungsdatum.replace('"', '')
        self.umsatz = umsatz.replace('"', '')
        self.verwendungszweck = verwendungszweck.replace('"', '')

        self.VERWENDUNGSZWECK_FIELD_LENGTH = 27
        self.VERWENDUNGSZWECK_FIELD_FIELD_COUNT = 10

    def create_datev_format(s) -> str:
        datev_format = f'"{s.BIC}";"{s.IBAN}";"";"";"{s.wertstellungsdatum}";"{s.buchungsdatum}";{s.umsatz};"";"";"";"";'

        verwendungszweck_index = 0

        for i in range(s.VERWENDUNGSZWECK_FIELD_FIELD_COUNT):
            # DATEV format: verwendungszweck 1-4 | Geschäftsvorgangscode | Währung | Buchungstext | verwendungszweck 5-10
            if(i == 4):
                datev_format = datev_format + f'"";"{s.waerung}";"";'

            datev_format = datev_format + f'"{s.verwendungszweck[verwendungszweck_index:verwendungszweck_index + s.VERWENDUNGSZWECK_FIELD_LENGTH]}";'

            verwendungszweck_index = verwendungszweck_index + s.VERWENDUNGSZWECK_FIELD_LENGTH


        return re.sub(r'("";)*$', '', datev_format)

    def parse(iban: str, bic: str, input: str):
        account_owner = re.search('"Kontoinhaber:";"(.*)"\n', input)

        if(account_owner is None):
            account_owner = ''

        else:
            account_owner = account_owner.group(1)


        date_regex = '\d\d.\d\d.\d\d\d\d'
        umsatz_regex = '\d,\d\d'

        transaction_line_regex = f'.*{date_regex}.*{date_regex}.*{umsatz_regex}.*'

        splitted_input = input.split('\n')

        transactions = []

        for line in splitted_input:
            if re.search(transaction_line_regex, line) is not None:
                transactions.append(line)


        transactions_by_date = defaultdict(list)

        for transaction in transactions:
            values = transaction.split(';')

            if(len(values) < 5):
                raise Exception()

            datev_transaction = Transaction(iban, bic, values[1], values[0], values[3], values[2], values[4])

            valuta_month = values[1].split('.')[1]
            valuta_year = values[1].split('.')[2].replace('"', '')

            transactions_by_date[valuta_year+valuta_month].append(datev_transaction)

        return account_owner, transactions_by_date

def sort_by_buchungstag(transactions: list[Transaction]):
    return sorted(transactions, key=lambda x: datetime.datetime.strptime(x.buchungsdatum, '%d.%m.%Y'))
