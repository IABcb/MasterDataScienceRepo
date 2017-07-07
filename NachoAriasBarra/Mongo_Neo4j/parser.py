#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import json
import io, os

def iterate_tree(context, prefix):
    collaborations = [u'inproceedings', u'incollection', u'article']
    # xml categories
    author_array = []
    title = ''

    # read chunk line by line
    # we focus author and title
    counter = 0
    for _, elem in context:
        record = {}
        record["author"] = []
        if elem.tag == 'author':
            author_array.append(elem.text)

        if elem.tag == 'title':
            if elem.text:
                title = elem.text

        if elem.tag == 'journal' or elem.tag == 'booktitle':
            if elem.text:
                container = elem.text

        if elem.tag == 'year':
            if elem.text:
                year = elem.text

        if elem.tag in collaborations:
            if len(author_array) is not 0 and title is not '':
                # rejected paper has no author or title
                # it should be checked
                record["title"] = title
                record["author"] = [author for author in author_array]
                record["id"] = elem.get("key")
                record["year"] = int(year)
                record["type"] = elem.tag
                record_json = json.dumps(record,
                                         sort_keys=True,
                                         ensure_ascii=False)

                file_name = '{0}-{1:02d}.json'.format(prefix, counter)
                try:
                    stats = os.stat(file_name)
                    file_size = stats.st_size
                except FileNotFoundError :
                    file_size = 0
                if file_size > 104857600 :
                    counter += 1
                    file_name = '{0}{1:02d}.json'.format(prefix, counter)
                write_element(record_json, file_name)

                title = ''
                del author_array[:]

        elem.clear()
        while elem.getprevious() is not None:
            try :
                del elem.getparent()[0]
            except TypeError:
                break
    del context

def write_element (elem, file_output):
    print ('.')
    with io.open(file_output, 'a', encoding='utf8') as outfile:
        outfile.write(to_unicode(elem))
        outfile.write(u"\n")

if __name__ == "__main__":
    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str
    json_file_prefix = "dblp"
    input_files = ['dblp.0.xml', 'dblp.1.xml', 'dblp.2.xml']
    for input_file in input_files :
        context = etree.iterparse(input_file, load_dtd=True, html=True)
        # To use iterparse, we don't need to read all of xml.
        iterate_tree(context, json_file_prefix)
    print ('Finished')