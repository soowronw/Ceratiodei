from flask_login import login_required, logout_user
from flask_login import current_user, login_user
from app import appFlask, db
from flask import redirect, request, render_template, url_for
from app.models import Captured_data, Links, User
from app.forms import LoginForm
from app.p0fclient import P0f


def catch_ip(request, url):
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    referrer = request.headers.get("Referer")
    rule = url
    row = Captured_data(url=str(rule), ip=str(user_ip), ua=str(user_agent), referrer=str(referrer))
    db.session.add(row)
    db.session.commit()


try:
    adminroute = '/' + Links.query.filter_by(role=1).first().route
except:
    print("err")
    adminroute = '/' + 'admin'
adminrouteapi_change = adminroute + 'apichange'
adminrouteapi_delete = adminroute + 'apidelete'
adminrouteapi_add = adminroute + 'apiadd'
adminroute_logout = adminroute + 'logout'

adminroute_data = adminroute + 'data'
adminrouteapi_data_delete_row = adminroute_data + 'apidelete'
adminrouteapi_data_delete_all = adminroute_data + 'apideleteall'



@appFlask.route(adminroute, methods=['GET', 'POST'])
def admin():
    def getLinks():
        links = []
        rows = db.session.query(Links).filter(Links.role != 1).all()
        for row in rows:
            if row.route == '/':
                links.append({'id': row.id, 'route': row.route, 'link': row.link, 'status': 'disabled'})
            else:
                links.append({'id': row.id, 'route': row.route, 'link': row.link})
        print(links)
        return links

    form = LoginForm()
    if current_user.is_authenticated:
        return render_template('settings.html', links=getLinks(), adminrouteapi_change=adminrouteapi_change,
                               adminrouteapi_delete=adminrouteapi_delete, adminrouteapi_add=adminrouteapi_add,
                               adminroute=adminroute, adminroute_data=adminroute_data,
                               adminroute_logout=adminroute_logout)
    if request.method == 'POST':
        user = db.session.query(User).filter(User.username == form.username.data).first()
        form = LoginForm()
        if user and user.check_password(form.password.data):
            login_user(user)
            return render_template('settings.html', links=getLinks(), adminrouteapi_change=adminrouteapi_change,
                                   adminrouteapi_delete=adminrouteapi_delete, adminrouteapi_add=adminrouteapi_add,
                                   adminroute=adminroute, adminroute_data=adminroute_data,
                                   adminroute_logout=adminroute_logout)
    return render_template('login_new.html', form=form)


@appFlask.route(adminroute_data)
def show_data():
    def getData():
        data = []
        rows = db.session.query(Captured_data).all()
        for row in rows:
            data.append({'id': row.id, 'url': row.url, 'ip': str(row.ip), 'ua': row.ua, 'referrer': row.referrer,
                         'created': row.created})
        return data


    if current_user.is_authenticated:
        return render_template('data.html', data=getData(), adminroute=adminroute, adminroute_data=adminroute_data,
                               adminroute_logout=adminroute_logout,
                               adminrouteapi_data_delete_row=adminrouteapi_data_delete_row,
                               adminrouteapi_data_delete_all=adminrouteapi_data_delete_all)

    return redirect(url_for('admin'))


@appFlask.route(adminroute_logout)
def logout():
    logout_user()
    return redirect(url_for('admin'))


@appFlask.route('/')
def index():
    url = '/'
    catch_ip(request, url)
    link = db.session.query(Links.link).filter(Links.route == '/').scalar()
    try:
        # sudo p0f -i eth0 -s /home/support/Repo/cera/p0f.sock
        p0f_client = P0f("p0f.sock")
        p0f_info = p0f_client.get_info(request.remote_addr)
        print(p0f_info)
        print(p0f_info['magic'])
        print(p0f_info['status'])
        print(p0f_info['first_seen'])
        print(p0f_info['last_seen'])
        print(p0f_info['total_conn'])
        print(p0f_info['uptime_min'])
        print(p0f_info['up_mod_days'])
        print(p0f_info['last_nat'])
        print(p0f_info['last_chg'])
        print(p0f_info['distance'])
        print(p0f_info['bad_sw'])
        print(p0f_info['os_match_q'])
        print(p0f_info['os_name'].decode("utf-8"))
        print(p0f_info['os_flavor'].decode("utf-8"))
        print(p0f_info['http_name'].decode("utf-8"))
        print(p0f_info['http_flavor'].decode("utf-8"))
        print('LINK TYPE',p0f_info['link_type'].decode("utf-8"))
        print(p0f_info['language'].decode("utf-8"))
        print(p0f_info['uptime'])
        print(p0f_info['uptime_sec'])





    except Exception as e:
        print('Err p0f')
        print(e)

    return redirect(link, code=302)


@appFlask.route('/<url>')
def redir(url):
    catch_ip(request, url)
    link = db.session.query(Links.link).filter(Links.route == url).scalar()
    if link is None:
        link = db.session.query(Links.link).filter(Links.route == '/').scalar()
    return redirect(link, code=302)


@appFlask.route(adminrouteapi_change, methods=['POST'])
def change():
    if current_user.is_authenticated:
        id = request.form.get("id")
        route = request.form.get("route")
        link = request.form.get("link")
        try:
            row = db.session.query(Links).filter(Links.id == id).scalar()
            print(row)
            row.route = route
            row.link = link
            db.session.commit()
            return "ok"
        except Exception as e:
            print(e)
            return "error"


@appFlask.route(adminrouteapi_delete, methods=['POST'])
def delete():
    if current_user.is_authenticated:
        id = request.form.get("id")

        print(id)
        try:
            row = db.session.query(Links).filter(Links.id == id).scalar()
            if row.route == '/':
                return "error. main route"
            db.session.query(Links).filter(Links.id == id).delete()
            db.session.commit()
            return "ok"
        except Exception as e:
            print(e)
            return "error"


@appFlask.route(adminrouteapi_add, methods=['POST'])
def add():
    if current_user.is_authenticated:
        route = request.form.get("route")
        link = request.form.get("link")
        if (':' in route) or ('/' in route) or ('\\' in route):
            return "Invalid character in route"
        if not route and not link:
            return "Empty strings"
        route.replace(' ', '')
        try:
            row = Links(route=route, link=link)
            db.session.add(row)
            db.session.commit()
            return "ok"
        except Exception as e:
            print(e)
            return "error"


@appFlask.route(adminrouteapi_data_delete_row, methods=['POST'])
def data_delete_row():
    if current_user.is_authenticated:
        id = request.form.get("id")
        try:
            db.session.query(Captured_data).filter(Captured_data.id == id).delete()
            db.session.commit()
            return "ok"
        except Exception as e:
            print(e)
            return "error"

@appFlask.route(adminrouteapi_data_delete_all, methods=['POST'])
def data_delete_allrows():
    if current_user.is_authenticated:
        try:
            db.session.query(Captured_data).delete()
            db.session.commit()
            return "ok"
        except Exception as e:
            print(e)
            return "error"