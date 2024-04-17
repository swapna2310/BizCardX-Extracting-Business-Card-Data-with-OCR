import easyocr
from PIL import Image
import re
import pandas as pd
import numpy as np
import os
import cv2
import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import matplotlib.pyplot as plt

reader= easyocr.Reader(['en'])

#Creating a database
import pymysql
config = {
            'user':'root', 'password':'1234',
            'host':'127.0.0.1','port':3306,'database':'bizcard'
        }

connection = pymysql.connect(**config) 
cursor=connection.cursor()

Create_Query= '''CREATE TABLE IF NOT EXISTS card_data(Name text,
                                                        Designation text,
                                                        Contact varchar(100),
                                                        Email text,
                                                        Website text,
                                                        Area varchar(50),
                                                        City text,
                                                        State text,
                                                        Pincode varchar(10),
                                                        Company_Name text
                                                        )'''
cursor.execute(Create_Query)
connection.commit()

# streamlit page 
page_bg_img='''
<style>
[data-testid="stAppViewContainer"]{
        background-color:#87CEEB;   
}
</style>'''
st.set_page_config(page_title= "Business Card Data Extraction with OCR",
                layout= "wide",
                initial_sidebar_state= "expanded",)
st.markdown("<h1 style='text-align: center; color: Black;'>Business Card Data Extraction</h1>", unsafe_allow_html=True)
st.markdown(page_bg_img,unsafe_allow_html=True)
st.divider()

SELECT = option_menu(None, ["Home", "Upload & Extract", "Modify"],
                    icons=["house", "cloud-upload","vector-pen"],
                    default_index=2,
                    orientation="horizontal",
                    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100%"},
                            "icon": {"color": "black", "font-size": "20px"},
                            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#FFA500"},
                            "nav-link-selected": {"background-color": "#FFA500"}})


if SELECT== "Home":

    st.subheader("About the Application")
    st.write(" Users can save the information extracted from the card image using easy OCR. The information can be uploaded into a database (MySQL) after alterations that supports multiple entries. ")     
    st.markdown("## :red[Domain] : Digital Buisness Card")
    st.markdown("## :red[Overview] : The purpose of the project is to automate the process of extracting data from the bizzcard The extracted information should be displayed in a clean and organized manner, and users should be able to easily add it to the database with the click of a button and Allow the user to Read the data,Update the data and Allow the user to delete the data through the streamlit UI")
    st.markdown("## :green[**Technologies Used :**] Python,easy OCR, Streamlit, SQL, Pandas")
    st.subheader("Existing Data in Database")
    cursor.execute('''Select Name, Designation, Contact, Email, Website,
                         Area, City, State, Pincode, Company_Name from card_data''')
    updated_df = pd.DataFrame(cursor.fetchall(),
                    columns=['Name','Designation','Contact',
                            'Email','Website','Area','City','State','Pincode','Company_Name'])

    st.write(updated_df)  


