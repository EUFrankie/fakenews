from application import create_app
from flask_migrate import Manager, MigrateCommand

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)

"""
    the commands are
    flask db migrate
    flask db upgrade
    flask db stamp head
    
    => if the migrate doesn't work at the start
    then do 
    flask db stamp head
    flask db migrate
    flask db upgrade
    flask db stamp head
    
"""