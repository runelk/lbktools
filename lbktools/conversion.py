import json
import re
import codecs

def load_config(filename):
    with open(filename) as f:
        return json.load(f)


def make_column_dict(config, extra=[u'word', u'lemma']):
    return {
        item[1]:item[0]
        for item in enumerate(extra + config['columns'])
    }


def convert_attribute(tag, config):
    if tag.strip() in config['conversions']:
        return config['conversions'][tag]
    return { u'none': tag }


def parse_attributes(line, config):
    spl = line.strip().split()
    lst = [spl[0].strip('"')] + spl[1:]
    cnv = [{ 'lemma': lst[0] }] + [convert_attribute(item, config) for item in lst[1:]]
    return cnv


def make_row(word, attributes, column_dict):
    row = [None] * len(column_dict)
    row[0] = word
    for attribute in attributes:
        for k, v in attribute.iteritems():
            if k != 'none':
                position = column_dict[k]
                row[position] = v
    return row


def parse_cg3(filename_in, filename_out, config):
    rx_word = re.compile("<word>(.*?)</word>")
    column_dict = make_column_dict(config)

    with codecs.open(filename_out, 'w', 'utf-8') as fout:
        with codecs.open(filename_in, 'r', 'utf-8') as fin:
            current_word = None

            for line in fin:

                # Empty line signifies sentence end
                if not line.strip():
                    fout.write("\n")

                # Extract attributes from lines beginning with TAB
                if line.startswith("\t"):
                    attributes = parse_attributes(line, config)
                    row = make_row(current_word, attributes, column_dict)
                    fout.write("\t".join([item if item else '' for item in row]) + "\n")
                    continue

                #################################################################
                # NB: We're ignoring lines that:
                #     - do not begin with TAB
                #     - do not contain a <word> tag
                # Remember to supply the -wxml argument to mtag for this to work
                #################################################################

                rx = rx_word.search(line.strip())
                if (rx):
                    current_word = rx.group(1)
