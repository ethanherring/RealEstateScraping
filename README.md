# RealEstateScraping
This project was initially a project for an UpWork Client that never contacted me to actually complete.
Ethan Herring 05/21/2020
Objective: 
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
