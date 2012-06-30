#/usr/bin/python
#coding=utf8

import argparse
import os
import string
import sqlite3
import sys


def new_table(table_name, filename='to-do.db'):
    '''Create a new table.'''
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    try:
        table_name = to_unicode(table_name)
        c.execute('''CREATE TABLE %s
                     (short description, details)''' % table_name)
    except sqlite3.OperationalError:
        pass


def remove_table(table_name, filename='to-do.db'):
    '''Remove a table.'''
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    if table_name == None:
        # Remove all categories.
        query = 'Permanently remove all data from the database (y/n)? '
        if raw_input(query) in 'yY' and query != '':
            os.remove(filename)
        sys.exit()
    table_name = to_unicode(table_name)
    try:
        c.execute('''DROP TABLE %s''' % table_name)
    except sqlite3.OperationalError as error:
        print 'Error: %s' % error


def add_data(data, table, filename='to-do.db'):
    '''Add data to a table.'''
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    head = to_unicode(data[0])
    tail = to_unicode(data[1])
    table = to_unicode(table)
    if head:
        if not tail:
            tail = ''
        c.execute('''INSERT INTO %s
                     VALUES (?, ?)''' % table, (head, tail))
    conn.commit()


def list_data(table, filename='to-do.db'):
    '''List all data.'''
    category_name = table
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    if table == None:
        # Get all category names.
        table = c.execute('''SELECT name FROM sqlite_master
                            WHERE type='table'
                            ORDER BY name''')
        for category in table:
            list_data(category[0])
    else:
        try:
            table = c.execute('''SELECT * FROM %s''' % table)
        except sqlite3.OperationalError:
            print 'The category "%s" does not exist.' % table
            sys.exit()
        print string.capitalize(category_name)
        for row in table:
            if row[0]:
                head = to_unicode(row[0])
                print '  - ' + string.capitalize(str(head))
                if row[1]:
                    tail = to_unicode(row[1])
                    print '    ' + string.capitalize(str(tail))
        print


def to_unicode(obj, encoding='utf-8'):
    '''Convert to unicode if required.'''
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


def merge(*args):
    '''Merge categories.'''
    pass


def main():
    # TODO Add a default action if no arguments are passed.
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', nargs='?', default=False,
                        help='''Add data to a category. If it doesn't exist it
                                will be created.''')
    parser.add_argument('-r', '--remove', nargs='?', default=False,
                        help='''Remove data from a category.''')
    parser.add_argument('-l', '--list', nargs='?', default=False,
                        help='''List all the data in the database for the
                                specified category.''') 
    parser.add_argument('-m', '--merge',
                        help='''Merge categories.''')
    args = parser.parse_args()

    # Create the database if it does not exist.
    if not os.path.isfile('to-do.db'):
        new_table('general')

    # Assign args.add to 'general' if -a was passed without a category name.
    if args.add == None:
        args.add = 'general'
    # Only executes if -a was passed (with or without a category name).
    if args.add:
        new_table(args.add)
        if args.add.isdigit():
            print 'Error: digits not allowed'
            sys.exit()
        task = raw_input('Enter a descriptive title for the task: ')
        if task:
            details = raw_input('Enter a detailed description: ')
        else:
            print 'You must enter a descriptive title for the task.'
            sys.exit()
        if not task:
            task = None
        if not details:
            details = None
        add_data([task, details], args.add)
    # Remove everything without an argument, otherwise the passed category.
    # Separate a list of categories with a comma.
    if args.remove != False:
        if args.remove != None:
            for category in args.remove.split(','):
                remove_table(category)
        else:
            remove_table(args.remove)
    # List everything without an argument, otherwise the passed category.
    if args.list != False:
        list_data(args.list)
    if args.merge:
        merge(args.merge)


if __name__ == '__main__':
    main()
