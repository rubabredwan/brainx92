import csv
import urllib.request
import gzip
import requests
import json
import re

class FlyBase:
  fbgn = {}
  annotation = {}
  symbol = {}

  def download_data(self):
    urllib.request.urlretrieve('http://ftp.flybase.net/releases/current/precomputed_files/genes/fbgn_annotation_ID.tsv.gz', '.fbgn_annotation_ID.tsv.gz')
    f = gzip.open('.fbgn_annotation_ID.tsv.gz', 'rt')
    return f

  def __init__(self):
    reader = csv.reader(self.download_data(), delimiter='\t')
    cur = 0
    for row in reader:
      if len(row) == 1:
        continue
      cur += 1
      if cur > 1:
        ids = row[2].split(",") + row[3].split(",")
        ann = row[4].split(",") + row[5].split(",")
        self.symbol[row[0]] = row[2]
        for _ in ann:
          self.annotation[_] = row[2]
        for _ in ids:
          self.fbgn[_] = row[0]


  def get_symbol(self, _):
    if _ in self.symbol:
      return _
    elif _ in self.fbgn:
      return self.fbgn[_]
    elif _ in self.annotation:
      return self.fbgn[self.annotation[_]]

  def get_fbgn(self, _):
    if _ in self.fbgn:
      return _
    elif _ in self.symbol:
      return self.symbol[_]
    elif _ in self.annotation:
      return self.annotation[_]

  def get_hitlist(self, fbgn) :
    r = requests.get(f'https://flybase.org/hitlist/{fbgn}/to/FBst')
    m = re.compile('var FlyBaseHitList = (.*}}});')
    data = json.loads(m.search(r.text).group(1))
    return data['ids']

  def get_stocks(self, symbol) :
    hitlist = self.get_hitlist(self.get_fbgn(symbol))
    data = {
      "ids": ','.join(hitlist)
    }
    r = requests.post("https://flybase.org/api/hitlist/fetch/", data=data)
    rs = json.loads(r.text)
    genes = []
    print(len(rs['resultset']['result']))
    for _ in rs['resultset']['result']:
      if _['collection'] != 'Bloomington Drosophila Stock Center':
        continue
      if _['genotype'].find('TRiP') == -1:
        continue
      genes.append({
        "stock": "https://bdsc.indiana.edu/stocks/" + _['stock_num'],
        "genotype": _['genotype'].replace('<sup>', '[').replace('</sup>', ']'),
        "flybase_id": _['id']
      })
    return genes

if __name__ == '__main__':
  main = FlyBase()
  print(main.get_fbgn('FBgn0287621'))
  print(main.get_symbol('FBgn0287621'))
  print(main.get_symbol('CG13200'))
  print(main.get_fbgn('CG13200'))
  print(main.get_stocks('FBgn0000490'))

