import utils.funcs as f
from datetime import datetime

TABLE_CLASS_FDA = "table-striped"
TABLE_PRODUCT_CLASS_FDA = "exampleApplOrig"
API_REST_FDA = "https://www.fda.gov/drugs/new-drugs-fda-cders-new-molecular-entities-and-new-therapeutic-biological-products/novel-drug-approvals-"
FDA_YEARS = ["2020","2019","2018","2017","2016","2015"]
THEAD_PRODUCT_FDA_TABLE = ["Drug Name","Active Ingredient","Approval Date","FDA-approved use on approval date"]
THEAD_PRODUCT_FDA_DETAIL = ["Action Date","Submission","Action Type","Submission Classification","Review Priority; Orphan Status","Letters, Reviews, Labels, Patient Package Insert", "Notes"]
PDF_DATE_PATTERNS = ["BLA dated and received on (.*) and","BLA dated and received (.*) and","BLA dated (.*) received","BLA received (.*) and","NDA dated and received on (.*) and","NDA dated and received (.*) and","NDA received (.*) and","NDA dated (.*) received","NDAs dated (.*) received","NDAs dated and received (.*) and","dated and received on (.*) and","dated and received (.*) and","submitted and received (.*) and","new drug application NDA dated (.*) received"]

def dateParser_fda(str):
    if str and "Unable to fetch data" not in str:
        return datetime.strptime(str, '%m/%d/%Y')
    return str

def getDateFromPDF(product_row):
    
    if len(product_row) >= 5 and "appletter" in product_row[5]:
        for url in product_row[5].splitlines():
            if "appletter" in url:
                pdf = f.pdf_get(url.strip())
                if "NDA" not in pdf and "BLA" not in pdf:
                    pdf = f.extract_text_from_pdf_url(url.strip())
                
                pdf = pdf.replace(',', '').replace('.', '').replace('(', '').replace(')', '').replace('\n', ' ').replace('\r', ' ')
                pdf = " ".join(pdf.split())
                
                res = None
                for pattern in PDF_DATE_PATTERNS:
                    if f.re.search(pattern, pdf):
                        res = f.re.search(pattern, pdf).group(1)
                        break
                
                if res is None:
                    return "Unable to retrieve date from Letter PDF"

                res = res.split(" ")[:3]
                res = ' '.join(res)

                date = ""
                try:
                    date = datetime.strptime(res, '%B %d %Y')
                except:
                    if f.re.match(r"([A-Za-z]+)([0-9]+)", res, f.re.I):
                        date = res.replace(res, ' '.join(f.re.match(r"([a-z]+)([0-9]+)", res, f.re.I).groups()))
                    else:
                        date = "Unable to retrieve date from Letter PDF"

                return date

                #return dateParser_fda(res)
    return "No letter issued"

# FDA - Clean product element detail
def cleanColumns(td):
    if td.text:
        if td.find("a"):
            str = ""
            for a in td.find_all("a"):
                if "#" not in a["href"]:
                    str = str + a["href"] + "\n "
            return str.strip()

        return "" + td.text.strip()
    return ""

# FDA - Returns the detail row as a string
def getProductDetail_fda(soup):
    product_row = []

    if soup.find("table", id=TABLE_PRODUCT_CLASS_FDA):

        tr = soup.find("td", text=lambda t: t and "New Molecular Entity" in t)
        if tr:
            tr = tr.parent
        else:
            tr = soup.find("table", id=TABLE_PRODUCT_CLASS_FDA).find('tbody').find('tr')
        
        tds = tr.findChildren("td" , recursive=False)
        
        product_row = [cleanColumns(td) for td in tds]

        if "http" in product_row[-1]:
            product_row.pop()

    else:
        product_row.append("Unable to fetch data")

    return product_row

def getTextFromTR(e):
    if not e.text.strip() and e.attrs and e.attrs['headers'][0] == 'header2':
        return e.findNext().text.strip()
    return e.text.strip()

# FDA - Returns excel row as a string
def getExcelRow_fda(tr):
    table_row = [getTextFromTR(e) for e in tr.findChildren("td" , recursive=False)]
    
    #remove first column
    if table_row:
        table_row.pop(0)

    # product detail row
    product_row = []
    
    if tr.find("a"):
        url_product = tr.find("a")["href"].replace("httphttp", "http").strip().replace("http:", "https:")
        table_row[0] = '=HYPERLINK("'+url_product+'", "'+table_row[0]+'")'

        soup = f.scrapBaseUrl(url_product)
        product_row = getProductDetail_fda(soup)
        product_row.append(getDateFromPDF(product_row))

    excel_row = table_row + product_row
    # Parse dates
    excel_row[2] = dateParser_fda(excel_row[2])
    if len(excel_row) > 4:
        excel_row[4] = dateParser_fda(excel_row[4])
    
    return excel_row