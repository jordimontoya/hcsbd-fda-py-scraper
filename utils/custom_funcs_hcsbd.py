import utils.funcs as f
from datetime import date

OUTPUT_FILE = "HCSBD-FDA-data-import.xlsx"
OUTPUT_FILE_TMP = "HCSBD-FDA-data-import-tmp.xlsx"

BASE_URL_HCSBD_1 = "https://hpr-rps.hres.ca/reg-content/summary-basis-decision-detailOne.php?lang=en&linkID="
BASE_URL_HCSBD_2 = "https://hpr-rps.hres.ca/reg-content/summary-basis-decision-detailTwo.php?lang=en&linkID="
BASE_URL_HCSBD_3 = "https://hpr-rps.hres.ca/reg-content/summary-basis-decision-medical-device-detailOne.php?lang=en&linkID="
API_REST_HCSBD_LIST = "https://health-products.canada.ca/api/dhpr/controller/dhprController.ashx?term=&pType=sbd&lang=en"
API_REST_HCSBD_DETAIL = "https://health-products.canada.ca/api/dhpr/controller/dhprController.ashx?linkID={}&pType=sbd&lang=en"

API_REST_KEYS_LIST = ["brand_name","med_ingredient","manufacturer"]

HCSBD_MILESTONE_SUBMISSION = [
    "Pre-submission 1|Pre-submission|Pre&#8209;submission",
    "Pre-submission 2|Pre-submission",
    "Advance Consideration",
    "Submission filed|Submissionfiled",
    "Acceptance Letter issued",
    "Rolling New Drug Submission (NDS) filed",
    "Administrative information, Cross-Reference to Rolling NDS",
    "Approval issued by Director",
    "Refusal"
    ]

HCSBD_MILESTONE_REQUEST_FOR_PRIORITY_STATUS = [
    "Filed",
    "Advance Consideration",
    "Request for reconsideration",
    "Health Canada requested withdrawal of priority status",
    "Sponsor withdrew priority status",
    "Approval issued|Approved|Granted",
    "Rejection issued|Rejection",
    "Acceptance Letter",
    "Submission filed"
    ]

HCSBD_MILESTONE_SCREENING = [
    "Pre-submission meeting",
    "Quality",
    "Clinical",
    "Deficiency Notice issued",
    "NON issued",
    "Pre-response to NON meeting",
    "Response filed",
    "Update Notice issued",
    "Submission received in Regulatory Affairs Division (RAD)",
    "Acceptance Letter",
    "Rejection Letter issued",
    "Request for Reconsideration|Reconsideration Decision Letter issued",
    "Labelling Review",
    "Response received",
    "Approval issued",
    "Submission filed",
    "NOC|Notice of Compliance"
    ]

HCSBD_MILESTONE_REVIEW = [
    "Pre-submission meeting",
    "On-Site Evaluation|On Site Evaluation",
    "SAC Teleconference",
    "Review of Risk Management Plan",
    "Labelling Review",
    "Biopharmaceutics",
    "Consistency Sample testing",
    "Medical",
    "Quality",
    "Comprehensive",
    "Biostatistics|Biostat",
    "Non-clinical",
    "Clinical",
    "Radiation Dosimetry",
    "Medical Devices",
    "Device",
    "Electrocardiogram",
    "Label",
    "Acceptance Letter",
    "Response received",
    "Scientific Advisory",
    "Review of Response to NOC/c‑QN",
    "Revised Qualifying Notice",
    "NOC/c-QN",
    "NOC/c|Notice of Compliance with Conditions",
    "NOC|Notice of Compliance",
    "Level 1 Appeal",
    "NOD/W|Notice of Deficiency/Withdrawal",
    "NON/NOD"
    "NOD|Notice of Deficiency",
    "Look Alike Sound Alike name change and revised NOC issued",
    "Response to NON filed",
    "NON/W",
    "NON|Notice of Non Compliance",
    "NOD|Notice of Decision",
    "Expert Advisory Panel meeting",
    "Acceptance of Advance Consideration",
    "Rejection issued",
    "Response filed",
    "Request to cancel submission filed",
    "Submission re-filed Control","Submission subject to Federal Court Stay",
    "Filed",
    "Interim Order issued",
    "Authorization for sale",
    "Submission withdrawn by sponsor|Withdrawal/Cancellation by sponsor|Sponsor withdrew the New Drug Submission|Submission cancelled by sponsor|withdrew submission",
    "Submission cancelled - administrative",
    "Cancellation Letter"
    ]