# UPLOAD AND EXTRACT MENU
if SELECT=="Upload & Extract":
    st.subheader(":black[Business Card]")
    image_file= st.file_uploader("Upload the Business Card below:", type=["png","jpg","jpeg"])
    #def extract_text(image_file):
        # uploaded_card= os.path.join(os.getcwd(),"Bizcard")
        # with open(os.path.join(uploaded_card, image_file.name), "wb") as f:
        #     f.write(image_file.getbuffer())
        
    # DISPLAYING THE UPLOADED CARD   
    if image_file is not None:
        col1, col2 = st.columns(2, gap="large")
        with col1:
            img=image_file.read()
            st.markdown("#     ")
            st.markdown("### Business Card has been uploaded")
            st.image(img,caption="The image has been uploaded successfully",width=500)
            #extract_text(image_file)

        with col2:
            saved_img = os.getcwd() + "\\" + "Bizcard" + "\\" + image_file.name
            image = cv2.imread(saved_img)
            reader= easyocr.Reader(['en'])
            details= reader.readtext(saved_img)

            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("### Image Processed and Data Extracted")
            def image_preview(image, details): 
                for (bbox,text,prob) in details:
                 # unpack the bounding box
                    (tl, tr, br, bl) = bbox
                    tl = (int(tl[0]), int(tl[1]))
                    tr = (int(tr[0]), int(tr[1]))
                    br = (int(br[0]), int(br[1]))
                    bl = (int(bl[0]), int(bl[1]))
                    cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                    cv2.putText(image, text, (tl[0], tl[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                plt.rcParams['figure.figsize'] = (15, 15)
                plt.axis('off')
                plt.imshow(image)
            b= image_preview(image, details) 
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(b)

# easy OCR
        saved_img = os.getcwd() + "\\" + "Bizcard" + "\\" + image_file.name
        reader= easyocr.Reader(['en'])
        result= reader.readtext(saved_img,detail=0, paragraph=False)
# CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
        def img_to_binary(file):
            # Convert image data to binary format
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData
        
        data={
            "Name":[],
            "Designation":[],
            "Contact":[],
            "Email":[],
            "Website":[],
            "Area":[],
            "City":[],
            "State":[],
            "Pincode":[],
            "Company_Name":[],
            #"image": img_to_binary(saved_img)
            }
        
        def process_data(details):
    
            for i in range(len(details)):
                match1 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+). ([a-zA-Z]+)', details[i])
                match2 = re.findall('([0-9]+ [A-Z]+ [A-Za-z]+)., ([a-zA-Z]+)', details[i])
                match3 = re.findall('^[E].+[a-z]', details[i])
                match4 = re.findall('([A-Za-z]+) ([0-9]+)', details[i])
                match5 = re.findall('([0-9]+ [a-zA-z]+)', details[i])
                match6 = re.findall('.com$', details[i])
                match7 = re.findall('([0-9]+)', details[i])

                if i == 0:
                    data['Name'].append(details[i])
                elif i == 1:    
                    data['Designation'].append(details[i])
                elif '-' in details[i]:
                    data['Contact'].append(details[i])
                elif '@' in details[i]:
                    data['Email'].append(details[i])
                elif "www " in details[i].lower() or "www." in details[i].lower():
                    data['Website'].append(details[i])
                elif "WWW" in details[i]:
                    data["Website"] = details[i] + "." + details[i+1]
                elif match6:
                    pass
                elif match1:
                    data["Area"] = match1[0][0]
                    data["City"] = match1[0][1]
                    data["State"] = match1[0][2]
                elif match2:
                    data["Area"] = match2[0][0]
                    data["City"] = match2[0][1]   
                elif match3:
                    data["City"] = match3[0]
                elif match4:
                    data["State"] = match4[0][0]
                    data["Pincode"] = match4[0][1]
                elif match5:
                    data["Area"] = match5[0] + ' St,'
                elif match7:
                    data["Pincode"] = match7[0]
                else:
                    data["Company_Name"].append(details[i])
                    
            data["Contact"] = " & ".join(data["Contact"])  
            # Joining company names with space
            data["Company_Name"] = " ".join(data["Company_Name"])
            #return data

        process_data(result)
        df = pd.DataFrame(data)
        st.success("### Data Extracted!")
        st.write(df)

        if st.button("Upload to Database"):
            for i, row in df.iterrows():
                insert_query=  '''Insert into card_data (Name, Designation, Contact, Email, Website, Area, City, State, Pincode, Company_Name)
                                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cursor.execute(insert_query,tuple(row))
                connection.commit()
                cursor.execute('''Select Name, Designation, Contact, Email, Website,
                                Area, City, State, Pincode, Company_Name from card_data''')
                updated_df = pd.DataFrame(cursor.fetchall(),
                            columns=['Name','Designation','Contact',
                                    'Email','Website','Area','City','State','Pincode','Company_Name'])

                st.success("#### Uploaded to database successfully!")
                st.write(updated_df)

# modify menu
elif SELECT == "Modify":
    st.subheader((':blue[You can view , alter or delete the extracted data in this app]'))
    select= option_menu(None,
                        options= ["ALTER", "DELETE"],
                        default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                 "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                 "nav-link-selected": {"background-color": "#FFA500"}})
    if select=="ALTER":
        st.markdown(":blue[Alter the data here]")

        try:
            cursor.execute("SELECT Name FROM card_data")
            result=cursor.fetchall()
            business_cards={}
            for row in result:
                business_cards[row[0]]=row[0]
            options= ['None'] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")

            else:
                st.markdown("#### Update or modify any data below")
                cursor.execute("SELECT Name,Designation,Contact,Email,Website,Area,City,State,Pincode,Company_Name FROM card_data WHERE Name=%s",
                (selected_card,))
                result=cursor.fetchone()

               # DISPLAYING ALL THE INFORMATIONS
                name= st.text_input("Name", result[0])
                designation= st.text_input("Designation", result[1])
                contact= st.text_input("Contact", result[2])
                email = st.text_input("Email", result[3])
                website = st.text_input("Website", result[4])
                area = st.text_input("Area", result[5])
                city = st.text_input("City", result[6])
                state = st.text_input("State", result[7])
                pin_code = st.text_input("Pincode", result[8])
                company_name = st.text_input("Company_Name", result[9])


                if st.button(":black[Commit changes to DB]"):
                    
                    # Update the information for the selected business card in the database
                    cursor.execute('''UPDATE card_data SET Name=%s,Designation=%s,Contact=%s, Email=%s, Website=%s,
                                    Area=%s, City=%s, State=%s, Pincode=%s, Company_Name=%s WHERE Name=%s''',
                                   (name, designation, contact, email, website, area, city, state, pin_code, company_name,
                    selected_card))
                    connection.commit()
                    st.success("Information updated in database successfully.")


            if st.button(":black [View data]"):
                cursor.execute('''Select Name, Designation, Contact, Email, Website,
                                Area, City, State, Pincode, Company_Name from card_data''')
                updated_df2 = pd.DataFrame(cursor.fetchall(),
                                columns=['Name','Designation','Contact',
                                        'Email','Website','Area','City','State','Pincode','Company_Name'])

                st.write(updated_df2)  

        except:
            st.warning("There is no data available in the database")

    if select== "DELETE":
        st.subheader(":blue[Delete the data]")
        try:
            cursor.execute("SELECT Name FROM card_data")
            result=cursor.fetchall()
            business_cards={}
            for row in result:
                business_cards[row[0]]=row[0]
            options= ['None'] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")

            else:
                st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
                st.write("#### Proceed to delete this card?")
                if st.button("confirm Delete"):
                    cursor.execute(f"DELETE FROM card_data WHERE Name='{selected_card}'")
                    connection.commit()
                    st.success("Business card information deleted from database.")

            if st.button(":black[View updated data]"):
                cursor.execute('''Select Name, Designation, Contact, Email, Website,
                                Area, City, State, Pincode, Company_Name from card_data''')
                updated_df3 = pd.DataFrame(cursor.fetchall(),
                                columns=['Name','Designation','Contact',
                                    'Email','Website','Area','City','State','Pincode','Company_Name'])

                st.write(updated_df3)  

        except:
            st.warning("There is no data available in the database")        

       