import math, urllib, urllib2, sys, re
sys.path.append("/home/ron/PythonBase")
import PyCurl, SQLite, senGraph

class PattyParse:
    def __init__(self, query, key=None, category="grant", fetch=False, patentGrab=False, db = "usptoPat.s3"):
        self.tbl  = "{category}_search".format(category=category)
        self.tbl2 = "{category}_list".format(category=category)
        self.db = db
        self.query = query
        self.category = category
        self.maxconn = 40
        self.patentGrab = patentGrab
        if fetch:
            self.fetch()

    def fetch(self):
        tbl = self.tbl
        tbl2 = self.tbl2
        db = self.db
        query = self.query
        category = self.category
        maxconn = self.maxconn
        #FIRST PATENT
        if category=="grant":
            base = "patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=/netahtml/PTO/search-adv.htm&r=0&f=S&l=50&d=PTXT"
            params = urllib.urlencode({"p":1, "Query":query})
        url = "http://{base}&{params}".format(base=base, params=params)
        
        firstkey = "{query}||{page}".format(query=query, page=1)
        PyCurl.PyCurl([[firstkey, url]], maxconn=maxconn, SQLdb=db, SQLtbl=tbl, opt="M")
        self.s = SQLite.SQLite(db=db, tbl=tbl)

        #SUBSEQUENT PATENT
        html = self.grab()
        pats = int(re.findall("<B>Results of Search.*?</B>: ([0-9]+) patents", html)[0])
        pages = int(math.ceil(float(pats)/50))
        print "Query: {query}\n  - Patents: {pats}, Pages: {pages}".format(query=query, pats=pats, pages=pages)

        urls = []
        Srch1 = re.findall('<INPUT TYPE="HIDDEN" NAME="Srch1" VALUE="(.*?)">', html)[0]
        for num in range(2, pages+1):
            params = urllib.urlencode({"Srch1":Srch1, "NextList{num}".format(num=num):"N"})
            urls.append(["{query}||{page}".format(query=query, page=num), "http://{base}&{params}".format(base=base, params=params)])

        if len(urls)>0:
            pc = PyCurl.PyCurl(urls, maxconn=maxconn, SQLdb=db, SQLtbl=tbl, opt="M")

            if pc.new or True:
                #BUILD PATENT LIST
                self.s.chgTbl(tbl2)
                self.s.c.execute("CREATE TABLE IF NOT EXISTS {tbl} (query TEXT, Patent VARCHAR(8), Title TEXT, UNIQUE(query, Patent))".format(tbl=tbl2))
                self.s.index(["Patent"])
                patUrl = []
                for num in range(0, pages):
                    html = self.grab(page=num+1)
                    base = re.findall("<TABLE><TR><TD>.*?</TABLE>", html, re.S)[0]
                    href = re.findall("<A  HREF=.*?>(.*?)</A>", base, re.S)
                    pats = []
                    for i in range(0, len(href), 2):
                         pat = [query, re.sub(",", "", href[i]), re.sub("  +", " ", re.sub("\n", "", href[i+1])).strip()]
                         pats.append(pat)
                         patUrl.append([pat[1], "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=1&f=G&l=50&d=PTXT&p=1&p=1&S1={patent}.PN.".format(patent=pat[1])])
                    self.s.c.executemany("INSERT OR IGNORE INTO {tbl} VALUES (?, ?, ?)".format(tbl=tbl2), pats)
                self.s.conn.commit()

                if self.patentGrab:
                    PyCurl.PyCurl(patUrl, maxconn=maxconn, SQLdb=db, SQLtbl="patent_search", opt="M", cache=None).new
                

    def grab(self, page=1):
        query = self.query
        category = self.category
        tbl = "{category}_search".format(category=category)
        key = "{query}||{page}".format(query=query, page=page)
        self.s.chgTbl(tbl)
        html = self.s.c.execute("SELECT html FROM {tbl} WHERE key=?".format(tbl=tbl), (key,)).fetchone()
        return html[0]

    def cleanup(self, category=None):
        if category==None:
            category = self.category
        tbl = "{category}_search".format(category=category)
        cleanup = self.s.c.execute("SELECT count(*) FROM {tbl} WHERE html LIKE 'Error #2012%'".format(tbl=tbl)).fetchone()
        if cleanup[0]>0:
            print "Clean up required ", cleanup[0]
            self.s.c.execute("DELETE FROM {tbl} WHERE html LIKE 'Error #2012%'".format(tbl=tbl))
            self.conn.commit()

    def pat_match(self):
    #Match a query against the Patent data
        query = self.query
        category = self.category
        tbl  = "{category}_list".format(category=category)

        self.t = SQLite.SQLite()
        self.t.attach(self.db)
        self.t.c.execute("""
            CREATE TABLE main AS
                SELECT Patent, Title FROM {tbl} WHERE query=?
            """.format(tbl=tbl), (query,)).fetchall()
        self.t.index(["Patent"])
        self.t.attach("/home/ron/disambig/sqlite/invpat.s3")
        self.t.c.execute("""
            CREATE TABLE invpat AS
                SELECT  a.*
                  FROM  db.invpat AS a
            INNER JOIN  main AS b
                    ON  a.Patent = b.Patent
                 WHERE  a.AppYearStr BETWEEN 1975 and 2001;
            """)
        #self.t.chgTbl("invpat")
        #self.t.csv_output()

    def network(self, InvNum):
        query = self.query
        category = self.category
        s = senGraph.senDBSQL()
        s.graph(vertex_list=s.nhood(InvNum), flag=InvNum, output="network.csv")
        sG = senGraph.senGraph(s.tab)
        sG.g.vs["size"] = [math.log(x)*3+4 for x in sG.g.vs["cnt"]]
        sG.vs_color("AsgNum", dbl=True)

        for x in InvNum:
            if x in sG.g.vs["Invnum_N"]:
                iG = sG.neighborhood([sG.g.vs["Invnum_N"].index(x)], 2)
                iG.g.vs["layout"] = iG.g.layout("FR")
                iG.json(output="%s.json" % x, vBool=["flag"], title="+2 degrees")
                
