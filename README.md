# hcsbd-fda-py-scraper

By: [Codekubik](http://www.codekubik.com)

## Introduction
This python script pulls data from 2 different websites and creates/overwrites 2 Excel worksheets with the results.
`scraper.exe` bundles the python scripts into one single stand-alone executable under Windows, Mac OS X and GNU/Linux.

Datasources and outputs:
- The *HC SBD* sheet contains the data extracted from the [Health Canada Summary Basis of Decision](https://hpr-rps.hres.ca/reg-content/summary-basis-decision-result.php?lang=en&term=) along with all product details for each record.
- The *FDA* sheet contains the new molecular entities extracted from the [FDA drug approvals](https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=reportsSearch.process) along with the Approval Date(s) and History, Letters, Labels, Reviews for each record. The submission dates has been retrieved from PDFs called "Letter (PDF)".


## What you need to know

- Expected execution time: around 3:30 minutes.
- Excel file will be created next to `scraper.exe`
- Excel file will be always called *HCSBD-FDA-data-import.xlsx*
- If Excel's file *HCSBD-FDA-data-import.xlsx* already exists, worksheets *HCSBD* and *FDA* will be overwritten. Formulas, datatables and Pivot tables in other sheets inside this workbook will continue working after scraper execution so you can reuse the same Excel's workbook every time.
- If *HCSBD-FDA-data-import.xlsx* file does not exists, the script will create the file automatically.


## Guidelines
> **Very important:** Before every execution, close entirely excel file *HCSBD-FDA-data-import.xlsx*. Otherwise the app will be unable to open the file.

> Killing the execution before it ends may cause the excel file still open on the background. Just kill Microsoft Excel process on Windows/MAC OS Task Manager

#### Execute scraper.exe

1. Download executable file by clicking on `scraper.exe` and then `Download` button
2. On first execution, right click and scan `scraper.exe` with your antivirus. Executable files coming from Internet are intercepted by all antivirus. Once scanned, the antivirus will let you execute the file as many times as you want.
3. Double click on `scraper.exe`
4. A cmd command will pop. Wait and do nothing until it disapears.
5. Once cmd command closed, excel *HCSBD-FDA-data-import.xlsx* is ready to use. Double check excel's last modification datetime.

#### Execute from IDE or Command line (only for development purposes)

1. Download and install [Python 3.9](https://www.python.org/downloads/release/python-390/) and `PIP`
2. Add python to system env variables
3. Download code source `cadth-pcpa-py-scraper`
4. Open cmd and execute pip install to import below libraries:
    - `pip install xlsxwriter`
    - `pip install xlwings`
    - `pip install beautifulsoup4`
    - `pip install multiprocess`
    - `pip install DateTime`
    - `pip install pdfminer`
    - `pip install cProfile`
5. Open cmd --> go to python directory --> execute command `python scraper.py`
6. Once script execution ends, excel file *HCSBD-FDA-data-import.xlsx* is ready to use. Double check excel's last modification datetime.
