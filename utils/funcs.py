import os, sys
import requests
import urllib.request
import json
import re
from io import StringIO, BytesIO
import string
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
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

def api_get(url):
    r = requests.get(url = url).text
    return json.loads(r)

def pdf_get(url):
    r = requests.get(url)
    return extract_text(BytesIO(r.content))

def extract_text_from_pdf_url(url, user_agent=None):
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)    

    if user_agent == None:
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'

    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(url, data=None, headers=headers)

    response = urllib.request.urlopen(request).read()
    fb = BytesIO(response)

    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    for page in PDFPage.get_pages(fb,
                                caching=True,
                                check_extractable=True):
        page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()

    # close open handles
    fb.close()
    converter.close()   
    fake_file_handle.close()

    if text:
        # If document has instances of \xa0 replace them with spaces.
        # NOTE: \xa0 is non-breaking space in Latin1 (ISO 8859-1) & chr(160)
        text = text.replace(u'\xa0', u' ')

        return text

def deleteSheet(wb, sheet_name):
    for sheet in wb.sheets:
        if sheet_name in sheet.name:
            sheet.delete()

def removeHtmlTagsFromString(str):
    str = str.strip().replace("<br>", " ").replace("<br/>", " ")
    return re.sub('<[^<]+?>', '', str)

# Returns excel columns' head as array
def getExcelHead(table, arr_head):
    thead = [e.text.strip() for e in table.find("thead").find_all("th")]
    return thead + arr_head

def excel_writer(func_name, worksheet, trs, startRow):   
    FILE_LINES = len(trs)
    NUM_WORKERS = cpu_count() * 2
    chunksize = FILE_LINES // NUM_WORKERS * 4
    pool = Pool(NUM_WORKERS)

    row = startRow
    result_iter = pool.imap(func_name, trs)
    for result in result_iter:
        worksheet.write_row(row, 0, result)
        row += 1

def sheet_format_range(sheet, format, array):
    if array:
        for c1 in array:
            for c2 in string.ascii_uppercase:
                sheet.set_column(c1+c2 +":"+ c1+c2, None, format)