import csv
import os


def _nest_dict_rec(k, v, out):
    k, *rest = k.split(": ", 1)
    if rest:
        _nest_dict_rec(rest[0], v, out.setdefault(k, {}))
    else:
        out[k] = v


p_dict = {}
t_dict = {}
with open('/Users/roneythomas/code/csc148/assignments/a2/cs1_papers.csv',
          mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if True:
            _nest_dict_rec(row["Category"],
                           {"Title": row["Title"],
                            "Citations": row[
                                "Citations"]}
                           , p_dict)

print(p_dict)
