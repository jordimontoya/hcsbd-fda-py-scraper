#!/usr/bin/env python
import xlsxwriter
import xlwings as xw
import utils.funcs as f
import utils.custom_funcs as cf
import cProfile

workbook = None
app = None

def run_scraper():

    print('Scraping website... START')

    # Create a workbook and declare specific formats.
    wb = xlsxwriter.Workbook(f.getAbsolutePath(cf.OUTPUT_FILE_TMP), {'constant_memory': True})
    bold = wb.add_format({'bold': True})
    underline = wb.get_default_url_format()
    date = wb.add_format({'num_format': 'dd-mmm-yyyy'})

    # HCSBD - Create worksheet and set link format and date format
    worksheetHCSBD = wb.add_worksheet('HCSBD')
    worksheetHCSBD.set_column('A:A', None, underline)
    #worksheetHCSBD.set_column('H:H', None, date)
    #worksheetHCSBD.set_column('I:I', None, date)

    # HCSBD - Scraps table
    r = f.scrapBaseUrl(cf.API_REST_HCSBD)
    data = r.json()

    # HCSBD - Builds and writes excel's head
    worksheetHCSBD.write_row(0, 0, cf.THEAD_PRODUCT_HCSBD, bold)

    # HCSBD - Builds and writes data to excel
    #data = data[:10]
    f.excel_writer(cf.getExcelRow_HCSBD, worksheetHCSBD, data)
    
    # FDA - Create worksheet and set link format and date format
    worksheetFDA = wb.add_worksheet('FDA')
    worksheetFDA.set_column('A:A', None, underline)
    worksheetFDA.set_column('F:F', None, date)
    worksheetFDA.set_column('G:G', None, date)
    worksheetFDA.set_column('M:M', None, date)
    worksheetFDA.set_column('P:P', None, date)
    worksheetFDA.set_column('Q:Q', None, date)
    worksheetFDA.set_column('R:R', None, date)
    worksheetFDA.set_column('U:U', None, date)
    worksheetFDA.set_column('V:V', None, date)
    worksheetFDA.set_column('W:W', None, date)
    worksheetFDA.set_column('X:X', None, date)
    worksheetFDA.set_column('Y:Y', None, date)
    worksheetFDA.set_column('Z:Z', None, date)
    worksheetFDA.set_column('AA:AA', None, date)

    # CADTH - Scraps table
    soup = f.scrapBaseUrl(cf.BASE_URL_CADTH + cf.PATH_CADTH)
    table_cadth = soup.find("table", class_=cf.TABLE_CLASS_CADTH)

    # CADTH - Builds and writes excel's head
    excel_head = f.getExcelHead(table_cadth, cf.THEAD_PRODUCT_CADTH)
    worksheetFDA.write_row(0, 0, excel_head, bold)

    # CADTH - Builds and writes data to excel
    trs = table_cadth.find_all("tr")
    #trs = trs[:10]
    f.excel_writer(cf.getExcelRow_cadth, worksheetFDA, trs)

    # Close csv file
    wb.close()

    print('Scraping website... END')

def override_sheet(name, range):
    global workbook

    print('Copying data to excel file... START')

    sNamList = [sh.name for sh in workbook.sheets]
    if name not in sNamList:
        workbook.sheets.add(name)

    source_wb = xw.books.open(f.getAbsolutePath(cf.OUTPUT_FILE_TMP))
    source_wb.sheets[name].range(range).copy(workbook.sheets[name].range(range))
    workbook.save()
    source_wb.close()

    print('Copying data to excel file... END')

def run_from_exe():
    global workbook

    print('Running mode: run_from_exe')

    # Start process
    run_scraper()

    # Initialize Excel instance
    app = xw.App(visible=False)

    # Open or create a workbook
    try:
        workbook = app.books.open(f.getAbsolutePath(cf.OUTPUT_FILE))
    except:
        workbook_create = xlsxwriter.Workbook(f.getAbsolutePath(cf.OUTPUT_FILE), {'constant_memory': True})
        workbook_create.add_worksheet('HCSBD')
        workbook_create.add_worksheet('FDA')
        workbook_create.close()
        workbook = app.books.open(f.getAbsolutePath(cf.OUTPUT_FILE))

    override_sheet('HCSBD', 'A1:AZ5000')
    override_sheet('FDA', 'A1:AZ5000')

    # Remove tmp file
    f.os.remove(f.getAbsolutePath(cf.OUTPUT_FILE_TMP))

    workbook.close()
    app.quit()

    print('Scraper executed successfully! END')

def run_from_xlsb():
    global workbook

    print('Running mode: run_from_xlsb... START')

    # Current workbook and sheets
    workbook = xw.Book.caller()
    
    run_scraper()

    override_sheet('CADTH', 'A1:AZ5000')
    override_sheet('pCPA', 'A1:AZ5000')
    # Remove tmp file
    f.os.remove(f.getAbsolutePath(cf.OUTPUT_FILE_TMP))

    print('Scraper executed successfully! END')

if __name__ == "__main__":
    run_from_exe()