from app import appFlask, db
from app.models import Links, User, generate_password_hash
import argparse
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-apn', '--adminpanel', default='admincera')
    parser.add_argument('-al', '--adminlogin', default='admin')
    parser.add_argument('-aps', '--adminpas', default='admin')
    namespace = parser.parse_args(sys.argv[1:])
    adminlink = Links.query.filter_by(role=1).first()
    adminlink.link = namespace.adminpanel
    adminlink.route = namespace.adminpanel
    loginpaslink = User.query.filter_by(role=1).first()
    loginpaslink.username = namespace.adminlogin
    loginpaslink.password_hash = generate_password_hash(namespace.adminpas)
    db.session.commit()
    appFlask.run(debug=True)
