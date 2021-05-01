import csv
import os
from flybase import FlyBase
import requests
import json

class SubCellular:
    subcellular = {}
    cache = []
    def __init__(self):
        flybase = FlyBase()
        os.chdir('Finalized Gene Data Sets (T1 and T4)')
        files = os.listdir()
        files.remove(".DS_Store")
        for _ in files:
            file = _[:-4].lower()
            x = file.find("match")
            if x != -1:
                sub = file[:x]
            else:
                sub = file
            with open(_) as f:
                fs = csv.reader(f)
                cur = 0
                for row in fs:
                    cur+=1
                    if cur == 1:
                        continue
                    else:
                        lol = flybase.get_id_from_name(row[1])
                        if lol in self.subcellular:
                            self.subcellular[lol].add(sub)
                        else:
                            self.subcellular[lol] = {sub}

        os.chdir("..")
        self.cache = os.listdir('cache')


    def download(self, x):
        response = requests.get(f"https://flybase.org/api/ribbon/go/cellular_component/{x}")
        data = response.json()
        with open(f'cache/{x}', 'w') as f:
            f.write(json.dumps(data))
            self.cache.append(x)


    def get_loc_from_flybase(self, x):
        if x not in self.cache:
            self.download(x)
        with open(f'cache/{x}') as f:
            data = json.loads(f.read())
        ontologyData = []
        slim_order = data['resultset']['result'][0]['slim_ids_order']
        termsObj = data['resultset']['result'][0]['ribbon']
        for id in range(len(slim_order)):
            termID = slim_order[id]
            ontologyData.append({
                'name': termsObj[termID]['name'],
                'descendant_terms': termsObj[termID]['descendant_terms'],
            })
        hullo = []
        for terms in ontologyData:
            if len(terms['descendant_terms']) > 0:
                hullo.append(terms['name'])
        return hullo

        
    def get_localization(self, x, flybase=True):
        if x not in self.subcellular:
            return None
        return self.get_loc_from_flybase(x)


if __name__ == '__main__':
    k = SubCellular()
    print(k.get_localization('FBgn0037218'))
    print(k.get_localization('FBgn0030011'))
