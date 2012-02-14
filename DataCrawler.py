class Crawler():
    
    '''
    classdocs
    '''

# Init the crawler with the name of the DB
    def __init__(self,dbname):
        from sqlite3 import dbapi2 as sqlite
        self.searchID = 1
        self.con= sqlite.connect(dbname)
        self.c = self.con.cursor()
        self.createindextables()
        self.search_limit = 10 # Limited to 10 pages per search
        pass
    
    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getentryid(self,table,field,value,createnew=True):
        ## Returns the ID of an entry, if it doesn't exist it is created
        cur = self.c.execute("select rowid from %s where %s = '%s'" % (table,field,value))
        res = cur.fetchone()
        
        if res==None:
            cur = self.c.execute("insert into %s (%s) values ('%s')" % (table,field,value))
            return cur.lastrowid
        else:
            return res[0]
        
        return None
    
    def addURLtoindex(self,url,search_term,page_num,searchID):
        self.c.execute("insert into searchInstance(URL,search_string,page_num,search_term) values ('%s','%s','%s','%s')" % (url,search_term,page_num,self.search_string))
        self.dbcommit()
        print "New page: %s" % url
        return 0
    
    def addtoindex(self,url,soup):
        
        ## Gets passed a url and stores it
        if self.isindexed(url):return
        print "Indexing %s" % url
        
        # Get the individual words
        text = self.gettextonly(soup)
        words = self.sepparatewords(text)
        
        # Get the URL id
        # Adds the URL to the db, returns the URL to associate the words with        
        urlid = self.getentryid('urllist', 'url', url) 
        
        # Link each word to this url
        for i in range(len(words)):
            word = words[i]
            if word in self.ignorewords:continue
            wordid =self.getentryid('wordlist', 'word', word)
            self.c.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid,wordid,i))
        
    def gettextonly(self,soup):
        v = soup.string
        if v==None:
            c= soup.contents
            resulttext =''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext +=subtext+'\n'
            return resulttext
        else:
            return v.strip()

    def sepparatewords(self,text):
        import re
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!='']
    
    def isindexed(self,url):
        u = self.c.execute("select * from searchInstance where URL='%s'" % url).fetchone()

        if u!=None:
            print "Indexed."
            return True
        else:
            print "Not indexed."
            return False
        
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass

    def testCrawl(self,page,search_string):
        from BeautifulSoup import *
        import urllib2 
        from urlparse import urljoin
        import re
        self.search_string = search_string
        start_url = page[0] 
        service = self.search_string
        mid_url = page[2]
        start_index = page[3]
        end_url = page[4]
        
        for i in range(0,self.search_limit):
            url = start_url+service+mid_url+str(start_index)+end_url
            if(self.isindexed(url)):
                print "URL as been indexed!"
                break
            else:
                print "Has not been indexed"
            try:
                c=urllib2.urlopen(url)
            except:
                print 'Could not open number %d for %s' % (start_index,service)
                return
            
            soup = BeautifulSoup(c)
            self.addURLtoindex(url,self.search_string,start_index,self.searchID)
            results = soup.findAll({'div':True},{"class":"listingInfoContainer"})
            imageResults = soup.findAll({'div':True},{"class":"logoAndDistanceContainer"})
            for j in range(0,len(results)):
                bus_name = re.findall("<span id=\"listing-name.*</span>",str(results[j]))
                if(len(bus_name)):
                    bus_name = re.findall(">.*</span>",bus_name[0])
                    bus_name = bus_name[0]
                    bus_name = bus_name[1:len(bus_name)-7]
                #    print bus_name
                else:
                    bus_name = "None"
                    
                bus_by_line = re.findall("<div class=\"textDesc paragraph\">.*</div>",str(results[j]))
                if (len(bus_by_line)):
                    bus_by_line = bus_by_line[0]
                    bus_by_line = re.findall(">.*</div>",bus_by_line)
                    bus_by_line = bus_by_line[0][1:len(bus_by_line[0])-6]
                #    print "Bus_by_line: "+bus_by_line
                else:
                    bus_by_line = "None"
                
                bus_desc = re.findall("<div class=\"enhancedTextDesc paragraph\">.*</div>",str(results[j]))
                if (len(bus_desc)):
                    bus_desc = bus_desc[0]
                    bus_desc = re.findall(">.*</div>",bus_desc)
                    bus_desc = bus_desc[0][1:len(bus_desc[0])-6]
                #    print "Bus_desc: "+bus_desc
                else:
                    bus_desc = "None"
                
                bus_phone = re.findall("<span preferredcontact=.*</span>",str(results[j]))
                if (len(bus_phone)):
                    bus_phone = bus_phone[0]
                    bus_phone = re.findall(">.*</span>",bus_phone)
                    bus_phone = bus_phone[0][1:len(bus_phone[0])-7]
                #    print "Bus_phone: "+bus_phone
                else:
                    bus_phone = "None"
                
                bus_address = re.findall("<span class=\"address\">.*</span>",str(results[j]))
                if (len(bus_address)):
                    bus_address = bus_address[0]
                    bus_address = re.findall(">.*</span>",bus_address)
                    bus_address = bus_address[0][1:len(bus_address[0])-7]
                #    print "Bus_address: "+bus_address
                else:
                    bus_address = "None"
                
                bus_website = re.findall(">www.*\.au",str(results[j]))
                if (len(bus_website)):
                    bus_website = bus_website[0][1:len(bus_website[0])]
                #    print "bus_website: "+bus_website
                else:
                #    print "Failed to find .com.au"
                    bus_website_com = re.findall(">www.*\.com",str(results[j]))
                    if(len(bus_website_com)):
                        bus_website = bus_website_com[0][1:len(bus_website_com[0])]
                    else:
                #        print "Failed to find .com"
                        bus_website = "None"
                imageUrl = re.findall("src=\".*\"",str(imageResults[j]))
                if(len(imageUrl)):
                    imageUrl = imageUrl[0]
                    imageUrl = imageUrl[5:len(imageUrl)-1]
                else:
                    imageUrl = "None"
                entry_id = self.getDBId()
                self.saveBusData(self.escapeInput(bus_name),self.escapeInput(bus_by_line),self.escapeInput(bus_address),self.escapeInput(bus_phone),self.escapeInput(bus_website),entry_id,self.escapeInput(bus_desc))
                self.saveURLAsBlob(imageUrl,entry_id)
                # End Result Loop
            #End URL Loop
            start_index = start_index +1
        # End function
        print "Finished after %d pages" % start_index
        return 0
       
    def saveBusData(self,bus_name,bus_by_line,bus_address,bus_phone,bus_website,entry_id,bus_desc):
        from datetime import *      
        now = datetime.now()
        modified = datetime.now()
        print "Saving %s" % bus_name
        query = "insert into business_data(business_name,businessbyline,businessdesc,address,phone,website,picture,search_id,DT_added,DT_modified,search_term) "
        query += "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (bus_name,bus_by_line,bus_desc,bus_address,bus_phone,bus_website,"Null",entry_id,str(now),str(modified),self.search_string)
        self.c.execute(query)
        self.dbcommit()
        return
    
    def saveURLAsBlob(self,image_url,entry_id):
        query = "insert into business_data_blobs(b_id,blob_data) values ('%s','%d')" % (image_url,int(entry_id))
        self.c.execute(query)
        self.dbcommit()
        return
    
    def getDBId(self):
        row_id = self.c.execute("select * from business_data").fetchall()
        row_id = len(row_id)
        #row_id = int(self.c.fetchall)+1
        return row_id
    
    def createindextables(self):
        self.c.execute('create table if not exists searchInstance(URL,search_string,page_num,search_term)')
        self.c.execute('create table if not exists business_data(business_name,businessbyline,businessdesc,address,phone,website,picture,search_id,DT_added,DT_modified,search_term)')
        self.c.execute('create table if not exists business_data_blobs(b_id,blob_data)')
        self.dbcommit()
    
    def escapeInput(self,input_string):
        #import xml.sax.saxutils as saxutils
        input_string = input_string.replace("'","&#39;")
        return input_string
     
    def unescapeInput(self,input_string):
        input_string = input_string.replace("&#39;","'")
        return input_string