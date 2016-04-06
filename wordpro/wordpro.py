import cgi
from google.appengine.api import users
import webapp2
from google.appengine.api import memcache
from google.appengine.api import mail

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/sign" method="post">
      <div><br><br>
        Which car would like: 
       <select name="car">
        <option value="volvo">Volvo</option>
        <option value="subaru">Subaru</option>
        <option value="mercedes">Mercedes</option>
        <option value="audi">Audi</option>
        </select><br>
        Enter your comments about this car<br>
      <textarea name="content" rows="3" cols="60"></textarea>
      </div>
      <div><input type="submit" value="Post comment"></div>
    </form>
  </body>
</html>
"""

class Indexpage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
            self.response.out.write('<html><body>%s</body></html>' % greeting)
            self.response.write(MAIN_PAGE_HTML)

        else:
            greeting = ('Welcome to Survey about cars <br> <a href="%s">Sign in with your google account</a>.' %
                        users.create_login_url('/'))
            self.response.out.write('<html><body>%s</body></html>' % greeting)
        

class Homepage(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
    	count = memcache.get('count')
        countv = memcache.get('countv')
        counts = memcache.get('counts')
        countm = memcache.get('countm')
        counta = memcache.get('counta')
        countvv = 0
        countss = 0
        countmm = 0
        countaa = 0
        car_info = cgi.escape(self.request.get('car'))
        car_info =  car_info.strip()
        greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                    (user.nickname(), users.create_logout_url('/')))
        self.response.out.write('<html><body>%s</body></html>' % greeting)


        self.response.write('</pre></body></html>')
        self.response.write(MAIN_PAGE_HTML)
        self.response.write('<html><body><br><br><u>Current Comment:</u><pre>')
        input_data = cgi.escape(self.request.get('content'))
        self.response.write(input_data)
        if (count== None):
        	memcache.set('count',1)
        else:
        	memcache.set('count',count+1)

        if (countv== None):
            memcache.set('countv',1)
        elif (car_info=='volvo'):
            memcache.set('countv',countv+1)

        if (counts== None):
            memcache.set('counts',1)
        elif (car_info=='subaru'):
            memcache.set('counts',counts+1)

        if (countm== None):
            memcache.set('countm',1)
        elif (car_info=='mercedes'):
            memcache.set('countm',countm+1)

        if (counta== None):
            memcache.set('counta',1)
        elif (car_info=='audi'):
            memcache.set('counta',counta+1)

        mem_key = 'comment'+str(count)
        memcache.set(mem_key,input_data)
        self.response.write('<h4> <u>Analysis of previous user opinion:</u> ')
        self.response.write('<br><h4> Total Comments till now : ')
        self.response.write(count)
        self.response.write('<br> percentage of user selection: ')

        #percentage calculation
        if(countv!=None):
            countvv = float(countv) / float((countv+counts+countm+counta))
            countvv = float(countvv) * 100
            countss = float(counts) / float((countv+counts+countm+counta))
            countss = float(countss) * 100
            countmm = float(countm) / float((countv+counts+countm+counta))
            countmm = float(countmm) * 100
            countaa = float(counta) / float((countv+counts+countm+counta))
            countaa = float(countaa) * 100
        self.response.write("<br>volvo :")
        self.response.write(countvv)
        self.response.write("<br>subaru :")
        self.response.write(countss)
        self.response.write("<br>mercedes :")
        self.response.write(countmm)
        self.response.write("<br>audi :")
        self.response.write(countaa)
        self.response.write('</h4><br>')
        i=0
        self.response.write('<h5>')
        if(count == None):
            self.response.write('<br>Previous comment : ')
            self.response.write(input_data)
            mem_key = 'comment0'
            memcache.set(mem_key,input_data)

        while i < count:
        	info = memcache.get('comment'+str(i))
        	self.response.write('<br>Previous comment : ')
        	self.response.write(info)
        	i = i+1

        self.response.write('</h5>')

app = webapp2.WSGIApplication([
    ('/', Indexpage),
    ('/sign', Homepage),
], debug=True)