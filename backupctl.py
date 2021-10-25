#!/bin/python3

import sys
import os
import datetime
import shutil
import getopt
import csv

from_path    = ""
to_path      = ""
format_      = "gztar"
journal_file = "journal.csv"
archive_file = ""
date_time    = datetime.datetime.now()

def usage():
    print("\nNAME\n\n",
          "\tbackupctl.py\n\n",
          "SYNOPSIS\n\n",
          "\t nbackupctl.py [options] parametrs\n\n",
          "DESCRIPTION\n\n",
          "\t Архивирует каталог.\n\n",
          "OPTIONS\n\n",
          "\t-h,\t--help\n",
          "\t\t\tВызов этой справочной информации.\n\n",
          "\t-j journal.csv,\t--journal journal.csv\n",
          "\t\t\tУказать в какой файл сохранять журнал.\n\t\t\tjournal.csv - путь до файла журнала.\n\t\t\tПо умолчанию сохраняет в текущей директории, в файл journal.csv\n\n",
          "\t-f format,\t-a format,\t--archive format,\t--format format\n",
          "\t\t\tУстановить формат создаваемого архива.\n",
          "\t\t\tgztar - .tar.gz (по умолчанию)\n"
          "\t\t\tzip - .zip\n",
          "\t\t\ttar - .tar\n",
          "\t\t\tbztar - .tar.bz2\n",
          "\t\t\txztar - .tar.xz\n\n",
          "PARAMETRS\n\n",
          "\t-d directory,\t--directory directory\n",
          "\t\t\tКаталог который необходми заархивировать.\n\n",
          "\t-o directory,\t--output directory\n",
          "\t\t\tКаталог в который положить архив.", sep="")

def journal(status = 'fail'):
    if os.path.isfile(journal_file):
        mode_wa = 'a'
    else:
        mode_wa = 'w'
    with open(journal_file, mode=mode_wa) as csv_file:
        fieldnames = ['backup_directory', 'file_archive', 'date_time', 'status']
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        if mode_wa == 'w':
            writer.writeheader()
        writer.writerow(
            {   'backup_directory': from_path, 
                'file_archive': archive_file, 
                'date_time':date_time.strftime("%d.%m.%Y %H:%M:%S"), 
                'status': status})

def get_name_arhiv():
    file_name = os.path.basename(from_path)
    file_name = file_name + datetime.datetime.now().strftime("_%Y-%m-%d_%H:%M:%S")
    return file_name

def make_archive():
    try:
        global to_path, from_path
        to_path =  os.path.abspath(to_path)
        from_path = os.path.abspath(from_path)
        name = os.path.join(to_path, get_name_arhiv())
        return shutil.make_archive(os.path.join(to_path, name), format_, from_path, to_path)
    except Exception as e:
        usage()
        journal()
        raise(e)
        #sys.exit(1)

def get_opts():
    try:
        opts, args = getopt.getopt(
                         sys.argv[1:], 
                         "hs:d:o:a:j:f:", 
                         ['help', 'directory=', 'output=',  'archive=', 'journal=', 'format=',]
                         )
    except Exception as e:
        usage()
        journal()
        raise(e)
        #sys.exit(1)

    flags={}
    for key, value in opts:
        flags[key] = value
    return flags

def check_opts(opts):
    global from_path, to_path, format_, journal_file
    if '-h' in opts.keys() or '--help' in opts.keys():
        usage()
        sys.exit(0)

    if '-d' in opts.keys() or '--directory' in opts.keys():
        from_path = opts.get('-d') if '-d' in opts.keys() else opts.get('--directory')
    else:
        usage()
        journal()
        sys.exit(1)

    if '-o' in opts.keys() or '--output' in opts.keys():
        to_path = opts.get('-o') if '-o' in opts.keys() else opts.get('--output')
    else:
        usage()
        journal()
        sys.exit(1)

    if '-a' in opts.keys() or '--archive' in opts.keys():
        format_ = opts.get('-a') if '-a' in opts.keys() else opts.get('--archive')
    elif '-f' in opts.keys() or '--format' in opts.keys():
        format_ = opts.get('-f') if '-f' in opts.keys() else opts.get('--format')

    if '-j' in opts.keys() or '--journal' in opts.keys():
        journal_file = opts.get('-j') if '-j' in opts.keys() else opts.get('--journal')




opts = get_opts()
check_opts(opts)
archive_file = make_archive()
print(archive_file)
journal("success")
