from django.contrib.auth.views import login
import logging

# logger = logging.getLogger("cwm")

def copenLogin(request):
    response = login(request, redirect_field_name="redirect_url")
    # response = bratLogin(request, response)
    return response


def bratLogin(request, response, server_path="/var/www/html/brat/server/src", session_path="/var/www/html/brat/work/sessions/", user="guest"):
    import os
    if not os.path.isdir(server_path):
        raise Exception('Invalid server_path')
    if not os.path.isdir(session_path):
        raise Exception('Invalid session_path')
    os.sys.path.append(server_path)
    from session import SessionCookie, Session

    from hashlib import sha224
    from datetime import datetime, timedelta
    import pickle
    from ipware.ip import get_ip

    ip = get_ip(request)
    sid = sha224('%s-%s' % (ip, datetime.utcnow())).hexdigest()
    cookie = SessionCookie(sid)
    current_session = Session(cookie)
    current_session['user'] = user
    ppath = os.path.join(session_path, sid+'.pickle')
    with open(ppath, 'wb') as f:
        pickle.dump(current_session, f)
    try:
        os.chown(ppath, 1002, 1002)
    except Exception as ex:
        print (ex)
        # raise Exception('If you\'re using "RUNSERVER", do it with root!')
        raise Exception('If you are using "RUNSERVER", do it with root!')
    exp = (datetime.utcnow() + timedelta(30)).strftime('%a, %d %b %Y %H:%M:%S')
    response.set_cookie('sid', sid, path='/brat/', expires=exp)

    return response
                            
