from flask import render_template
from flask import redirect, render_template
from flask_oauthlib.client import OAuth
from flask import g, session, request, url_for, flash
from flask import jsonify
from tweetapp import app

oauth = OAuth(app)
twitter = oauth.remote_app(
    'twitter',
    consumer_key='9pprqTKg9cGrqQ8uZRtRH80Hu',
    consumer_secret='c5Ejd7RfVJbdK9JwnXZe3fAVrrSu7ua5qdVzY85jh0EftStIwr',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    print dir(twitter)
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    recent_tweets = []
    screen_name = session['twitter_oauth']['screen_name']
    me =  twitter.get('users/show.json?screen_name=%s' % screen_name)
        
    return render_template(
        'dashboard.html', data={
            'user_name': me.data['name'],
            'screen_name': screen_name,
            'profile_image_url': me.data['profile_image_url'],
            'recent_tweets': get_tweets()
        }
    )

def get_tweets():
    screen_name = session['twitter_oauth']['screen_name']
    all_tweets = twitter.get("statuses/user_timeline.json?screen_name=%s&count=10" % screen_name)
    return [tweet.get('text') or '' for tweet in all_tweets.data]
    

@app.route('/tweet', methods=['POST'])
def tweet():    
    status = request.form['tweet_text']

    if not status:
        return redirect(url_for('index'))

    resp = twitter.post('statuses/update.json', data={
        'status': status
    })
    
    if resp.status == 403:
        response = {"status": False, 'msg': 'Your tweet was too long.'}
    elif resp.status == 401:
        response = {"status": False, 'msg': 'Authorization error with Twitter.'}
    else:
        response = {"status": True, 'recent_tweets': get_tweets()}
    return jsonify(response)


@app.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('home'))
