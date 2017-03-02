import xml.etree.ElementTree as ET
import yaml
import sys
import io
import os
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)


biblstruct = {
    # @type, text
    'idno': './teiHeader/fileDesc/sourceDesc/biblStruct/idno'
}

# in biblStruct
analytic = {
    # @born, @geogr, @sex
    'authors': './teiHeader/fileDesc/sourceDesc/biblStruct/analytic/author',
    'editors': './teiHeader/fileDesc/sourceDesc/biblStruct/analytic/editor',
    # /name, /resp (omit this in yaml version)
    'respstmt': './teiHeader/fileDesc/sourceDesc/biblStruct/analytic/respStmt',
    'title': './teiHeader/fileDesc/sourceDesc/biblStruct/analytic/title'
}

# in biblStruct
monogr = {
    # @born, @geogr, @sex
    'authors': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/author',
    # @born, @geogr, @sex
    'editors': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/editor',
    # @type (omit this in yaml version)
    'biblscope': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/biblScope',
    # @n
    'edition': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/edition',
    # /name, /resp (omit this in yaml version)
    'respstmt': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/respStmt',
    'title': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/title',
    # (omit this in yaml version)
    'note': './teiHeader/fileDesc/sourceDesc/biblStruct/note'
}

# in monogr
imprint = {
    # @born, @geogr, @sex
    'authors': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/imprint/author',
    'date': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/imprint/date',
    'publisher': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/imprint/publisher',
    'pubplace': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/imprint/pubPlace'
}


def node_text(root, path):
    n = root.find(path)
    if n is None:
        return ''
    if n.text is None:
        return ''
    return n.text

def node_attribute(root, path, attr):
    n = root.find(path)
    if n is None:
        return ''
    if attr not in n.attrib:
        return ''
    return n.attrib[attr]


def edition(root):
    edition_attr = node_attribute(root, monogr['edition'], 'n').strip()
    edition_text = node_text(root, monogr['edition']).strip()

    if edition_attr:
        if edition_text:
            return edition_attr + ', ' + edition_text
        return edition_attr
    if edition_text:
        return edition_text
    return ''

def authors(root, path, role):
    result = []

    for author in root.findall(path):
        res = {}
        if ('born' in author.attrib and author.attrib['born']):
            res['born'] = author.attrib['born']
        if ('geogr' in author.attrib and author.attrib['geogr']):
            res['geogr'] = author.attrib['geogr']
        if ('sex' in author.attrib and author.attrib['sex']):
            res['sex'] = author.attrib['sex']
        if (author.text):
            res['name'] = author.text.strip()
        if (res):
            res['role'] = role
            result = result + [res]

    return result


def convert(filename):
    parsed = ET.parse(filename)
    root = parsed.getroot()
    catref = root.find('./teiHeader/profileDesc/textClass/catRef').attrib['target']
    idno_type = node_attribute(root, biblstruct['idno'], 'type')
    idno_text = node_text(root, biblstruct['idno'])

    people = []
    for p in authors(root, monogr['authors'], 'author_monogr'):
        people = people + [p]
    for p in authors(root, analytic['authors'], 'author_analytic'):
        people = people + [p]
    for p in authors(root, monogr['editors'], 'editor_monogr'):
        people = people + [p]
    for p in authors(root, analytic['editors'], 'editor_analytic'):
        people = people + [p]
    for p in authors(root, imprint['authors'], 'author_imprint'):
        people = people + [p]

    title_analytic = node_text(root, analytic['title'])
    title_monogr = node_text(root, monogr['title'])
    # edition = node_attribute(root, monogr['edition'], 'n')
    ed = edition(root)

    publication_date = node_text(root, imprint['date'])
    publication_place = node_text(root, imprint['pubplace'])
    publisher = node_text(root, imprint['publisher'])

    result = {
        'id': root.attrib['id'],
        'idno': {
            'type': idno_type,
            'value': idno_text
        },
        'title_analytic': title_analytic,
        'title_monogr': title_monogr,
        'publication_date': publication_date,
        'publication_place': publication_place,
        'publisher': publisher,
        'edition': ed,
        'category': catref.split()[0],
        'topics': catref.split()[1:],
        'people': people
    }

    # if title_analytic:
    #     result['title_analytic'] = title_analytic
    # if title_monogr:
    #     result['title_monogr'] = title_monogr

    return result


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        filename_out = os.path.splitext(filename)[0] + ".yml"
        result = convert(filename)
        data = yaml.dump(result, default_flow_style=False)

        # print data.decode('unicode_escape')

        with io.open(filename_out, 'w', encoding='utf8') as f:
            try:
                f.write(data.decode('unicode_escape'))
                sys.stderr.write("DONE:\t" + filename + "\t" + filename_out + "\n")
            except UnicodeDecodeError, e:
                sys.stderr.write("ERROR:\t" + filename + "\t" + str(e) + "\n")
