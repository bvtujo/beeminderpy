import urllib
import urllib.request as urllib2
import settings
import json
import sys


# based on https://www.beeminder.com/api
class Beeminder:
  def __init__(self, this_auth_token):
    self._auth_token=this_auth_token
    self.base_url='https://www.beeminder.com/api/v1'

  def get_user(self,username):
    url = "%s/users/%s.json" % (self.base_url,username)
    values = {'auth_token':self._auth_token}
    result = self.call_api(url,values,'GET')
    return result

  def get_goal(self,username,goalname):
    url = "%s/users/%s/goals/%s.json" % (self.base_url,username,goalname)
    values = {'auth_token':self._auth_token}
    result = self.call_api(url,values,'GET')
    return result

  def get_datapoints(self,username,goalname):
    url = self.base_url+'users/'+username+'/goals/'+goalname+'/datapoints.json'
    url = "%s/users/%s/goals/%s/datapoints.json" % (self.base_url,username,goalname)
    values = {'auth_token':self._auth_token}
    result = self.call_api(url,values,'GET')
    return result

  def create_datapoint(self,username,goalname,timestamp,value,comment=' ',sendmail='false'):
    url = self.base_url+'users/'+username+'/goals/'+goalname+'/datapoints.json'
    url = "%s/users/%s/goals/%s/datapoints.json" % (self.base_url,username,goalname)
    values = {'auth_token':self._auth_token, 'timestamp':timestamp, 'value':value, 'comment':comment, 'sendmail':sendmail}
    result = self.call_api(url,values,'POST')
    return result

  def call_api(self,url,values,method='GET'):
    result=''
    data = urllib.parse.urlencode(values)
    if method=='POST':
      req = urllib2.Request(url,data.encode())
      response = urllib2.urlopen(req)
    else:
      response = urllib2.urlopen(url+'?'+data)
    result=response.read()
    return result


class User(Beeminder):
  def __init__(self, username=settings.BEEMINDER_USERNAME,
              this_auth_token=settings.BEEMINDER_AUTH_TOKEN):
    self.user = username
    Beeminder.__init__(self, this_auth_token)
    ud = Beeminder.get_user(self, username)
    ud = json.loads(ud)
    self._goals = ud['goals']

  def add_datapoint(self, goal, data, timestamp=None, comment='', sendmail='false'):
    if goal not in self._goals:
      print("Goal not found in available goals.")
      return -1
    else:
      res = Beeminder.create_datapoint(self, username=self.username, )
      return res