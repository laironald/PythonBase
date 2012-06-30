""" 
 2012/06/28:
  * DB and TBL/TABLE variables represent DB and TBL options
  * Added underscore functions
  * Add a debug option?

"""

def MySQL_cfg(cfg=None, title=None):
    import os, getpass
    if title!=None:
        print title
    if cfg==None:
        cfg = {}
    if "host" not in cfg:
        cfg["host"] = raw_input("host: ")
    if "user" not in cfg:
        cfg["user"] = raw_input("user: ")
    if "passwd" not in cfg:
        cfg["passwd"] = getpass.getpass("passwd: ")
    if "db" not in cfg:
        cfg["db"] = raw_input("db: ")
    return cfg



class SQLite:
    """ 
    The following is a wrapper for sqlite3, a commonly used library for creating
    transportable relational databases
     * Syntax can be found @ http://www.sqlite.org
     * Python documentation can be found @ http://docs.python.org/library/sqlite3.html
     * Can pass db, tbl to most parameters with **kwargs
    """
    def __init__(self, path=":memory:", db=None, tbl="main", output=False):
        """ 
        Creates and opens a database connection for
        "path" and default the table to "tbl"

        Args:
          path: the location of the database
          db: the location of the database **legacy
          tbl: the name of the primary table
        Returns: Nothing
          Sets self variables such as tbl, path, c (cursor), conn (connect)
        """
        import sqlite3
        self.path = path
        if db:
            self.path = db
        self.tbl = tbl
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()
        self.output = output

    def __del__(self):
        """ 
        Destructor running similar to a Garbage Collector
        """
        self.close()

    #-------------------------------------HIDDEN METHODS

    def _getSelf(self, fields=None, **kwargs):
        """ 
        GETS basic SELF defined variables (ie. self.tbl)

        Args:
          fields: specified files to return
          **kwargs: keyword arguments related self. variables
        Return:
          returns variables in sequence provided
        *NOTE: self.__dict__ returns a list of 
               avaiable SELF defined variables
        """
        list = []
        alias = {"table": "tbl", "tbl": "table"}
        if not fields:
            fields = kwargs.keys()

        for key in sorted(fields):
            if key in alias and alias[key] in kwargs:
                value = kwargs[alias[key]]
            elif key not in kwargs:
                value = None
            else:
                value = kwargs[key]
            if not value:
                if key in self.__dict__:
                    value = self.__dict__[key]
                elif key in alias and alias[key] in self.__dict__:
                    value = self.__dict__[alias[key]]
            list.append(value)
        return list

    def _dbAdd(self, **kwargs):
        """ 
        IF db exists, db.tbl ELSE tbl
        """
        db, tbl = self._getSelf(fields=["db", "tbl"], **kwargs)
        str = ""
        if db:
            str += (db+".")
        str += tbl
        return str

    def _decode(self, list):
        """ 
        TODO: Is this necessary?  What does this really do?
        """
        try:
            return [x.decode("iso-8859-1") for x in list]
        except:
            return list

    def _sqlmasterScan(self, var, type, lookup=None, db=None, seq=None):
        """ 
        Returns a list of items that exist within the database.
        *since SQLite is not case sensitive, lowercases everything

        Arg
          var: field to return
          type: type in database such as table, index
          db: consider a specific database?
          lookup: are we considering a specific item?
          seq: returns a range of indexes for numbering purposes
        Returns:
          a list of names that exist within the database.
          unless lookup specified: true or false
        """
        self.c.execute(""" 
            SELECT {var} FROM {table} 
             WHERE type='{type}' ORDER BY {var}
            """.format(var=var, type=type,
              table=self._dbAdd(db=db, tbl="sqlite_master"))) #"""
        list = [x[0].lower() for x in self.c]
        if seq:
            import re
            nums = []
            for x in list:
                if x.find(seq)==0:
                    d = re.findall('[0-9]+$', x)
                    if not d:
                        nums.append(1)
                    else:
                        nums.append(int(d[-1]))
            if not nums:
                return [0, 0]
            else:
                return [min(nums), max(nums)]
        elif not lookup:
            return list
        else:
            return lookup.lower() in list

    #-------------------------------------BACKGROUND FX

    def close(self):
        """ 
        Initiates a final commit (assumption, we want to commit data)
        Closes the appropriate cursors and connections 
        *chosen not to TEST this method
        """
        self.commit()
        self.c.close()
        self.conn.close()

    def optimize(self):
        """ 
        Optimize based on guidance found on the following:
          http://web.utk.edu/~jplyon/sqlite/SQLite_optimization_FAQ.html
        *chosen not to TEST this method
        """
        self.c.executescript(""" 
            PRAGMA cache_size=2000000;
            PRAGMA synchronous=OFF;
            PRAGMA temp_store=2;
            """) #"""

    def chgTbl(self, tbl):
        """ 
        Allows a user to change their default table
        *chosen not to TEST this method
        """
        self.tbl = tbl

    def commit(self):
        """ 
        Alias to self.conn.commit()
        *chosen not to TEST this method
        """
        self.conn.commit()

    def vacuum(self):
        """ 
        Databases expand with records.  This command compresses them to their
        smallest states.
        *chosen not to TEST this method
        """
        self.c.execute("vacuum")
        self.commit()

    #-------------------------------------TABLE MANIPULATION

    def add(self, key, typ="", **kwargs):
        if not table:
            table = self.tbl
        if type(key).__name__ in ('tuple', 'list'):
            key = [key]
        for k in key:
            if not self.columns(lower=True, lookup=k, **kwargs):
                self.c.execute("""
                    ALTER TABLE {table} ADD COLUMN {col} {typ}
                    """.format(table=table, col=k, typ=typ)) #"""
    
    def drop(self, keys, table=None): #drop columns -- doesn't exist so lame!
        import types
        if not table:
            table = self.tbl
        if type(keys)!=types.ListType:
            keys = [keys]
        cols = ", ".join([x for x in self.columns(output=False) if x.lower() not in [y.lower() for y in keys]])
        self.c.executescript("""
            DROP TABLE IF EXISTS %s_backup;
            ALTER TABLE %s RENAME TO %s_backup;
            """ % (table, table, table)) #"""
        self.c.execute("CREATE TABLE %s (%s)" % (table, ", ".join([" ".join([x[1], x[2]]) for x in self.c.execute("PRAGMA TABLE_INFO(%s_backup)" % table) if x[1].lower() not in [y.lower() for y in keys]])))
        self.replicate(tableTo=table, table="%s_backup" % table)
        self.c.execute("INSERT INTO %s SELECT %s FROM %s_backup" % (table, cols, table))
        self.c.execute("DROP TABLE %s_backup" % (table))

    def delete(self, table=None): #delete table
        if not table:
            table = self.tbl
        self.c.execute("DROP TABLE IF EXISTS %s" % table)
        self.conn.commit()

    #-------------------------------------STATS LIKE

    def tables(self, lookup=None, db=None, seq=None):
        #returns a list of tables or existence of a table
        return self._sqlmasterScan(var="tbl_name", 
            type="table", lookup=lookup, db=db, seq=seq)

    def indexes(self, lookup=None, db=None, seq=None):
        #returns a list of indexes or existence of a index
        return self._sqlmasterScan(var="name", 
            type="index", lookup=lookup, db=db, seq=seq)

    #-------------------------------------REPORTS
       
    def columns(self, lower=False, lookup=None, **kwargs):
        """ 
        Basic report that showcases columns

        Args:
          lower: lowercase the column names
          lookup: find a column within the columns
        Return:
          returns a list of columns or existence of column
        """
        db, output, tbl = self._getSelf(
            fields=["db", "tbl", "output"], **kwargs)
        self.c.execute("PRAGMA %s" % (
           self._dbAdd(db=db, tbl="TABLE_INFO("+tbl+")")))
        list = []
        for row in self.c:
            if output and not lookup: print row
            if lower:
                list.append(row[1].lower())
            else:
                list.append(row[1])
        if lookup:
            return lookup in list
        else:
            return list

    def count(self, **kwargs):
        """ 
        Basic report with time and date

        Args:
          default is time stamp and count (if output on)
        Return:
          returns the number of records for the table
        """
        import datetime
        db, output, tbl = self._getSelf(
            fields=["db", "tbl", "output"], **kwargs)
        if self.tables(lookup=tbl, db=db):
            cnt = self.c.execute("SELECT count(*) FROM {table}".\
                format(table=self._dbAdd(db=db, tbl=tbl))).fetchone()[0]
        else:
            cnt = 0
        if output:
            print datetime.datetime.now(), cnt
        return cnt

    #-------------------------------------ANALYSIS

    def fetch(self, fields="*", random=False, 
              limit=None, iterator=False, **kwargs):
        """ 
        Replicates common function where you return an array of values
        associated with a SQLite table

        Args:
          field: specific fields?
          limit: return a specific length of items?
          random: return data in a random sequence?
        Return: This is based on the iterator. 
        """
        db, tbl = self._getSelf(fields=["db", "tbl"], **kwargs)
        if type(fields).__name__ in ("list", "tuple"):
            fields = ",".join(fields)
 
        query = ["SELECT", fields, "FROM", self._dbAdd(db=db, tbl=tbl)]
        if random:
            query.append("ORDER BY random()")
        if limit:
            query.extend(["LIMIT", str(limit)])
        query = " ".join(query)
        
        if not self.tables(lookup=tbl, db=db):
            return []
        elif iterator:
            return self.c.execute(query)
        else:
            return self.c.execute(query).fetchall()

    #-------------------------------------DATABASE MGMT

    def attach(self, db, name="db"):
        """ 
        Attaches the "db" database as "name"

        Args:
          db: path or SQLite of database to attach
            *if SQLite, defaults to its path
          name: the alias of the database

        *chosen not to TEST this method
        """
        if db.__class__.__name__ == 'SQLite':
            db = db.path
        self.detach(name=name)
        self.c.execute("ATTACH DATABASE '{db}' AS {name}".format(db=db, name=name))

    def detach(self, name="db"):
        """ 
        Detaches the database "name"
        *chosen not to TEST this method
        """
        try:
            self.c.execute("DETACH DATABASE {name}".format(name=name))
        except:
            pass

    #-------------------------------------INPUT

    def csvInput(self, path, iterator=False, **kwargs):
        """ 
        Takes a CSV like file and processes into a iterator or list

        Args:
          file: self evident
          iterator: return a list or return an iterator?
          **kwargs are mostly for the CSV parser
            http://docs.python.org/library/csv.html
            can do things like delimiter
        Return: This is based on the iterator. 
        """
        import csv
        file = open(path, "rb")
        if iterator:
            return csv.reader(file, **kwargs)
        else:
            return [x for x in csv.reader(file, **kwargs)]

    # STOPPED AT THIS POINT
        
    def addSQL(self, data, db=None, table=None, header=False, field=True, allVars=False, insert=""):
        """
        This serves three functions depending the type of data (flat CSV, pure data, existing table)
        If data is a link to a database -- load the data into CSV
        
         - If data = table name, use the data as a base
           - If table doesn't exist, replicate ELSE Insert
         - Else
           - If data = filename (CSV) ... Generate table using quickSQL (header toggle is for this one)
         - ElseIf data = data, sounds good...!
           - Insert data

        Field=True, defaults that field names must match 1-1
        allVars => Make all variables VARCHARS (IGNORE BUILDING TYPE)
        """
        import types, os
        if not table:
            table = self.tbl
        isFile = False

        strBool = (type(data)==types.StringType or type(data)==types.UnicodeType)

        if strBool and os.path.exists(data):
            data = self.csvInput(data)
            isFile = True
        if insert!="":
            insert = "OR %s" % insert

        if not isFile:
            if strBool and self.tables(db=db, lookup=data):
                if self.tables(db=db, lookup=table):
                    self.replicate(tableTo=table, table=data, db=db)
                if field:
                    fieldTo = set(self.columns(table=table, output=False, lower=True))
                    fieldFr = set(self.columns(table=data, db=db, output=False, lower=True))
                    colList = ", ".join(list(fieldTo & fieldFr))
                    self.c.execute("INSERT %s INTO %s (%s) SELECT %s FROM %s" % (insert, table, colList, colList, self._dbAdd(db=db, tbl=data)))
                else:
                    self.c.execute("INSERT %s INTO %s SELECT * FROM %s" % (insert, table, self._dbAdd(db=db, tbl=data)))

        #if file exists, use quickSQL..        
        elif self.tables(db=db, lookup=table):
            #self.quickSQL(data, table=table, header=header)
            self.c.executemany("INSERT %s INTO %s VALUES (%s)" % (insert, table, ", ".join(["?"]*len(data[0]))), data[int(header):])
        else:
            self.quickSQL(data, table=table, header=header, allVars=allVars)
            #need to make this so the variables are more flexible
        self.conn.commit()

    def quickSQL(self, data, table=None, override=False, header=False, allVars=False, typescan=50, typeList=[]):
        """
            allVars => Make all variables VARCHARS (IGNORE BUILDING TYPE)
        """
        import re, types
        if not table:
            table = self.tbl
        if override:
            self.c.execute("DROP TABLE IF EXISTS %s" % table)
        elif self.tables(db=None, lookup=table):
            return

        if header:
            headLst = []
            for x in data[0]:
                headLst.append(re.sub("[()!@#$%^&*'-]+", "", x).replace(" ", "_").replace("?", ""))
                if headLst[-1] in headLst[:-1]:
                    headLst[-1]+=str(headLst[:-1].count(headLst[-1])+1)
        tList = []
        for i,x in enumerate(data[1]):
            if str(typeList).upper().find("%s " % data[0][i].upper())<0:
                cType = {types.StringType:"VARCHAR", types.UnicodeType:"VARCHAR", types.IntType:"INTEGER", types.FloatType: "REAL", types.NoneType: "VARCHAR"}[type(x)]
                if type(typescan)==types.IntType and cType=="VARCHAR":
                    least = 2
                    ints = 1
                    for j in range(1, min(typescan+1, len(data))):
                        if type(data[j][i])==types.StringType or type(data[j][i])==types.UnicodeType:
                            if re.sub(r"[-,.]", "", data[j][i]).isdigit():
                                if len(re.findall(r"[.]", data[j][i]))==0:   pass
                                elif len(re.findall(r"[.]", data[j][i]))==1: ints = 0
                                else: least = 0; break
                            else: least = 0; break
                    cType = {0:"VARCHAR", 1:"INTEGER", 2:"REAL"}[max(least-ints, 0)]
                if header:
                    if allVars:
                        tList.append("%s" % (headLst[i],))
                    else:                    
                        tList.append("%s %s" % (headLst[i], cType))
                else:
                    if allVars:
                        tList.append("v%d" % (i,))
                    else:                    
                        tList.append("v%d %s" % (i, cType))
            else:
                tList.extend([y for y in typeList if y.upper().find("%s " % data[0][i].upper())==0])

        #print("CREATE TABLE IF NOT EXISTS %s (%s)" % (table, ", ".join(tList)))
        self.c.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (table, ", ".join(tList)))
        if header==False:
            self.c.executemany("INSERT INTO %s VALUES (%s)" % (table, ", ".join(["?"]*len(data[0]))), data)
        else:
            self.c.executemany("INSERT INTO %s VALUES (%s)" % (table, ", ".join(["?"]*len(data[0]))), data[1:])
        self.conn.commit()            

    def replicate(self, tableTo=None, table=None, db=None):
        """
        Replicates the basic structure of another table
        """
        import re
        #replicate the structure of a table
        if not table:
            table = self.tbl
        if db==None:
            if tableTo==None: #THIS ALLOWS US TO AUTOMATICALLY ADD TABLES
                tableTo = [(lambda x:len(x)>0 and int(x[0]) or 1)(re.findall('[0-9]+', x)) for x in self.tables() if x.find(table.lower())>=0]
                tableTo = len(tableTo)==0 and table or "%s%d" % (table, max(tableTo)+1)
        else:
            tableTo = table
        sqls = self.c.execute("SELECT sql, name, type FROM {table} WHERE tbl_name='{filter}';".\
            format(table=self._dbAdd(db=db, tbl="sqlite_master"), filter=table)).fetchall()

        idxC = 0
        idxA = self.baseIndex()
        idxR = self.indexes(seq='idx_idx')
        def cleanTbl(wrd):
            wrd = re.sub(re.compile('create table ["\']?%s["\']?' % table, re.I), 'create table %s' % tableTo, wrd)
            return wrd
        def cleanIdx(wrd, name, newname):
            wrd = re.sub(re.compile(' on ["\']?%s["\']?' % table, re.I), ' on %s' % tableTo, wrd)
            wrd = re.sub(re.compile('INDEX %s ON' % name, re.I), 'INDEX %s ON' % newname, wrd)
            return self.baseIndex(idx=wrd) not in idxA and wrd or "";
        for x in sqls:
            try:
                if x[2]=='table':
                    self.c.execute(cleanTbl(x[0]))
                elif 'index':
                    idxC+=1
                    if idxC>=idxR[0] and idxC<=idxR[1]:
                        idxC = idxR[1]+1
                    self.c.execute(cleanIdx(x[0], x[1], "idx_idx%d" % idxC))
            except:
                y=0
    def baseIndex(self, idx=None, db=None):
        """
        Boils down a Index to its most basic form.
        Throw in an idx (string) to process that specific SQL.
        """
        import re
        if idx==None:
            sqls = self.c.execute("SELECT sql FROM %s WHERE type='index';" % (self._dbAdd(db=db, tbl="sqlite_master"))).fetchall()
        else:
            sqls = [[idx,]]
        #simplify the list
        idxLst = [re.sub("  +", " ", re.sub(", ", ",", re.sub(re.compile('INDEX .*? ON', re.I), 'INDEX ON', x[0]))).lower() for x in sqls if x[0]!=None]
        #reorders the keys (so sequentiality matters!)
        idxLst = [re.sub("[(].*?[)]", "(%s)" % ",".join(sorted(re.findall("[(](.*?)[)]", x)[0].split(','))), x) for x in idxLst] 
        if idx==None:
            return idxLst
        else:
            return idxLst[0]
        
    def index(self, keys, index=None, table=None, db=None, unique=False, combo=False):
        """
        Hey Amy!  Look, documentation
        Index is for index name

        Indicates if Index is created with Index name or None
        """

        import itertools

        if combo:
            for x in xrange(len(keys)):
                for k in itertools.combinations(keys, x+1):
                    self.index(k, index, table, db, unique)
        
        import re
        if not table:
            table = self.tbl
        if index==None: 
            index = [(lambda x:len(x)>0 and int(x[0]) or 1)(re.findall('[0-9]+', x)) for x in self.indexes(db=db) if x.find('idx_idx')>=0]
            index = len(index)==0 and "idx_idx" or "idx_idx%d" % (max(index)+1)

        #only create indexes if its necessary!  (it doens't already exist)
        idxA = self.baseIndex()
        idxSQL = "CREATE %sINDEX %s ON %s (%s)" % (unique and "UNIQUE " or "", self._dbAdd(db=db, tbl=index), table, ",".join(keys))
        try:
            if self.baseIndex(idx=idxSQL, db=db) not in idxA:
                self.c.execute(idxSQL)
                return self._dbAdd(db=db, tbl=index)
            else:
                return None
        except:
            return None

    #----- MERGE -----#

    def merge(self, key, on, tableFrom, keyType=None, table=None, db=None):
        """
        Matches the on variables from two tables and updates the key values

        Example of usage: (its on the table perspective, so that's first)
        On and Keys take an iterable with values of string or list:

        ie.
        key = ["ed", ["eric", "amy"]]
        on = ["ron", ["ron1", "amy"]]
        keyType = ['VARCHAR', 'VARCHAR'] #if nothing will just be blanks

        All together:

        .add('ed', 'VARCHAR')
        .add('eric', 'VARCHAR')

        c.executemany("UPDATE table SET ed=?, eric=? WHERE ron=? AND ron1=?",
            c.execute("SELECT b.ed, b.amy, b.ron, b.amy
                         FROM table AS a INNER JOIN tableFrom AS b
                           ON a.ron=b.ron AND a.ron1=b.amy").fetchall())       
        """
        import types, datetime
        if not table:
            table = self.tbl
        key = [type(x)==types.StringType and [x,x] or x for x in key]
        on = [type(x)==types.StringType and [x,x] or x for x in on]

        for i,x in enumerate(key):
            self.add(x[0], keyType!=None and keyType[i] or "", table=table)

        def huggleMe(lst, idx=0, head="", tail="", inner=", "):
            return head+("%s%s%s" % (tail, inner, head)).join([x[idx] for x in lst])+tail

        idxT = self.index(keys=[x[0] for x in on], table=table)
        idxF = self.index(keys=[x[1] for x in on], table=tableFrom, db=db)

        self.c.executescript("""
            DROP TABLE IF EXISTS TblA;
            DROP TABLE IF EXISTS TblB;
            CREATE TEMPORARY TABLE TblA AS SELECT %s FROM %s GROUP BY %s;
            CREATE TEMPORARY TABLE TblB AS SELECT %s, %s FROM %s GROUP BY %s;
            """ % (huggleMe(on), table, huggleMe(on),
                   huggleMe(key, idx=1), huggleMe(on, idx=1), self._dbAdd(db=db, table=tableFrom), huggleMe(on, idx=1))) #"""
        self.index(keys=[x[0] for x in on], table="TblA", index='idx_temp_TblA')
        self.index(keys=[x[1] for x in on], table="TblB", index='idx_temp_TblB')
        
        sqlS = "UPDATE %s SET %s WHERE %s" % (table, huggleMe(key, tail="=?"), huggleMe(on, tail="=?", inner=" AND "))
        sqlV = "SELECT %s, %s FROM TblA AS a INNER JOIN TblB AS b ON %s" % (
            huggleMe(key, idx=1, head="b."), huggleMe(on, idx=1, head="b."),
            " AND ".join(["a."+"=b.".join(x) for x in on]))
        vals = self.c.execute(sqlV).fetchall()
        if len(vals)>0:
            self.c.executemany(sqlS, vals)

        #remove indices that we just temporarily created
        for x in [idxT, idxF]:
            if x!=None:
                self.c.execute("DROP INDEX %s" % x)
        
    #----- OUTPUTS -----#

    def csv_output(self, fname="default.csv", table=None):
        """
            Exports data into a CSV which is defaulted to "default.csv"
        """
        import unicodedata
        def asc(val):
            return [unicodedata.normalize('NFKD', unicode(x)).encode('ascii', 'ignore') for x in val]

        import csv
        if not table:
            table = self.tbl
        f = open(fname, "wb")
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows([self.columns(table, output=False)])
        writer.writerows([asc(x) for x in self.c.execute("SELECT * FROM %s" % table).fetchall()])
        writer = None
        f.close()

    def mysql_output(self, cfg={'host':'localhost', 'db':'RD'}, textList=[], intList=[], varList=[], tableTo=None, table=None, full=True):
        """
        Output table into MySQL database.
        Auto converts fields TEXT, VARCHAR, and [Blank] to VARCHAR(255)
        Add additional text field names by using the textList
            (useful for the incorrect fields) tableTo is the MySQL table
        Add additional integer field names by using the intList
        Add additional varList.  This allows you to specify whatever you want.
            Format: [["name", "format"]]
        
        Full = True (input data)
        """
        textList = [x.lower() for x in textList]
        intList = [x.lower() for x in intList]

        if varList!=[]:
            varList = zip(*varList)
            varList[0] = [x.lower() for x in varList[0]]
        cfg = MySQL_cfg(cfg)
        
        import MySQLdb, re, types, unicodedata, sys, datetime
        if not table:
            table = self.tbl
        if tableTo == None:
            tableTo = table
        def field(name, type):
            name = name.lower()
            type = type.lower()

            if varList!=[] and name in varList[0]:
                return varList[1][varList[0].index(name)]
            if name in textList:
                return "VARCHAR(64)";
            elif name in intList:
                return "INTEGER";
            elif type.find("varchar")>=0 or type=="text" or type=="":
                return "VARCHAR(64)";
            elif type.find("int")>=0:
                return "INTEGER";
            elif type.find("real")>=0:
                return "REAL";
            else:
                return type
        
        mconn = MySQLdb.connect(host=cfg['host'], user=cfg['user'], passwd=cfg['passwd'], db=cfg['db'])
        mc = mconn.cursor()
        #get column and types for fields
        cols = ["`%s` %s" % (x[1], field(x[1], x[2])) for x in self.c.execute("PRAGMA TABLE_INFO(%s)" % table)]
        sql = "CREATE TABLE %s (%s);" % (tableTo, ", ".join(cols))

        try:
            mc.execute(sql)
        except:
            y=0
        indexes = [x[0] for x in self.c.execute("SELECT sql FROM sqlite_master WHERE type='index' and tbl_name='%s'" % table)]

        for idx in indexes:
            if idx!=None:
                idx = idx.lower()
                idx = idx.replace('on %s (' % table.lower(),
                                  'on %s (' % tableTo)
                try:
                    #print idx
                    mc.execute(idx)
                except:
                    y=0
                    print "Error:", idx

        if full:
            self.c.execute("SELECT * FROM %s" % table)
            t0 = datetime.datetime.now()
            i = 0
            while True:
                i = i + 1
                val = self.c.fetchone()
                if not val:
                    break
                
                insert = [(type(x)==types.UnicodeType or type(x)==types.StringType) and
                          unicodedata.normalize('NFKD', unicode(x)).encode('ascii', 'ignore') or x for x in val]
                try:
                    mc.execute("INSERT IGNORE INTO %s VALUES (%s)" % (tableTo, ", ".join(["%s"]*len(cols))), insert)
                except:
                    print i,val
                sys.stdout.write("{clear}  - {x} {time}".format(clear="\b"*30, x=i, time=datetime.datetime.now()-t0))
            print ""

