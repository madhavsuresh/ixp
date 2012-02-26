#!/usr/bin/env python
#list of servers, general location (city level or country level), google maps api grab city

import urllib
import re
import json
import sys
import os
import unicodedata

endpoint = 'http://www-wanmon.slac.stanford.edu/cgi-wrap/tulip-viz.cgi?target=v3vee.org'

class Tulip():
    _tulip_endpoint = 'http://www-wanmon.slac.stanford.edu/cgi-wrap/tulip-viz.cgi?target='
    _maps_endpoint = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&latlng='
    _server_header = ['city','country','ip','min_rtt','a_rtt','max_rtt','loss','type','teir','distance']

    #input host name, output coordinates and servers that were hit
    def getHostInfo(self,raw_data,name):
        #print name
        #f = open('log/' + name,'w')
        '''
        sock = urllib.urlopen(self._tulip_endpoint+name)
        raw_data = sock.read()
        f.write(raw_data)
        sock.close()
        f.close()
        '''
        if 'Unable to get 3 minimun rtt values'  in raw_data:
            print '%s :ERROR Unable to triangulate host' % (name)
            return None
        elif 'Error: ping timeout' in raw_data:
            print '%s:ERROR Ping timeout' % (name)
            return None
        elif len(raw_data) == 0:
            print '%s: ERROR empty file' %(name)
            return None
        

        location = self.getLocation(raw_data)
        if not location:
            print 'ERROR: Geoip not found'
            return None
        else:
            print 'Coordinates: %s, %s. Address: %s' % (location['coords'][0],location['coords'][1],location['address'])
        #servers = self.getServers(raw_data)
        #print servers

    # get in raw_data, return list of servers that were used to geolocate
    def getServers(self,raw_data):
        reg = re.compile(r'addRow\(([\w \',\.]+)\)')
        raw_list = reg.findall(raw_data)
        raw_list = [re.sub(r'\'','',string) for  string in raw_list]
        pretty_print = '\n'.join(raw_list)
        return  pretty_print
        #server_list = [server_string.split(',') for server_string in raw_list]
        #output = [dict(zip(self._server_header,server)) for server in server_list[1:]]

    #given raw data, returns coordinates and address of queried address
    def getLocation(self,raw_data):
        reg = re.compile(r'L\w+ through GEOIP is\s+?:\s+?(-?\d+\.?\d*)')
        coords = reg.findall(raw_data)

        if len(coords) == 0:
            return None

        maps = urllib.urlopen(self._maps_endpoint+coords[0] + ',' + coords[1])

        map_data = json.loads(maps.read())
        address_string = map_data['results'][0]['formatted_address']
        address_string = unicodedata.normalize('NFKD', address_string).encode('ascii','ignore')
        return {'coords':coords,'address':address_string}

if __name__ == '__main__':

    files = os.listdir('log')
    t = Tulip()

    for f in files:
        of = open('log/' + f,'r')
        raw_data = of.read()

        t.getHostInfo(raw_data,f)



