import xml.etree.ElementTree as ET
import yaml
import sys

biblstruct = {
    # @type, text
    'idno': './teiHeader/fileDesc/sourceDesc/biblStruct/idno'
}

# in biblStruct
analytic = {
    # @born, @geogr, @sex
    'authors': './teiHeader/fileDesc/sourceDesc/biblStruct/analytic/author',
    'editors': './teiHeader/fileDesc/sourceDesc/biblStruct/analytic/editor',
    # /name, /resp
    'respstmt': './teiHeader/fileDesc/sourceDesc/biblStruct/analytic/respStmt',
    'title': './teiHeader/fileDesc/sourceDesc/biblStruct/analytic/title'
}

# in biblStruct
monogr = {
    # @born, @geogr, @sex
    'authors': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/author',
    # @born, @geogr, @sex
    'editors': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/editor',
    # @type
    'biblscope': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/biblScope',
    # @n
    'edition': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/edition',
    # /name, /resp
    'respstmt': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/respStmt',
    'title': './teiHeader/fileDesc/sourceDesc/biblStruct/monogr/title',
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

def node_text(root, path):
    n = root.find(path)
    if n is None:
        return ''
    return n.text


def convert(filename):
    parsed = ET.parse(filename)
    root = parsed.getroot()
    catref = root.find('./teiHeader/profileDesc/textClass/catRef').attrib['target']

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

    result = {
        'id': root.attrib['id'],
        'category': catref.split()[0],
        'topics': catref.split()[1:],
        'people': people
    }

    if title_analytic:
        result['title_analytic'] = title_analytic
    if title_monogr:
        result['title_monogr'] = title_monogr

    return result


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print filename
        result = convert(filename)
        print yaml.dump(result, default_flow_style=False)
