from ruffus import *
# import subprocess
import os

starting_files = [
    "testdata/AV03Un0201.txt",
    "testdata/AV03Un0202.txt",
    "testdata/AV03Un0210.txt"
]

@transform(starting_files, suffix(".txt"), ".mtag")
def run_mtag(input_file, output_file):
    os.system("./vendor/mtag/mtag64 -wxml < %s > %s" % (input_file, output_file))

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

@transform(second_task, suffix(".cg3"), ".third")
def third_task(input_file, output_file):
    ii = open(input_file)
    oo = open(output_file, "w")

pipeline_run(target_tasks=[third_task])
