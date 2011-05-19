#!/usr/bin/python
import pycurl, types, SQLite, time, sys, re
import cStringIO as StringIO
sys.path.append("/home/ron/PythonBase")
import senAdd

class PyCurl:
    def __init__(self, urls, maxconn=20,
                 SQLdb=":memory:", SQLtbl="main", cache = 604800, opt="F"):
        #cache = how long do we cache the results, in seconds?  default = 7 day
        #cache = None, cache forever

        #opt = S(low), M(edium), F(ast).  Faster we go: more potential errors
        opt = { pycurl.FOLLOWLOCATION: 1,
                pycurl.CONNECTTIMEOUT: {"S":120, "M":60, "F":30}[opt],
                pycurl.TIMEOUT: {"S":300, "M":120, "F":45}[opt],
                pycurl.NOSIGNAL: 1 }
        
        #idea type: [[key, url] ... ]
        if type(urls)==types.StringType:
            urls = [[0, urls]]
        elif type(urls)==types.ListType:
            if type(urls[0])!=types.ListType:
                urls = [[i,x] for i,x in enumerate(urls)]
        
        self.maxconn = maxconn
        self.opt = opt
        self.list = []

        self.SQLtbl = SQLtbl
        self.sql = SQLite.SQLite(SQLdb, tbl=SQLtbl)
        self.sql.c.execute("CREATE TABLE IF NOT EXISTS {tbl} (key, url, html TEXT, created REAL)".format(tbl=SQLtbl))
        self.sql.index(["key"], unique=True)
        self.sql.index(["key", "created"])
        self.sql.index(["url"])

        okUrl = []
        cTime = time.time()
        for x in urls:
            if self.sql.c.execute("SELECT count(*) FROM {tbl} WHERE key=?".format(tbl=SQLtbl), (x[0],)).fetchone()[0] == 0:
                okUrl.append(x)
            elif cache!=None:
                if self.sql.c.execute("SELECT count(*) FROM {tbl} WHERE key=? and created>?".format(tbl=SQLtbl), (x[0], cTime-cache)).fetchone()[0] == 0:
                    okUrl.append(x)
        if len(okUrl)>0:
            self.__init_curl(okUrl, maxconn)
            self.new = True
        else:
            self.new = False

    def __setopt(self, c):
        for x in self.opt:
            c.setopt(x, self.opt[x])
        return c

    def __init_curl(self, urls, maxconn=20):
        total = len(urls)
        num_conn = min(total, maxconn)
        m = pycurl.CurlMulti()
        m.handles = []
        for i in range(num_conn):
            c = pycurl.Curl()
            c.html = None
            c = self.__setopt(c)
            m.handles.append(c)

        freelist = m.handles[:]
        num_processed = 0
        while num_processed < total:
            while urls and freelist:
                c = freelist.pop()
                c.k, c.url = urls.pop(0)
                c.html = StringIO.StringIO()
                c.setopt(pycurl.URL, c.url)
                c.setopt(pycurl.WRITEFUNCTION, c.html.write)
                m.add_handle(c)
 
            while 1:
                ret, num_handles = m.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break

            while 1:
                num, ok, err = m.info_read()
                for c in ok:

                    if len(re.findall("Error [#]2012", c.html.getvalue()))>0:
                        print " | Patent Errored Out Bro!"
                        return
                    
                    self.sql.c.execute("INSERT OR REPLACE INTO {tbl} (key, url, html, created) VALUES (?, ?, ?, ?)".format(tbl=self.SQLtbl), (c.k, c.url, senAdd.uni2asc(c.html.getvalue()), time.time()))
                    c.html.close()
                    c.html = None
                    m.remove_handle(c)
                    freelist.append(c)
##                for c in err:
##                    try:
##                        print "  > error: {key}, {url}".format(key=c.k, url=c.url)
##                    except:
##                        print "  > error"
                    
                sys.stdout.write("{clear}  - {x}".format(clear="\b"*20, x=num_processed))
                num_processed = num_processed + len(ok) + len(err)
                if num_processed % 800 == 0 and num_processed > 0:
                    self.sql.conn.commit()
                if num == 0:
                    break

        for c in m.handles:
            if c.html is not None:
                c.html.close()
                c.html = None
            c.close()
        m.close()
        self.sql.conn.commit()
        print ""

#p = PyCurl("www.google.com", maxconn=100)
