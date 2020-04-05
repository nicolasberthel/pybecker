import logging
import os
import time
import sqlite3

NUMBER_FILE = "centronic-stick.num"

_LOGGER = logging.getLogger(__name__)


class Database:

    def __init__(self):
        self.filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'centronic-stick.db')
        self.conn = sqlite3.connect(self.filename)
        self.check()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def check(self):
        # check if table already exist
        c = self.conn.cursor()
        check_table = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='unit'")
        if check_table.fetchone() is None:
            self.create()
            self.migrate()

    def migrate(self):
        try:
            # migrate the previous *.num file into its sqllite database
            self.old_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), NUMBER_FILE)
            if os.path.isfile(self.old_file):
                _LOGGER.info('Migrate previous *.num file...')
                with open(self.old_file, "r") as file:
                    number = int(file.read())
                    c = self.conn.cursor()
                    c.execute("UPDATE unit SET increment = ?, configured = ? WHERE code = ?", (number, 1, '1737b',))
                    self.conn.commit()
                    os.remove(self.old_file)
        except (sqlite3.Error, OSError):
            _LOGGER.error('Migration failed')
            self.conn.rollback()

    def create(self):
        # create the database table

        _LOGGER.info('Create database...')
        c = self.conn.cursor()
        c.execute('CREATE TABLE unit (code NVARCHAR(5), increment INTEGER(4), configured BIT, executed INTEGER, UNIQUE(code))')
        c.execute("INSERT INTO unit VALUES (?, ?, ?, ?)", ('1737b', 0, 0, 0,))
        c.execute("INSERT INTO unit VALUES (?, ?, ?, ?)", ('1737c', 0, 0, 0,))
        c.execute("INSERT INTO unit VALUES (?, ?, ?, ?)", ('1737d', 0, 0, 0,))
        c.execute("INSERT INTO unit VALUES (?, ?, ?, ?)", ('1737e', 0, 0, 0,))
        c.execute("INSERT INTO unit VALUES (?, ?, ?, ?)", ('1737f', 0, 0, 0,))

        self.conn.commit()

    def output(self):
        c = self.conn.cursor()
        res = c.execute('SELECT * FROM unit')
        _LOGGER.info('%-10s%-10s%-12s%-15s' % ('code', 'increment', 'configured', 'last run'))
        for line in res.fetchall():
            last_run = '(unknown)'

            if line[3] > 0:
                last_run = time.strftime('%Y-%m-%d %H:%M', time.localtime(line[3]))
            _LOGGER.info('%-10s%-10s%-12s%-15s' % (line[0], line[1], line[2], last_run))

    def get_unit(self, rowid):
        c = self.conn.cursor()
        res = c.execute("SELECT code, increment, configured FROM unit WHERE rowid = ?", (rowid,))
        result = res.fetchone()

        if result is not None:
            return list(result)

    def get_all_units(self):
        c = self.conn.cursor()
        res = c.execute('SELECT code, increment, configured FROM unit WHERE configured = 1 ORDER BY code ASC')
        result = []

        for row in res.fetchall():
            result.append(list(row))

        return result

    def set_unit(self, unit, test=False):
        c = self.conn.cursor()
        last_run = int(time.time())

        c.execute('UPDATE unit SET increment = ?, configured = ?, executed = ? WHERE code = ?',
                  (unit[1], unit[2], last_run, unit[0],))

        if test:
            self.conn.rollback()
            return

        self.conn.commit()
