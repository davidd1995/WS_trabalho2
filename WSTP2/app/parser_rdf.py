import csv



Entity = "http://www.student-mat.com/entity/"
Property = "http://www.student-mat.com/pred/"

triples = []

filename = "clean_data/" + input("Filename: ")
file_in = open(filename, 'r', encoding='utf-8')

reader = csv.reader(file_in)
for sub, pred, obj in reader:
    triples.append((sub, pred, obj))
file_in.close()

file_out = open('filent.nt', 'w')
for sub, pred, obj in triples:
    uri_sub = '<' + Entity + str(sub).lower().replace(' ', '_') + '>'
    uri_pred = '<' + Property + str(pred).lower().replace(' ', '_') + '>'
    obj_uri = '"' + obj + '"'
    file_out.write('{} {} {} .\n'.format(uri_sub, uri_pred, obj_uri))
file_out.close()
print("filent.nt created")
