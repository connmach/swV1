import google.oauth2.credentials
import googleapiclient.discovery
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)
@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))

 
@app.route('/course/fb/login')
def fblogin():
 pass  
#  return facebook.authorize(callback=url_for('facebook_authorized',
  #      next=request.args.get('next') or request.referrer or None,
  #      _external=True))


@app.route('/course/fb/auth')
 
def facebook_auth_redirect(): 
 
    session['userid']= "test"
    session['user_info'] ="test"
    session['myCourses']='{"A01","A03" }' 

    status,result=fetchLHAll(session['userid'])
    app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))

    session['LH']= result
    out=session['LH']
    resDict=json.loads(out)
    app.logger.info('-------------------------Login:LH {0} // {1}'.format( type(out),type(resDict)))

    app.logger.info('*****Login:LH history from session****** status{0} result{1}'.format( status, result))

 
    session['Badge'] = "ninjaBeginner"
    session['LHHours'] ="30"
    session['Score'] = "2.0"
    session['LearningTrack'] = "Foundation"
    session['recentCourses']  =["cs001","cs003"]



    return redirect(url_for('homePage',userId=user_info['given_name']))





@app.route('/login_old')
def authentication():

   return render_template('index.html')

@app.route('/course/google/login') 
def googlelogin():
    gses  = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            redirect_uri=AUTH_REDIRECT_URI)
  
    uri, state = gses.authorization_url(AUTHORIZATION_URL)
    session[AUTH_STATE_KEY] = state
    app.logger.info('*******Auth state {0} {1}'.format(str(session[AUTH_STATE_KEY]),state))
    session.permanent = True

    return  redirect(uri, code=302)

@app.after_request
def set_response_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

def is_logged_in():
    return True if AUTH_TOKEN_KEY in session else False

def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens =  session[AUTH_TOKEN_KEY]
    
    return google.oauth2.credentials.Credentials(
                oauth2_tokens['access_token'],
                refresh_token=oauth2_tokens['refresh_token'],
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                token_uri=ACCESS_TOKEN_URI)
def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials)

    return oauth2_client.userinfo().get().execute()

@app.route('/course/google/auth')
 
def google_auth_redirect():
    req_state = request.args.get('state', default=None, type=None)
    app.logger.info('*******Auth state {0} '.format(req_state))
    session[AUTH_STATE_KEY]=req_state
   # if req_state !=  session[AUTH_STATE_KEY]:
   #      response =  make_response('Invalid state parameter', 401)
   #      return response
    
    gses = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state= session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = gses.fetch_access_token(
                        ACCESS_TOKEN_URI,            
                        authorization_response=request.url)

    session[AUTH_TOKEN_KEY] = oauth2_tokens
    user_info = get_user_info()
    session['userid']=user_info['given_name']
    session['user_info'] =user_info
    session['myCourses']='{"A01","A03" }' 

    status,result=fetchLHAll(session['userid'])
    app.logger.info('*****Login:LH history****** status{0} result{1}'.format( status, result))

    session['LH']= result
    out=session['LH']
    resDict=json.loads(out)
    app.logger.info('-------------------------Login:LH {0} // {1}'.format( type(out),type(resDict)))

    app.logger.info('*****Login:LH history from session****** status{0} result{1}'.format( status, result))

 
    session['Badge'] = "ninjaBeginner"
    session['LHHours'] ="30"
    session['Score'] = "2.0"
    session['LearningTrack'] = "Foundation"
    session['recentCourses']  =["cs001","cs003"]



    return redirect(url_for('homePage',userId=user_info['given_name']))

@app.route('/course/google/logout')
 
def glogout():
    flask.session.pop(AUTH_TOKEN_KEY, None)
    flask.session.pop(AUTH_STATE_KEY, None)

    return flask.redirect(BASE_URI, code=302)
