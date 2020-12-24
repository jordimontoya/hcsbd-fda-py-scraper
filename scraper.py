#!/usr/bin/env python
import xlsxwriter
import xlwings as xw
import utils.funcs as f
import utils.custom_funcs_hcsbd as cfhcsbd
import utils.custom_funcs_fda as cffda
import cProfile

workbook = None
app = None

def listHeader(array):
    return [s.split("|")[0] for s in array]

def run_scraper():

    print('Scraping website... START')

    # Create a workbook and declare specific formats.
    wb = xlsxwriter.Workbook(f.getAbsolutePath(cfhcsbd.OUTPUT_FILE_TMP), {'constant_memory': True})
    
    bold = wb.add_format({'bold': True})
    underline = wb.get_default_url_format()
    date = wb.add_format({'num_format': 'mm-dd-yyyy'})
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
    f.sheet_format_range(worksheetHCSBD, date, ["","A","B","C","D","E","F","G","H"])
    worksheetHCSBD.set_column('A:A', None, underline)

    # HCSBD - Builds and writes excel's header section
    worksheetHCSBD.merge_range('A1:D1', 'Data entries', merge_format)
    worksheetHCSBD.merge_range('E1:M1', 'Milestone submission', merge_format_milestone)
    worksheetHCSBD.merge_range('N1:V1', 'Request for priority status', merge_format_priority)
    worksheetHCSBD.merge_range('W1:AM1', 'Screening 1', merge_format_screening)
    worksheetHCSBD.merge_range('AN1:CH1', 'Review 1', merge_format_review)
    worksheetHCSBD.merge_range('CI1:CY1', 'Screening 2', merge_format_screening)
    worksheetHCSBD.merge_range('CZ1:ET1', 'Review 2', merge_format_review)
    worksheetHCSBD.merge_range('EU1:FK1', 'Screening 3', merge_format_screening)
    worksheetHCSBD.merge_range('FL1:HF1', 'Review 3', merge_format_review)

    # HCSBD - Builds and writes excel's subheader
    header_arr = cfhcsbd.API_REST_KEYS_LIST + ["id"] + listHeader(cfhcsbd.HCSBD_MILESTONE_SUBMISSION) + listHeader(cfhcsbd.HCSBD_MILESTONE_REQUEST_FOR_PRIORITY_STATUS) + listHeader(cfhcsbd.HCSBD_MILESTONE_SCREENING) + listHeader(cfhcsbd.HCSBD_MILESTONE_REVIEW) + listHeader(cfhcsbd.HCSBD_MILESTONE_SCREENING) + listHeader(cfhcsbd.HCSBD_MILESTONE_REVIEW) + listHeader(cfhcsbd.HCSBD_MILESTONE_SCREENING) + listHeader(cfhcsbd.HCSBD_MILESTONE_REVIEW)
    worksheetHCSBD.write_row(1, 0, header_arr, bold)

    # HCSBD - Scraps table
    response = f.api_get(cfhcsbd.API_REST_HCSBD_LIST)["data"]
    
    # HCSBD - Builds and writes data to excel
    f.excel_writer(cfhcsbd.getExcelRow_HCSBD, worksheetHCSBD, response, 2)

    #for item in response:
    #    cfhcsbd.getExcelRow_HCSBD(item)
    
    # FDA - Create worksheet and set link format and date format
    worksheetFDA = wb.add_worksheet('FDA')
    worksheetFDA.set_column('A:A', None, underline)

    # FDA - Builds and writes excel's head
    worksheetFDA.write_row(0, 0, cffda.THEAD_PRODUCT_FDA_TABLE + cffda.THEAD_PRODUCT_FDA_DETAIL + ["PDF filed for approval"], bold)
    worksheetFDA.set_column('J:J', None, underline)
    worksheetFDA.set_column('C:C', None, date)
    worksheetFDA.set_column('E:E', None, date)
    worksheetFDA.set_column('L:L', None, date)

    # FDA - Scraps tables
    trs = []
    for year in cffda.FDA_YEARS:
        
        soup = f.scrapBaseUrl(cffda.API_REST_FDA + year)
        trs = trs + soup.find("table", class_=cffda.TABLE_CLASS_FDA).find("tbody").findChildren("tr" , recursive=False)
    
    for index, tr in enumerate(trs):
            if tr.find("th"):
                del trs[index]

    # FDA - Builds and writes data to excel
    f.excel_writer(cffda.getExcelRow_fda, worksheetFDA, trs, 1)

    #for tr in trs:
    #    cffda.getExcelRow_fda(tr)
        
    # Close csv file
    wb.close()

    print('Scraping website... END')

def override_sheet(name, range):
    global workbook

    print('Copying data to excel file... START')

    sNamList = [sh.name for sh in workbook.sheets]
    if name not in sNamList:
        workbook.sheets.add(name)

    print(f.getAbsolutePath(cfhcsbd.OUTPUT_FILE_TMP))

    source_wb = xw.books.open(f.getAbsolutePath(cfhcsbd.OUTPUT_FILE_TMP))
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
        workbook = app.books.open(f.getAbsolutePath(cfhcsbd.OUTPUT_FILE))
    except:
        workbook_create = xlsxwriter.Workbook(f.getAbsolutePath(cfhcsbd.OUTPUT_FILE), {'constant_memory': True})
        workbook_create.add_worksheet('HCSBD')
        workbook_create.add_worksheet('FDA')
        workbook_create.close()
        workbook = app.books.open(f.getAbsolutePath(cfhcsbd.OUTPUT_FILE))

    override_sheet('HCSBD', 'A1:HH2000')
    override_sheet('FDA', 'A1:AZ5000')

    # Remove tmp file
    f.os.remove(f.getAbsolutePath(cfhcsbd.OUTPUT_FILE_TMP))

    workbook.close()
    app.quit()

    print('Scraper executed successfully! END')

def run_from_xlsb():
    global workbook

    print('Running mode: run_from_xlsb... START')

    # Current workbook and sheets
    workbook = xw.Book.caller()
    
    run_scraper()

    override_sheet('HCSBD', 'A1:HH2000')
    override_sheet('FDA', 'A1:AZ5000')
    # Remove tmp file
    f.os.remove(f.getAbsolutePath(cfhcsbd.OUTPUT_FILE_TMP))

    print('Scraper executed successfully! END')

if __name__ == "__main__":
    run_from_exe()