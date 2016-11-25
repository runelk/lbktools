# LBKtools

A collection of tools for the
[LBK](http://www.hf.uio.no/iln/tjenester/kunnskap/samlinger/bokmal/veiledningkorpus/)
corpus.

Makes use of [Ruffus](http://www.ruffus.org.uk/) for handling
computation pipelines.

## Misc Notes

Ruffus keeps track of which files to ignore in an SQLite database:
`.ruffus_history.sqlite`. If you delete this, all tasks will be run on
all files regardless.
