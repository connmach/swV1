from flask import Flask
import pathlib
import logging

project_dir = pathlib.Path(__file__).resolve().parent.parent
print("project dir" + str(project_dir))
web_dir = project_dir/'core'
template_dir = project_dir/'templates'
static_dir = '/var/www/coursePlatform/static'
config_file = project_dir/'config.py'
 
app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir ) 
app.config.from_pyfile(str(config_file))
logging.basicConfig(level=logging.DEBUG)

app.logger.info(f'-------------------------Login:LH {project_dir} ') 

#app.config.from_object(config_file)
app.secret_key = 'eduninja'
app.config['GITHUB_CLIENT_ID'] = 'Iv1.c1601169c882543e'
app.config['GITHUB_CLIENT_SECRET'] = 'c62c7fdc5c520b1d3c184ceb7bf783a09bfe504a'


print("configuration read")
#print(gradingURL)
import web.views 