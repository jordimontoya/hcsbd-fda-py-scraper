#!/usr/bin/env python
import xlsxwriter
import xlwings as xw
import utils.funcs as f
import utils.custom_funcs as cf
import cProfile

workbook = None
app = None

def listHeader(array):
    return [s.split("|")[0] for s in array]

def run_scraper():

    print('Scraping website... START')

    # Create a workbook and declare specific formats.
    wb = xlsxwriter.Workbook(f.getAbsolutePath(cf.OUTPUT_FILE_TMP), {'constant_memory': True})
    bold = wb.add_format({'bold': True})
    underline = wb.get_default_url_format()
    date = wb.add_format({'num_format': 'dd-mmm-yyyy'})
    merge_format = wb.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter'})
    merge_format_milestone = wb.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#828AE0'})
    merge_format_priority = wb.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#E0B4B4'})
    merge_format_screening = wb.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#999FE0'})
    merge_format_review = wb.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#95E0AA'})
        

    # HCSBD - Create worksheet and set link format and date format
    worksheetHCSBD = wb.add_worksheet('HCSBD')
    worksheetHCSBD.set_column('A:A', None, underline)
    worksheetHCSBD.set_column('D:D', None, date)
    worksheetHCSBD.set_column('E:E', None, date)
    worksheetHCSBD.set_column('F:F', None, date)
    worksheetHCSBD.set_column('G:G', None, date)
    worksheetHCSBD.set_column('H:H', None, date)
    worksheetHCSBD.set_column('I:I', None, date)
    worksheetHCSBD.set_column('J:J', None, date)
    worksheetHCSBD.set_column('K:K', None, date)
    worksheetHCSBD.set_column('L:L', None, date)
    worksheetHCSBD.set_column('M:M', None, date)
    worksheetHCSBD.set_column('N:N', None, date)
    worksheetHCSBD.set_column('O:O', None, date)
    worksheetHCSBD.set_column('P:P', None, date)
    worksheetHCSBD.set_column('Q:Q', None, date)
    worksheetHCSBD.set_column('R:R', None, date)
    worksheetHCSBD.set_column('S:S', None, date)
    worksheetHCSBD.set_column('T:T', None, date)
    worksheetHCSBD.set_column('U:U', None, date)
    worksheetHCSBD.set_column('V:V', None, date)
    worksheetHCSBD.set_column('W:W', None, date)
    worksheetHCSBD.set_column('X:X', None, date)
    worksheetHCSBD.set_column('Y:Y', None, date)
    worksheetHCSBD.set_column('Z:Z', None, date)
    worksheetHCSBD.set_column('AA:AA', None, date)
    worksheetHCSBD.set_column('AB:AB', None, date)
    worksheetHCSBD.set_column('AC:AC', None, date)
    worksheetHCSBD.set_column('AD:AD', None, date)

    # HCSBD - Scraps table
    response = f.api_get(cf.API_REST_HCSBD_LIST)["data"]

    # HCSBD - Builds and writes excel's header section
    worksheetHCSBD.merge_range('A1:D1', 'Data entries', merge_format)
    worksheetHCSBD.merge_range('E1:K1', 'Milestone submission', merge_format_milestone)
    worksheetHCSBD.merge_range('L1:S1', 'Request for priority status', merge_format_priority)
    worksheetHCSBD.merge_range('T1:AJ1', 'Screening 1', merge_format_screening)
    worksheetHCSBD.merge_range('AK1:CD1', 'Review 1', merge_format_review)
    worksheetHCSBD.merge_range('CE1:CT1', 'Screening 2', merge_format_screening)
    worksheetHCSBD.merge_range('CU1:EM1', 'Review 2', merge_format_review)
    worksheetHCSBD.merge_range('EN1:FD1', 'Screening 3', merge_format_screening)
    worksheetHCSBD.merge_range('FE1:GW1', 'Review 3', merge_format_review)

    # HCSBD - Builds and writes excel's subheader
    header_arr = cf.API_REST_KEYS_LIST + ["id"] + listHeader(cf.HCSBD_MILESTONE_SUBMISSION) + listHeader(cf.HCSBD_MILESTONE_REQUEST_FOR_PRIORITY_STATUS) + listHeader(cf.HCSBD_MILESTONE_SCREENING) + listHeader(cf.HCSBD_MILESTONE_REVIEW) + listHeader(cf.HCSBD_MILESTONE_SCREENING) + listHeader(cf.HCSBD_MILESTONE_REVIEW) + listHeader(cf.HCSBD_MILESTONE_SCREENING) + listHeader(cf.HCSBD_MILESTONE_REVIEW)
    worksheetHCSBD.write_row(1, 0, header_arr, bold)
    
    # HCSBD - Builds and writes data to excel
    f.excel_writer(cf.getExcelRow_HCSBD, worksheetHCSBD, response)

    #count = 0
    #for item in response:
    #    if count == 497:
    #        print(item)
    #    cf.getExcelRow_HCSBD(item)
    #    count = count+1
    
    # FDA - Create worksheet and set link format and date format
    worksheetFDA = wb.add_worksheet('FDA')
    worksheetFDA.set_column('A:A', None, underline)
    

    # CADTH - Scraps table
    #soup = f.scrapBaseUrl(cf.BASE_URL_CADTH + cf.PATH_CADTH)
    #table_cadth = soup.find("table", class_=cf.TABLE_CLASS_CADTH)

    # CADTH - Builds and writes excel's head
    #excel_head = f.getExcelHead(table_cadth, cf.THEAD_PRODUCT_CADTH)
    #worksheetFDA.write_row(0, 0, excel_head, bold)

    # CADTH - Builds and writes data to excel
    #trs = table_cadth.find_all("tr")
    #trs = trs[:10]
    #f.excel_writer(cf.getExcelRow_cadth, worksheetFDA, trs)

    # Close csv file
    wb.close()

    print('Scraping website... END')

def override_sheet(name, range):
    global workbook

    print('Copying data to excel file... START')

    sNamList = [sh.name for sh in workbook.sheets]
    if name not in sNamList:
        workbook.sheets.add(name)
    print(f.getAbsolutePath(cf.OUTPUT_FILE_TMP))
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

    override_sheet('HCSBD', 'A1:BZ5000')
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

    override_sheet('HCSBD', 'A1:AZ5000')
    override_sheet('FDA', 'A1:AZ5000')
    # Remove tmp file
    f.os.remove(f.getAbsolutePath(cf.OUTPUT_FILE_TMP))

    print('Scraper executed successfully! END')

if __name__ == "__main__":
    run_from_exe()