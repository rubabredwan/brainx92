import csv

class FlyBase:
  annotation2name = {}
  annotation2id = {}
  id2name = {}
  name2id = {}
  def __init__(self):
    with open('fbgn_annotation_ID.tsv') as f:
      reader = csv.reader(f, delimiter='\t')
      cur = 0
      for row in reader:
        cur += 1
        if cur > 1:
          ids = row[2].split(",") + row[3].split(",")
          ann = row[4].split(",") + row[5].split(",")
          self.name2id[row[0]] = row[2]
          for _ in ann:
            self.annotation2name[_] = row[0]
            self.annotation2id[_] = row[2]
          for _ in ids:
            self.id2name[_] = row[0]


  def get_name_from_id(self, ID):
    if ID in self.id2name:
      return self.id2name[ID]

  def get_name_from_ann(self, ann):
    if ann in self.annotation2name:
      return self.annotation2name[ann]

  def get_id_from_ann(self, ann):
    if ann in self.annotation2id:
      return self.annotation2id[ann]

  def get_id_from_name(self, name):
    name = name.strip()
    if name in self.name2id:
      return self.name2id[name]

if __name__ == '__main__':
  main = FlyBase()
  print(main.get_name_from_id('FBgn0287621'))
  print(main.get_id_from_ann('CG13200'))

