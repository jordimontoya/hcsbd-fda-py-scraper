import os, sys
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count

def getAbsolutePath(relative_path):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        running_mode = 'Frozen/executable'
    else:
        try:
            script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
            application_path = os.path.dirname(script_dir)
            running_mode = "Non-interactive (e.g. 'python myapp.py')"
        except NameError:
            application_path = os.getcwd()
            running_mode = 'Interactive'
    
    os.makedirs(os.path.dirname(application_path), exist_ok=True)
    config_full_path = os.path.join(application_path, relative_path)

    print('Running mode:', running_mode)
    print('  Appliction path  :', application_path)
    print('  Config full path :', config_full_path)

    return os.path.join(application_path, relative_path)

def scrapBaseUrl(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    r = requests.get(url, headers=headers)
    r.raw.chunked = True
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'lxml')

def deleteSheet(wb, sheet_name):
    for sheet in wb.sheets:
        if sheet_name in sheet.name:
            sheet.delete()

# Returns excel columns' head as array
def getExcelHead(table, arr_head):
    thead = [e.text for e in table.find("thead").find_all("th")]
    return thead + arr_head

def excel_writer(func_name, worksheet, trs):   
    FILE_LINES = len(trs)
    NUM_WORKERS = cpu_count() * 2
    chunksize = FILE_LINES // NUM_WORKERS * 4
    pool = Pool(NUM_WORKERS)

    row = 1
    result_iter = pool.imap(func_name, trs)
    for result in result_iter:
        worksheet.write_row(row, 0, result)
        row += 1