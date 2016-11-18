
mtag = [
    "./vendor/mtag/mtag64",
    "-wxml"
]

cg3 = [
    "./vendor/vislcg3/vislcg3",
    "--codepage-grammar", "latin1",
    "--codepage-input", "utf-8",
    "--grammar", "./vendor/vislcg3/cg/bm_morf.cg",
    "--codepage-output", "utf-8",
    "--no-pass-origin"
]
stat = [
    "./vendor/OBT-Stat/bin/run_obt_stat.rb"
]

dep = []