HCSBD_MILESTONE_AVOIDED_TITLES = ["Control Number","Original Submission","Refiled Submission","Submission No","Submission filed","Control No","Re-filed","Request for Reconsideration"]
# Request for Reconsideration - https://hpr-rps.hres.ca/reg-content/summary-basis-decision-detailOne.php?lang=en&linkID=SBD00156
# Regulatory hold title - https://hpr-rps.hres.ca/reg-content/summary-basis-decision-detailOne.php?lang=en&linkID=SBD00240
# Patent Hold title - https://hpr-rps.hres.ca/reg-content/summary-basis-decision-detailOne.php?lang=en&linkID=SBD00281

def dateParser_HCSBD(str):
    if str and str != '':
        return date.fromtimestamp(int(str))
    return ""

def getMilestoneCompletedDate(element):
    if element["completed_date"]:
        date = element["completed_date"].replace("/Date(", "")
        if "-" in date:
            date = date.split("-")[0]
        elif "+" in date:
            date = date.split("+")[0]

        date = date.strip().replace('\n', '').replace('\r', '')[0:10]

        return dateParser_HCSBD(date)
    else:
        return ""

# Looping through milestone_list and if found, retrieve date and remove item from list
# If milestone title found (<b> or <strong>, break loop and return "", this means next phase starts)
def getProductMilestones(element, array):
    for index, item in enumerate(array):
        if "<b>" in item["milestone"] or "<strong>" in item["milestone"] or "<p>" in item["milestone"]:
            if "Pre-submission meeting" in item["milestone"] or "Submission filed" in item["milestone"]:
                date = getMilestoneCompletedDate(item)
                del array[index]
                return date
            break
        else:
            if "|" in element:
                if [s for s in element.lower().split("|") if s in item["milestone"].lower()]:
                    date = getMilestoneCompletedDate(item)
                    del array[index]
                    return date
            
            elif element.lower() in item["milestone"].lower():
                date = getMilestoneCompletedDate(item)
                del array[index]
                return date
        
    return ""

def isTitle(item):
    return "<b>" in item["milestone"] or "<strong>" in item["milestone"] or "<p>" in item["milestone"]  or ("Screening" in item["milestone"] and not item["completed_date"]) or ("Review" in item["milestone"] and not item["completed_date"]) or ("Request for priority status" in item["milestone"] and not item["completed_date"])

def removeMilestoneTitle(array):
    if isTitle(array[0]):
        array.pop(0)

def checkTitle(title, array):
    if array and array[0]["milestone"] and isTitle(array[0]):
        if array and title.lower() in array[0]["milestone"].lower():
            return True
        elif ("Level" in array[0]["milestone"] and "Appeal" in array[0]) or [s for s in HCSBD_MILESTONE_AVOIDED_TITLES if s in array[0]["milestone"]]:
            array.pop(0)
            removeDuplicateMilestones(array)
            if array and title.lower() in array[0]["milestone"].lower():
                return True

    return False

def removeDuplicateMilestones(array):
    toRemove = []
    if array and array[0]["milestone"] and not isTitle(array[0]):
        for item in array:
            if not isTitle(item):
                toRemove.append(item)
            else:
                break
        for removeItem in toRemove:
            if removeItem["milestone"] in array[0]["milestone"]:
                array.remove(removeItem)

    #elif array and array[0]["milestone"] and ("Level" not in array[0]["milestone"] and "Appeal" not in array[0]["milestone"]) and [s for s in HCSBD_MILESTONE_AVOIDED_TITLES if s not in array[0]["milestone"]]:
    #    if not checkTitle("Screening", array) and not checkTitle("Review", array):
    #        print("wow")

