#Ethan Herring 05/21/2020
'''Objective: 
Create a database of historical real estate transaction data
Desired dataset:
• All historical transaction records (1985-2020)
• Homes zoned as ‘single family residential’
• All transactions in the city of San Francisco

Data required:
• Transaction information:
o Date closed [yyyy.mm.dd]
o Price paid [$]
o Transaction Record - San Francisco MLS [#]
o Listing Date [yyyy.mm.dd] (earliest date preceding sale)
o Listing Price [$]
• Address information:
o Number and street name [text]
o Zip code [#####-####]
o Neighborhood [#]
o Assessor’s Parcel [#]
o Assessor’s Block [#]
o Assessor’s Lot [#]
• Property information:
o Property size (aka Property Area) [sq ft]
o Parcel size (aka Lot Area) [sq ft]
o Parcel depth [sq ft]
o Bedrooms [#]
o Bathrooms [#]
o Stories [#]
o Rooms [#]
o Year Built [yyyy]
• Zoning information:
o Property Class Code [text]
o Zoning Code [text]

Data sources:
https://data.sfgov.org/Housing-and-Buildings/Assessor-Historical-Secured-Property-Tax-Rolls/wv5m-vpq2
https://www.zillow.com/research/data/
This is a project for UpWork
'''
import pandas as pd
import requests
import csv
import datetime
import scrapy

outputDF = pd.DataFrame()
addressList = []
yearBuiltList = []
lastSalePriceList = []
zipCodeList = []
mlsNumberList = []
earlyDateList = []
earlyPriceList = []

class readData:
    def __init__(self, filepath):
        self.filepath = filepath

    def getSFData(self, filepath):
        return (pd.read_csv(filepath, header=0, index_col=2, usecols=["Parcel Number", "Use Definition", "Block", "Lot", "Zoning Code", "Current Sales Date", "Property Location", "Property Area", "Number of Stories",
        "Number of Rooms", "Number of Bedrooms", "Number of Bathrooms", "Property Class Code", "Property Class Code Definition", "Assessor Neighborhood Code"]))

class Conversions:
    def __init__(self, inputDF):
        self.inputDF = inputDF
    
    #Updates date to datetime format and limits results to specified years
    def units(self, inputDF):
        inputDF['Current Sales Date'] = pd.to_datetime(inputDF['Current Sales Date'])
        startYear = datetime.datetime(1985, 1, 1)
        #Limit results to only sales past 1985
        inputDF = inputDF[inputDF['Current Sales Date'] >= startYear]
        inputDF = inputDF[inputDF['Use Definition'] == 'Single Family Residential']
        print("length of addresses after filter: ", len(dataSF['Parcel Number']))
        return inputDF

