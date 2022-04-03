# oss-backend
Getting Started
git clone https://github.com/OSS-team-org/oss-backend.git

Don't forget to create your virtual environment

cd oss-backend
pip install -r requirements.txt


Secondly, set your app's secret key as an environment variable. For example, add the following to .bashrc or .bash_profile.

export TULIX_SECRET='something-really-secret'

Before running shell commands, set the FLASK_APP and FLASK_DEBUG environment variables

export FLASK_APP=/path/to/autoapp.py
export FLASK_DEBUG=1 


Run the following commands to create your app's database tables and perform the initial migration

flask db init
flask db migrate
flask db upgrade

To run the web application use:
flask run --with-threads
