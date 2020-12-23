import utils.funcs as f
from datetime import date

TABLE_CLASS_FDA = "table-striped"
TABLE_PRODUCT_CLASS_FDA = "exampleApplOrig"
API_REST_FDA = "https://www.fda.gov/drugs/new-drugs-fda-cders-new-molecular-entities-and-new-therapeutic-biological-products/novel-drug-approvals-"
FDA_YEARS = ["2020","2019","2018","2017","2016","2015"]
THEAD_PRODUCT_FDA_TABLE = ["Drug Name","Active Ingredient","Approval Date","FDA-approved use on approval date"]
THEAD_PRODUCT_FDA_DETAIL = ["Action Date","Submission","Action Type","Submission Classification","Review Priority; Orphan Status","Letters, Reviews, Labels, Patient Package Insert", "Notes"]
#API_REST_FDA = "https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_class_code_description:%22Type%201%20-%20New%20Molecular%20Entity%22&limit=1000&sort=submissions.submission_status_date:desc"
#PDF to text pro version: https://stackoverflow.com/questions/34819638/python-scraping-pdf-from-url
#and this one:https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python/26495057#26495057

#PDF to text: https://stackoverflow.com/questions/52683133/text-scraping-a-pdf-with-python-pdfquery
#PDF to text: https://stackoverflow.com/questions/59130672/how-to-scrape-pdfs-using-python-specific-content-only

def dateParser_fda(str):
    if str and str != 'N/A':
        return datetime.strptime(str, '%B %d, %Y')
    return str

# FDA - Clean product element detail
def cleanColumns(td):
    if td.find("a"):
        str = ""
        for a in td.find_all("a"):
            str = str + a["href"] + "\n "
        return str.rstrip()

    return ""+td.text.strip()

# FDA - Returns the detail row as a string
def getProductDetail_fda(soup):
    product_row = []

    if soup.find("table", id=TABLE_PRODUCT_CLASS_FDA):
        tds = soup.find("table", id=TABLE_PRODUCT_CLASS_FDA).find('tbody').find('tr').findChildren("td" , recursive=False)
        product_row = [cleanColumns(td) for td in tds]
        product_row.pop()

    else:
        product_row.append("Unable to fetch data, new web format")

    return product_row

# FDA - Returns excel row as a string
def getExcelRow_fda(tr):
    table_row = [e.text.strip() for e in tr.findChildren("td" , recursive=False)]
    
    #remove first column
    if table_row:
        table_row.pop(0)

    # product detail row
    product_row = []
    
    if tr.find("a"):
        url_product = tr.find("a")["href"].replace("httphttp", "http")
        table_row[0] = '=HYPERLINK("'+url_product+'", "'+table_row[0]+'")'

        print("Start: "+url_product)

        soup = f.scrapBaseUrl(url_product)
        product_row = getProductDetail_fda(soup)

    excel_row = table_row + product_row

    # Parse dates
    #if len(excel_row) > 4:
        #excel_row[9] = dateParser_fda(excel_row[9])
    
    return excel_row