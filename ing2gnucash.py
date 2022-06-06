"""
ing2gnucash, copyright 2022 Ronald Philipsen
"""

import sys
import logging
import argparse
from io import TextIOWrapper

import pandas as pd


logger = logging.getLogger('ING2GnuCash')
log_levels = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}

class Ing2GnuCash:
    """
    Main module for the Ing2Gnucash
    """


    def __init__(self, infile:TextIOWrapper, outfile:TextIOWrapper) -> None:
        self.input_data: pd.DataFrame = pd.read_csv(infile, delimiter=';')
        self.outfile:TextIOWrapper = outfile
        debug_output =  f'Input_data\n{str(self.input_data["Af Bij"].value_counts())}'
        logger.debug(debug_output)

    def convert(self):
        """
        convert ING-specific format to gnucash format
        """
        amount='Bedrag (EUR)'

        output_data = pd.DataFrame()
        output_data['Date'] = self.input_data['Datum']
        output_data['Description'] = self.input_data['Naam / Omschrijving']
        output_data['Account'] = self.input_data['Rekening']
        output_data['Deposit'] = self.input_data[amount][self.input_data['Af Bij'] == 'Bij']
        output_data['Withdrawal']  = self.input_data[amount][self.input_data['Af Bij'] == 'Af']
        output_data['Action'] = self.input_data['Mutatiesoort']
        output_data['Notes'] = self.input_data['Mededelingen']

        output_data.to_csv(self.outfile, sep=',')

if __name__ == "__main__":
    DESCRIPTION = 'Convert ING CSV files to GNUCash compatible CSV files'
    logger.addHandler(logging.StreamHandler())


    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-v", "--verbose", dest="verbosity", action="count", default=0,
                    help="Verbosity (between 1-4 occurrences with more leading to more "
                         "verbose logging). CRITICAL=0, ERROR=1, WARN=2, INFO=3, "
                         "DEBUG=4")

    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

    args = parser.parse_args()
    logging.basicConfig(level=log_levels[args.verbosity])

    if args.infile:
        main =  Ing2GnuCash(args.infile, args.outfile)
        main.convert()
    else:
        logger.error('No Input files defined, exiting')
        parser.print_usage()
