# BizCardX-Extracting-Business-Card-Data-with-OCR

# Project Overview
BizCardX is a user-friendly tool for extracting information from business cards. The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. Users can access the extracted information using a GUI built using streamlit. The BizCardX application is a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button. Further the data stored in database can be easily Read, updated and deleted by user as per the requirement.

# Libraries/Modules used for the project!
1. Pandas - (To Create a DataFrame with the scraped data)
2. mysql.connector - (To store and retrieve the data)
3. Streamlit - (To Create Graphical user Interface)
4. EasyOCR - (To extract text from images)

# Features
# User-Friendly Interface:
The application boasts a simple and intuitive UI that guides users seamlessly through the process of uploading a business card image and extracting information.

# Data Extraction:
Utilizing the easyOCR library, the application extracts key details including company name, cardholder name, designation, mobile number, email address, website URL, area, city, state, and pin code.

# Database Integration:
Users can save the extracted information into a database along with the uploaded business card image. The database, powered by SQLite or MySQL, is designed to store multiple entries, each associated with its respective business card image and extracted information.

# CRUD Operations:
The application supports essential CRUD (Create, Read, Update, Delete) operations. Users can easily add, view, update, and delete entries through the Streamlit UI.
