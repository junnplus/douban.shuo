import os
from urllib.parse import urlencode

from flask import Flask, session, redirect
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'secret key'
oauth = OAuth(app)

douban = oauth.remote_app(
    'douban',
    consumer_key=os.environ.get('DOUBAN_APPKEY'),
    consumer_secret=os.environ.get('DOUBAN_SECRET'),
    base_url='https://api.douban.com/',
    request_token_url=None,
    request_token_params={'scope': 'douban_basic_common,shuo_basic_r,shuo_basic_w'},
    access_token_url='https://www.douban.com/service/auth2/token',
    authorize_url='https://www.douban.com/service/auth2/auth',
    access_token_method='POST',
)


@app.route('/login/authorized')
def authorized():
    session['douban_oauthredir'] = os.environ.get('REDIRECT_URI')
    resp = douban.authorized_response()
    if resp is None:
        return redirect(os.environ.get('CALLBACK_URI'))
    return redirect('{0}?{1}'.format(os.environ.get('CALLBACK_URI'), urlencode(resp)))


if __name__ == '__main__':
    app.run(port=4040)
