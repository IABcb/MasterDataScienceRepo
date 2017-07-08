import csv
from lxml import etree
from operator import itemgetter
from itertools import groupby
import time

xml = '../may/dblp.xml'
parser = etree.iterparse(source=xml, dtd_validation=True, load_dtd=True)

INTEREST_PUBS = ['article', 'incollection', 'inproceedings']
ALLOWED_FIELDS = ["pubtype", "mdate", "booktitle", 
                  "year", "url", "author", 
                  "title", "key", "ee"]
OUTPUT_CSV_FILE = 'dblp-output.csv'



def xml_entry_as_dict(name, key, mdate, elements):
    """
    Receives a xml entry from the dblp.xml database and retrieve a dict containing the ALLOWED_FIELDS
    :param name: The name attribute from the xml entry
    :param key: The key attribute from the xml entry
    :param mdate:  The mdate attribute from the xml entry
    :param elements: The attribute, value pairs from the xml entry
    :return: The xml entry as python dictionary
    """
    entry = {}
    entry['pubtype'] = name
    entry['mdate'] = mdate
    entry['key'] = key
    for k, g in groupby(elements, itemgetter(0)):
        if k in ALLOWED_FIELDS:
            groups = list(g)
            if len(groups) == 1:
                entry[k] = groups[0][1]
            else:
                entry[k] = ';'.join([v for k, v in groups])
    return entry


if __name__ == "__main__":
    t0 = time.time()
    lines = 0
    valid_lines = 0
    with open(OUTPUT_CSV_FILE, 'w') as f:
        csvwriter = csv.DictWriter(f, fieldnames=ALLOWED_FIELDS)
        csvwriter.writeheader()
        for _, elem in parser:
            lines = lines + 1
            if lines % 1000000 == 0:
                print("Processed {0} lines. {1} valid. Took {2:0.2f} secs".format(lines, valid_lines, time.time()-t0))

            if elem.tag in INTEREST_PUBS:
                valid_lines = valid_lines + 1
                
                key = elem.attrib['key']
                mdate = elem.attrib['mdate']
                elements = []
                for e in elem:
                    if e.tag == 'year':
                        text = int(e.text)
                    elif e.text:
                        text = e.text.replace('"',' ')
                    else:
                        continue
                    elements.append((e.tag, text))
                entry = xml_entry_as_dict(elem.tag, key, mdate, elements)
                csvwriter.writerow(entry)
            else:
                continue
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
    print("Finish. Total Lines:{0}. \
           Valid Lines:{1}. \
           Total Time: {2:0.2f} secs".format(lines, valid_lines, time.time()-t0))
