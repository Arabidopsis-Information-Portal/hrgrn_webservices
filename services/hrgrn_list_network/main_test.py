# file: main_test.py
import logging
import main as driver

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

TOKEN="89758e3ab391b309a9d2b18b02c2a2d"

def list(args):
     raise Exception('Not implemented yet')

def main():
    """test logic for when running this module as the primary one!"""

    # search test case
    #args = {'locus': 'AT2G38470'}
    #driver.search(args)

    # list test case - DON'T CALL THIS. Now it would kill the endpoint!!!
    args = {}
    driver.list(args)
    #search(args)
    #param_map = rb.build_param_map(args, TOKEN)
    #log.info("Param Map:")
    #log.info(param_map)


if __name__ == '__main__':
    main()
