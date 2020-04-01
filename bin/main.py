from dotenv import load_dotenv
import os
import sys
is_local = os.path.split(os.getcwd())[-1] == 'bin'

if is_local:
    print('!!!! local execution !!!!')
    from context import crawler_rent


if __name__ == '__main__':
    if is_local:
        load_dotenv('../.env')
        from crawler_rent import cli
        sys.exit(cli.main())

    else:
        load_dotenv('.env')
        from crawler_rent import cli
        sys.exit(cli.main())
