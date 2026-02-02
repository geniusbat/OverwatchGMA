import os, argparse,sys
import random, string

#Add root path to import usual_data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import usual_data


parser=argparse.ArgumentParser()
parser.add_argument('--test', help="Run website without gunicorn", action='store_true')
args=parser.parse_args()

if args.test:
    print("Running test")
    os.environ["OVGMA_DEBUG"] = str(usual_data.DEBUG)
    os.environ["OVGMA_DJANGO_SECRET"] = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    os.system("python manage.py runserver 0.0.0.0:{}".format(usual_data.API_PORT))
else:
    print("Running pseudo-prod")
    print("Remember that static files are not served and the db is possibly not migrated")
    os.system("python manage.py collectstatic")
    os.system("gunicorn web.wsgi --bind 0.0.0.0:{} --workers 2".format(usual_data.API_PORT))