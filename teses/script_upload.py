import os
import json
import django

# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teses.settings")

# Initialize Django
#django.setup()


#from teses.models import Orientador

file_name = 'tfcs_22.json'

app_directory = os.path.dirname(__file__)
json_file_path = os.path.join(app_directory, file_name)



with open(json_file_path) as f:
    tfcs = json.load(f)['tfcs']

orientadores = set()
for tfc in tfcs:
    orientadores.add(tfc['orientador'])

print(orientadores)