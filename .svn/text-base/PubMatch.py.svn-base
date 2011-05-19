import SQLite

class PubMatch:
    """
        PubMed names are Lastname, First (initials) OR Lastname-First
        Let's match this to the patent
    """
    def __init__(self, match="patent"):
        self.match = match
        files = {'patent': ['/home/ron/disambig/sqlite/invpat.sqlite3', 'invpat']}
        self.s = SQLite.SQLite(db=files[self.match][0], tbl=files[self.match][1])

    def close(self):
        self.s.close()

    def names(self, names, output="default.csv", debug=False):
        import csv
        nameList = []
        for i,x in enumerate(names):
            if x.find(", ") > -1:
                nameList.append([x.split(", "), x])
            elif x.find(" ") > -1:
                nameList.append([x.rsplit(" ", 1), x])
            elif x.find("-") > -1:
                nameList.append([x.replace("-", " ").rsplit(" ", 1), x])

        fullList = []
        for name in nameList:
            if debug:
                print name[1]
            res = self.s.c.execute("SELECT invnum_N, new_invnum_N, lastname, firstname, city, state, country, assignee FROM invpat WHERE lastname like '%s'" % (name[0][0],))
            res = [x for x in res]

            empty = True
            for result in res:
                if result[3] != "":
                    if "".join([x[0] for x in result[3].split(" ")])==name[0][1]:
                        cRec = [name[1]]
                        cRec.extend(result)
                        fullList.append(cRec)
                        empty = False
                        if debug:
                            print fullList[-1][1:]

            if empty and len(name[0][1])>1:
                for result in res:
                    if result[3] != "":
                        if "".join([x[0] for x in result[3].split(" ")])==name[0][1][0]:
                            cRec = [name[1]]
                            cRec.extend(result)
                            fullList.append(cRec)
                            empty = False
                            if debug:
                                print fullList[-1][1:]

        if output!=None:
            f = open(output, "wb")
            writer = csv.writer(f, lineterminator="\n")
            writer.writerows([['PubMed name', 'invnum_a', 'invnum_c', 'lastname', 'firstname', 'city', 'state', 'country', 'assignee']])
            writer.writerows(fullList)
            writer = None
            f = None
        else:
            return fullList