##            vals = [x for x in self.c.execute("SELECT * FROM %s" % table)]                
##            for i,val in enumerate(vals):
##                #this is done to normalize the data
##                insert = [(type(x)==types.UnicodeType or type(x)==types.StringType) and
##                          unicodedata.normalize('NFKD', unicode(x)).encode('ascii', 'ignore') or x for x in val]
##                try:
##                    mc.execute("INSERT IGNORE INTO %s VALUES (%s)" % (tableTo, ", ".join(["%s"]*len(cols))), insert)
##                except:
##                    print i+1,val
        
        mc.close()
        mconn.close()

    """
    EXPERIMENTAL FUNCTIONS
    """
    # IGRAPH / VISUALIZATION RELATED FUNCTIONS, very very preliminary

    def igraph(self, where, table=None,
                 vx="Invnum_N", ed="Patent", order="AppYear",
                 va=", Lastname||', '||Firstname AS Name, City||'-'||State||'-'||Country AS Loc, Assignee, AsgNum",
                 ea=", a.AppYear AS AppYear", eg=', a.AppYear'):
        import math, datetime, senGraph
        if not table:
            table = self.tbl
        tab = senGraph.senTab()
        self.c.executescript("""
            DROP TABLE IF EXISTS G0;
            DROP TABLE IF EXISTS vx0;
            DROP TABLE IF EXISTS ed0;
            CREATE TEMP TABLE G0 AS
                SELECT * FROM %s WHERE %s ORDER BY %s;
            CREATE INDEX G_id ON G0 (%s);
            CREATE INDEX G_ed ON G0 (%s, %s);
            CREATE TEMPORARY TABLE vx0 AS
                SELECT %s, count(*) AS Patents %s FROM G0
                 GROUP BY %s;
            CREATE INDEX vx_id ON vx0 (%s);
            CREATE TEMPORARY TABLE ed0 AS
                SELECT  a.%s, b.%s, a.%s AS hId, b.%s AS tId, count(*) AS Weight %s
                  FROM  G0 AS a INNER JOIN G0 AS b
                    ON  a.%s=b.%s AND a.%s<b.%s
              GROUP BY  a.%s, b.%s %s;
            """ % (table, where, order, ed, vx, ed, vx, va, vx, vx,
                   vx, vx, vx, vx, ea, ed, ed, vx, vx, vx, vx, eg))

        tab.vList = self.c.execute("SELECT * FROM vx0").fetchall()
        tab.vlst = self.columns(table="vx0", output=False)[1:]
        tab.eList = self.c.execute("SELECT * FROM ed0").fetchall()
        tab.elst = self.columns(table="ed0", output=False)[2:]
        s = senGraph.senGraph(tab, "vertex")
        return s        