# HCSBD - Returns the detail row as a string
def getMilestonesRow_HCSBD(array):
    product_row = []

    product_row = [getProductMilestones(element, array) for element in HCSBD_MILESTONE_SUBMISSION]
    
    if checkTitle("Request for priority status", array):
        removeMilestoneTitle(array)
        if any("Request for priority status" in sublist["milestone"] for sublist in array):
            array = [sublist for sublist in array if "Request for priority status" not in sublist["milestone"]]
        product_row = product_row + [getProductMilestones(element, array) for element in HCSBD_MILESTONE_REQUEST_FOR_PRIORITY_STATUS]
    else:
        product_row = product_row + ["" for element in HCSBD_MILESTONE_REQUEST_FOR_PRIORITY_STATUS]
    
    # Screening 1
    if not checkTitle("Screening", array) and not checkTitle("Screnning", array):
        removeDuplicateMilestones(array)
    if checkTitle("Screening", array) or checkTitle("Screnning", array):
        removeMilestoneTitle(array)
        product_row = product_row + [getProductMilestones(element, array) for element in HCSBD_MILESTONE_SCREENING]

    # Review 1
    if not checkTitle("Review", array):
        removeDuplicateMilestones(array)
    if checkTitle("Review", array):
        removeMilestoneTitle(array)
        product_row = product_row + [getProductMilestones(element, array) for element in HCSBD_MILESTONE_REVIEW]

    # Screening 2
    if not checkTitle("Screening", array) and not checkTitle("Screnning", array):
        removeDuplicateMilestones(array)
    if checkTitle("Screening", array) or checkTitle("Screnning", array):
        removeMilestoneTitle(array)
        product_row = product_row + [getProductMilestones(element, array) for element in HCSBD_MILESTONE_SCREENING]

    # Review 2
    if not checkTitle("Review", array):
        removeDuplicateMilestones(array)
    if checkTitle("Review", array):
        removeMilestoneTitle(array)
        product_row = product_row + [getProductMilestones(element, array) for element in HCSBD_MILESTONE_REVIEW]

    # Screening 3
    if not checkTitle("Screening", array) and not checkTitle("Screnning", array):
        removeDuplicateMilestones(array)
    if checkTitle("Screening", array) or checkTitle("Screnning", array):
        removeMilestoneTitle(array)
        product_row = product_row + [getProductMilestones(element, array) for element in HCSBD_MILESTONE_SCREENING]

    # Review 3
    if not checkTitle("Review", array):
        removeDuplicateMilestones(array)
    if checkTitle("Review", array):
        removeMilestoneTitle(array)
        product_row = product_row + [getProductMilestones(element, array) for element in HCSBD_MILESTONE_REVIEW]

    return product_row

# HCSBD - Returns excel row as a string
def getExcelRow_HCSBD(item):
    table_row = [item[""+element] for element in API_REST_KEYS_LIST]

    # product url
    url_product = BASE_URL_HCSBD_1 + item['link_id']

    if item['template'] == 2:
        url_product = BASE_URL_HCSBD_2 + item['link_id']

    if "N/A" in item['med_ingredient']:
        url_product = BASE_URL_HCSBD_3 + item['link_id']

    if "</sup>" in table_row[0]:
        table_row[0] = table_row[0].replace("<sup>"," ").split('</sup>')[0]

    if "<em>" in table_row[0]:
        table_row[0] = table_row[0].replace("<em>"," ").split('</em>')[0]

    table_row[0] = '=HYPERLINK("'+url_product+'", "'+table_row[0].replace("<sup>","")+'")'
    table_row.append(item['link_id'])

    response = f.api_get(API_REST_HCSBD_DETAIL.format(item['link_id']))
    #print("Start: "+API_REST_HCSBD_DETAIL.format(item['link_id']))
    
    product_row = []
    if "milestone_list" in response and "N/A" not in item['med_ingredient']:
        product_row = getMilestonesRow_HCSBD(response["milestone_list"])

    return table_row + product_row