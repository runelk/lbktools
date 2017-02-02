from peewee import MySQLDatabase, Model, CharField, IntegerField


class LBKText(Model):
    tid = CharField()
    title = CharField()
    collection = CharField()
    issnisbn = CharField()
    wordcount = IntegerField()
    version = CharField()
    category = CharField()
    publisher = CharField()
    pubdate = IntegerField()
    pubplace = CharField()
    corpus_date = CharField()
    translation = CharField()
    startpos = IntegerField()
    endpos = IntegerField()
    supcat = CharField()

    class Meta:
        database = db
        db_table = 'BOKMALtext'


class LBKAuthor(Model):
    a_id = IntegerField()
    firstname = CharField()
    lastname = CharField()
    authortype = CharField(db_column='type')
    sex = CharField()
    geogr = CharField()
    born = IntegerField()
    tid = CharField()
    name = CharField()
    in_collection = IntegerField()

    class Meta:
        database = db
        db_table = 'BOKMALauthor'


class LBKClass(Model):
    tid = CharField()
    textclass = CharField(db_column='class')

    class Meta:
        database = db
        db_table = 'BOKMALclass'


def db_reset():
    pass


def xml2db():
    pass


def yaml2db():
    pass
