import csv
import ftplib
import os
import pickle

from ncl import settings


def pickle_load(filepath) -> None:
    with open(filepath, mode='rb') as f:
        data = pickle.load(f)
    return data


def pickle_dump(dumpdata, filepath: str) -> None:
    with open(filepath, mode='wb') as f:
        pickle.dump(dumpdata, f)
        f.flush()


def extract_category(path):
    basename = os.path.basename(path)
    category, _ = os.path.splitext(basename)
    return category


def find_and_load_ftp_files():
    ftp = ftplib.FTP()
    ftp.encoding = 'utf-8'
    ftp.connect(settings.FTP_SERVER, 21)
    ftp.login(settings.FTP_USER, settings.FTP_PASS)
    find_result = set()
    for cat in settings.CATEGORIES:
        category_path = '{0}/{1}'.format(settings.FTP_NEWS_DIR, cat)

        def find_ftp(line):
            filename = line.split(' ')[-1]
            filepath = '{0}/{1}'.format(category_path, filename)
            find_result.add(filepath)

        lscmd = 'LIST {}'.format(category_path)
        ftp.retrlines(lscmd, find_ftp)

    all_chunks = {}
    for path in find_result:
        retrcmd = 'RETR {}'.format(path)
        byte_list = bytearray()
        ftp.retrbinary(retrcmd, byte_list.extend)
        lines = byte_list.decode('utf-8').split('\n')
        chunk = []
        for line in csv.reader(lines):
            if len(line) != 4:
                continue
            line_dic = {'category': line[0],
                        'title': line[1],
                        'manuscript_len': line[2],
                        'manuscript': line[3]}
            chunk.append(line_dic)
        basename = os.path.basename(path)
        name, ext = os.path.splitext(basename)
        all_chunks[name] = chunk
    ftp.quit()
    print(len(all_chunks))
    return all_chunks


def find_and_load_news():
    all_paths = []
    for cat in settings.CATEGORIES:
        # if time is not None:
        #    timestr = time.strftime('%Y-%m-%d')
        #    regex = './data/csv/{1}/*_{2}.csv'.format(cat, timestr)
        # all_paths += glob.glob(regex)
        print(all_paths)
    all_chunks = []
    for path in all_paths:
        with open(path, 'r') as f:
            chunk = []
            for line in csv.reader(f):
                line_dic = {'category': line[0],
                            'title': line[1],
                            'manuscript_len': line[2],
                            'manuscript': line[3]}
                chunk.append(line_dic)
        all_chunks += chunk
    return all_chunks
