import csv

genes = []
genes = []
f = open("HPA_subcell_location_Plasma_2087.txt")
reader = csv.reader(f)
for row in reader:
    genes.append(row[0].split()[0])
    
f = open('genes.txt', 'w')
f.write('\n'.join(genes))
f.close()

fml = {}
with open('diopt_results_2021-09-14 124826.csv') as f:
    reader = csv.reader(f)
    cur = 0
    for row in reader:
        cur += 1
        if cur == 1:
            continue
        if row[1] not in fml:
            fml[row[1]] = []
        fml[row[1]].append(row[8]) 
        fml[row[1]].sort()
        
for key in fml:
    fml[key] = ' '.join(fml[key])

with open('HPA_subcell_location_Plasma_2087.txt') as f:
    m = open('HPA_subcell_location_Plasma_with_orthologs.csv', 'w')
    writer = csv.writer(m)
    reader = csv.reader(f, delimiter='\t')
    cur = 0
    for row in reader:
        cur += 1
        if cur == 1:
            writer.writerow(row[:1] + ['Fly Ortholog'] + row[1:]) 
            continue
        if row[0] not in fml:
            fml[row[0]] = ''
        writer.writerow(row[:1] + [fml[row[0]]] + row[1:]) 
        
    
