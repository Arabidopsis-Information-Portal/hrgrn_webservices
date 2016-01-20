# file: main_test.py
import logging
import main as driver

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

TOKEN="d148fa0d549d5489af3a87549f37485"

def list(args):
     raise Exception('Not implemented yet')

def main():
    """test logic for when running this module as the primary one!"""

    # search test case
    args = {'locus': 'AT2G38470'}
    #args = {'locus': 'X'}
    driver.search(args)

if __name__ == '__main__':
    main()
