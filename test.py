from ruffus import *
# import subprocess
import os
import lbktools.conversion as c

starting_files = [
    "testdata/AV03Un0201.txt",
    "testdata/AV03Un0202.txt",
    "testdata/AV03Un0210.txt"
]

@transform(starting_files, suffix(".txt"), ".mtag")
def run_mtag(input_file, output_file):
    cmdstr = ' '.join([
        "./vendor/mtag/mtag64",
        "-wxml",
        "< %s" % input_file,
        "> %s" % output_file
    ])
    os.system(cmdstr)

@transform(run_mtag, suffix(".mtag"), ".cg3")
def run_cg3(input_file, output_file):
    cmdstr = ' '.join([
        "./vendor/vislcg3/vislcg3",
        "--codepage-grammar latin1",
        "--codepage-input utf-8",
        "--grammar ./vendor/vislcg3/cg/bm_morf.cg",
        "--codepage-output utf-8",
        "--no-pass-origin",
        "< %s" % input_file,
        "> %s" % output_file
    ])
    os.system(cmdstr)

@transform(run_cg3, suffix(".cg3"), ".stat")
def run_stat(input_file, output_file):
    cmdstr = ' '.join([
        "./vendor/OBT-Stat/bin/run_obt_stat.rb",
        "--input", input_file,
        "> %s" % output_file
    ])
    os.system(cmdstr)

@transform(run_stat, suffix(".stat"), ".tsv")
def run_tsv(input_file, output_file):
    config = c.load_config('./config/misc/no.json')
    c.parse_cg3(input_file, output_file, config)


pipeline_run(target_tasks=[run_tsv])
