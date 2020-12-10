import utils.funcs as f
from datetime import datetime

OUTPUT_FILE = "HCSBD-FDA-data-import.xlsx"
OUTPUT_FILE_TMP = "HCSBD-FDA-data-import-tmp.xlsx"
BASE_URL_HCSBD_1 = "https://hpr-rps.hres.ca/reg-content/summary-basis-decision-detailOne.php?lang=en&linkID="
BASE_URL_HCSBD_2 = "https://hpr-rps.hres.ca/reg-content/summary-basis-decision-detailTwo.php?lang=en&linkID="
API_REST_HCSBD = "https://health-products.canada.ca/api/dhpr/controller/dhprController.ashx?term=&pType=sbd&lang=en"
#API_REST_KEYS = ["brand_name","med_ingredient","manufacturer"]

THEAD_PRODUCT_HCSBD = ["Brand name","Medicinal ingredient","Manufacturer"]

BASE_URL_FDA = "https://www.pcpacanada.ca"
PATH_FDA = "/negotiations"
TABLE_CLASS_FDA = "datatable"
THEAD_PRODUCT_FDA = ["pCPA File Number","Sponsor/Manufacturer","CADTH Project Number","pCPA Engagement Letter Issued","Negotiation Process Concluded"]

def dateParser_HCSBD(str):
    if str and str != 'N/A':
        return datetime.strptime(str, '%B %d, %Y')
    return str

def dateParser_FDA(str):
    if str and str != 'Not Applicable':
        return datetime.strptime(str, '%Y-%m-%d')
    return str

# CADTH - Parse product table
def parseProductTable(element, product_tr_list):
    if product_tr_list.find("th", text=lambda t: t and element in t):
        product_td = product_tr_list.find("th", text=lambda t: t and element in t).find_next_sibling("td").get_text(separator=" ").strip()
        product_td = product_td.replace('\n', ' ').replace('\r', '')
        return product_td

    return ""

# CADTH - Clean product element detail
def cleanProductElement(element, soup):
    if element == "Manufacturer":
        #clean manufacturer value
        manufacturer = soup.find("p", class_="field_manufacturer")
        manufacturer.strong.decompose()
        return manufacturer.get_text(separator=" ").strip()

    elif element == "Submission Type" and soup.find("p", class_="field_submission_type"):
        #clean submission type value
        submission_type = soup.find("p", class_="field_submission_type")
        submission_type.strong.decompose()
        return submission_type.get_text(separator=" ").strip()

    elif soup.find("table", class_="cdr_milestones_table"):
        product_tr_list = soup.find("table", class_="cdr_milestones_table")
        if product_tr_list.find("th", text=lambda t: t and element in t):
            product_td = product_tr_list.find("th", text=lambda t: t and element in t).find_next_sibling("td").get_text(separator=" ").strip()
            product_td = product_td.replace('\n', ' ').replace('\r', '')
            return product_td
        
    return ""

# CADTH - Clean product element detail
def replaceEmptyProductElement(product_row, element, product_tr_list):
    if product_tr_list.find("th", text=lambda t: t and element in t):
        product_td = product_tr_list.find("th", text=lambda t: t and element in t).find_next_sibling("td").get_text(separator=" ").strip()
        product_td = product_td.replace('\n', ' ').replace('\r', '')
        return product_td

    return product_row

# CADTH - Returns the detail row as a string
def getProductDetail_HCSBD(soup):
    product_row = []

    #1st detected format (ex: https://www.cadth.ca/xalkori-resubmission-first-line-advanced-nsclc-details)
    #2nd detected format (ex: https://www.cadth.ca/ibrutinib-imbruvica-leukemia)
    if soup.find("table", class_=TABLE_PRODUCT_CLASS_HCSBD):
        product_tr_list = soup.find("table", class_=TABLE_PRODUCT_CLASS_HCSBD)
        product_row = [parseProductTable(element, product_tr_list) for element in THEAD_PRODUCT_HCSBD]

    #3rd detected format (ex: https://www.cadth.ca/aripiprazole-25)
    #4th detected format (ex: https://www.cadth.ca/pegfilgrastim-6)
    elif soup.find("div", class_="publish-date"):
        product_row = [cleanProductElement(element, soup) for element in THEAD_PRODUCT_HCSBD]

    else:
        product_row.append("Unable to fetch data, new web format")

    return product_row

# CADTH - Returns excel row as a string
def getExcelRow_HCSBD(item):

    # product url
    url_product = BASE_URL_HCSBD_1 + item['link_id']
    if item['template'] == 2:
        url_product = BASE_URL_HCSBD_1 + item['link_id']

    table_row[0] = '=HYPERLINK("'+url_product+'", "'+table_row[0]+'")'

    soup = f.scrapBaseUrl(url_product)
    product_row = getProductDetail_HCSBD(soup)

    excel_row = table_row + product_row

    # Parse dates
    excel_row[5] = dateParser_HCSBD(excel_row[5])
    excel_row[6] = dateParser_HCSBD(excel_row[6])
    excel_row[12] = dateParser_HCSBD(excel_row[12])
    excel_row[15] = dateParser_HCSBD(excel_row[15])
    excel_row[16] = dateParser_HCSBD(excel_row[16])
    excel_row[17] = dateParser_HCSBD(excel_row[17])
    excel_row[20] = dateParser_HCSBD(excel_row[20])
    excel_row[21] = dateParser_HCSBD(excel_row[21])
    excel_row[22] = dateParser_HCSBD(excel_row[22])
    excel_row[23] = dateParser_HCSBD(excel_row[23])
    excel_row[24] = dateParser_HCSBD(excel_row[24])
    excel_row[25] = dateParser_HCSBD(excel_row[25])
    excel_row[26] = dateParser_HCSBD(excel_row[26])

    return excel_row

# CADTH - Returns the detail row as a string
def getProductDetail_FDA(soup):
    product_row = []
    product_row.append(soup.find("span", class_="views-label-nid").find_next_sibling("span").get_text(separator=" ").strip())
    product_row.append(soup.find("span", class_="views-label-field-manufacturer-name").find_next_sibling("div").get_text(separator=" ").strip())
    product_row.append(soup.find("span", class_="views-label-field-cadth-project-id").find_next_sibling("div").get_text(separator=" ").strip())
    product_row.append(soup.find("span", class_="views-label-field-engagement-date").find_next_sibling("div").get_text(separator=" ").strip())
    product_row.append(soup.find("span", class_="views-label-field-close-date").find_next_sibling("div").get_text(separator=" ").strip())
    
    return product_row

# CADTH - Returns excel row as a string
def getExcelRow_FDA(tr):
    table_row = [e.get_text(separator=" ").strip() for e in tr.find_all("td")]

    # product url
    url_product = BASE_URL_FDA + tr.td.a['href']
    table_row[0] = '=HYPERLINK("'+url_product+'", "'+table_row[0]+'")'

    soup = f.scrapBaseUrl(url_product)
    product_row = getProductDetail_FDA(soup)

    excel_row = table_row + product_row

    # Parse dates
    excel_row[7] = dateParser_FDA(excel_row[7])
    excel_row[8] = dateParser_FDA(excel_row[8])

    return excel_row