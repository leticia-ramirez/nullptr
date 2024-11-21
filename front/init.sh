python3 -m venv .venv

. .venv/bin/activate

pip install Flask
pip install requests


#Dependencias necesarias para conectar a mysql desde flask.
pip install flask_sqlalchemy
pip install mysql-connector-python
#pip install mysqlclient