class SLAuto:
    def __init__(self, frame):
        self.frame = frame

    def automateWeb(self, frame):
        #plug in parcel numbers to sfplanninggis.org/PIM/ to get other data (sale price, year built, street address)
        sfplanningURL = 'https://sfplanninggis.org/PIM/'
        options = Options()
        #options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
        options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        driver_path = '/usr/local/bin/chromedriver'
        driver = webdriver.Chrome(options = options, executable_path= driver_path)

        adList = []
        yearBList = []
        lastSPList = []
        zpCdList = []
        earlyDLst = []
        earlyPLst = []
        mlsNmbLst = []

        for x in frame['Parcel Number']:
            driver.get(sfplanningURL)
            searchBar = driver.find_element_by_id("addressInput")
            #searchBar = driver.find_element_by_class_name("Header-Search-field")
            searchBar.send_keys(str(x))
            #searchBar = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "Header-Search-field disabledDIV")))
            #searchBar.send_keys(Keys.RETURN)
            #searchBar = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "Header-Search-field")))
            #searchBar.send_keys(Keys.ENTER)
            icon = driver.find_element_by_id('Search-icon')
            icon.click()
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'Search-icon'))).click()
            #searchIcon = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "Search-icon")))
            #searchIcon.click()
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'Search-icon'))).click()
            address = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Report_DynamicContent_Property"]/div[1]/div[2]/div/div[2]/div[3]/span[1]'))).text
            adList.append(address)
            print(address)
            zipInput = driver.find_element_by_xpath('/html/body/div/div[2]/div[9]/div[3]/div[2]/div[3]/span/div[1]/div[2]/div/div[2]/div[3]').text
            zipCode = int(zipInput[-6:])
            print(zipCode)
            zpCdList.append(zipCode)
            driver.find_element_by_xpath('/html/body/div/div[2]/div[9]/div[3]/div[2]/div[3]/span/div[1]/div[2]/div/div[2]/div[4]/a[1]').click()
            if WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[4]/div/div[8]/div[2]"))).text != "-":    
                yearBuilt = int(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[4]/div/div[8]/div[2]"))).text)
            else:
                yearBuilt = None
            print(yearBuilt)
            yearBList.append(yearBuilt)

        #loops through Redfin to get transaction data for each entry
        i = 0
        for item in adList:
            redfinURL = 'https://www.redfin.com/'
            driver.get(redfinURL)
            zipCodeEntry = str(zpCdList[i])
            inputSearch = str(item + zipCodeEntry)
            searchBar = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "search-input-box")))
            searchBar.send_keys(inputSearch)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabContentId0"]/div/div/form/div[1]/button'))).click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headerUnifiedSearch"]/div/form/div/button'))).click()
            lastSalePrice = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[8]/div[3]/div/div/div/div[2]/div[1]/div/div[2]/div"))).text
            lastSPList.append(lastSalePrice)
            print(lastSalePrice)
            mlsNumber = int(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[20]/div/div/section/div/div/div/div/div/div[5]/div[7]/span[2]"))).text)
            mlsNmbLst.append(mlsNumber)
            print(mlsNumber)
            earlyListDate = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[26]/div/div/section/div/div/div/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/p[1]"))).text
            print("Early list date is: ", earlyListDate)
            earlyDLst.append(earlyListDate)
            earlyListPrice = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="propertyHistory-2"]/div[3]/div'))).text
            earlyPLst.append(earlyListPrice)
            print(earlyListPrice)
            i += 1
        driver.close()
        return adList, yearBList, lastSPList, zpCdList, earlyDLst, earlyPLst, mlsNmbLst
        


if __name__ == "__main__":
    dataSFPath = 'Assessor_Historical_Secured_Property_Tax_Rolls.csv'
    p = readData(dataSFPath)
    dataSF = p.getSFData(dataSFPath)
    print("length of addresses before filter: ", len(dataSF['Parcel Number']))
    
    autoInstance = SLAuto(dataSF)
    webInstance = autoInstance.automateWeb(dataSF)
    addressList, yearBuiltList, lastSalePriceList, zipCodeList, mlsNumberList, earlyDateList, earlyPriceList = webInstance()

    #Create columns in new output dataframe
    outputDF['Address'] = addressList
    outputDF['Zip_Code'] = zipCodeList
    outputDF['Year_Built'] = yearBuiltList
    outputDF['Earliest_List_Date'] = earlyDateList
    outputDF['Earliest_List_Price'] = earlyPriceList
    outputDF['Last_Sale_Price'] = lastSalePriceList
    outputDF['Parcel_Number'] = dataSF['Parcel Number']
    outputDF['Block'] = dataSF['Block']
    outputDF['Lot'] = dataSF['Lot']
    outputDF['Last_Sales_date'] = dataSF['Current Sales Date']
    outputDF['Street_Address'] = dataSF['Property Location']
    outputDF['Zoning_Code'] = dataSF['Zoning Code']
    outputDF['Property_Area'] = dataSF['Property Area']
    outputDF['Lot_Area'] = dataSF['Lot Area']
    outputDF['Parcel_Depth'] = dataSF['Lot Depth']
    outputDF['Number_of_Stories'] = dataSF['Number of Stories']
    outputDF['Number_of_Rooms'] = dataSF['Number of Rooms']
    outputDF['Number_of_Bedrooms'] = dataSF['Number of Bedrooms']
    outputDF['Number_of_Bathrooms'] = dataSF['Number of Bathrooms']
    outputDF['Property_Class_Code'] = dataSF['Property Class Code']
    outputDF['Property_Class_Code_Definition'] = dataSF['Property Class Code Definition']
    outputDF['Assessor_neighborhood_code'] = dataSF['Assessor Neighborhood Code']

    print("Process Complete")
    outputDF.to_csv('SanFran RealEstate DB',index=False, encoding='utf-8')
