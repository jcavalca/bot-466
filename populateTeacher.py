import pandas as pd, numpy as np, requests, sys, pymysql.cursors
from bs4 import BeautifulSoup

def read_stat_prof():
        url = "https://statistics.calpoly.edu/content/directory#:~:text=F%204%3A10%2D6pm%20Zoom,See%20Canvas%20for%20Zoom%20Link."
        myRequest = requests.get(url)
        soup = BeautifulSoup(myRequest.text,"html.parser")
        tables = soup.find_all('table')
        admin = tables[0]
        profs = tables[1]

        df_cols = ['Name', 'Office', 'Phone', 'Email', 'OfficeHours']
        df = pd.DataFrame(columns = df_cols)

        arows = admin.find_all('tr')
        prows = profs.find_all('tr')
        rows = arows + prows
        
        for i, row in enumerate(rows):
            values = row.find_all('td')
            if values:
                # 1) GET NAME
                # works for: <td>NAME</td>
                # and: <td><a href=“…”><strong>NAME</strong></a></td>
                name = values[0].string
                
                if not name:
                   # works for: <td><p><a href=“…”><strong>NAME</strong></a></p></td>
                   # and: <td><p><strong><a href=“..”.>NAME</a></strong><\p><\td> (but going to
                   # except to un-nest the result)
                   name = values[0].find_all('strong')
                   
                   if not name:
                       # works for: <td><p><b>NAME</b></p></td>
                       name = values[0].find_all('b')

                   # To un-nest the  resulting list
                   # for: <td><p><a href=“…”><strong>NAME</strong></a></p></td>
                   # and: <td><p><b>NAME</b></p></td>
                   try:
                       name = ",".join([item for items in name for item in items])

                   # for: <td><p><strong><a href=“..”.>NAME</a></strong><\p><\td> 
                   except:
                       name = ",".join([item.text for items in name for item in items])
      
                # 2) GET OFFICE 
                office = values[1].text.strip()

                # 3) GET iPHONE
                phone = values[2].text.strip()
                phone = '805' + phone.replace('-', '')

                # 4) GET EMAIL
                email = values[3].text.strip()

                # 5) GET OFFICE HOURS                  
                oh = values[4].find_all('strong')
                oh = ", ".join([item.strip() for items in oh for item in items])
                if oh.endswith(", TRF ("):
                    oh = oh[:-len(", TRF (")]
                if oh.endswith(", TRF"):
                    oh = oh[:-len(", TRF")]

                # Add to datafame 
                df.loc[len(df.index)] = [name, office, phone, email, oh]

        # remove '@calpoly.edu' from Email column
        df['Email'] = df['Email'].str.replace('@calpoly.edu', '') 
        
        # add title column
        df = add_title(df, "https://schedules.calpoly.edu/all_person_76-CSM_curr.htm", False)

        return df


def read_cs_prof():
        url = "http://frank.ored.calpoly.edu/CSSESpring2022.htm"
        df = pd.read_html(url, skiprows = 2, header=0)[0]

        # clean dataframe 
        df = df.dropna(axis=1, how='all')
        df = df.dropna(axis=0, how='all')
        df = df.iloc[:-3]

        # clean dataframe values
        df = df.applymap(lambda x: " ".join(x.strip().split()) if isinstance(x, str) else x)
        df['Email'] = df['Email'].str.replace('@', '')
        
        # add full phone number (instead of last 5 digits)
        df['Phone'].replace('none', np.nan, inplace=True)
        df['Phone'] = "80575" + df.Phone.map(str, na_action='ignore')

        # convert Monday, Tuesday, Wednesday, ... to Office Hours (ex: MTW 3:00-4:00 pm)
        df['OfficeHours'] = ""
        for i, row in df.iterrows():
            # key: time (ie 3:00-4:00 pm) and value: days of week (ie "MWF")
            officehrs = {}
            if pd.notna(row['Monday']):
                key = clean_oh(row['Monday'])
                if key:
                    officehrs[key] = "M"
            if pd.notna(row['Tuesday']):
                key = clean_oh(row['Tuesday'])
                if key:
                    if key not in officehrs:
                        officehrs[key] = "T"
                    else:
                        officehrs[key] = officehrs.get(key) + "T"
            if pd.notna(row['Wednesday']):
                key = clean_oh(row['Wednesday'])
                if key: 
                    if key not in officehrs:
                        officehrs[key] = "W"
                    else:
                        officehrs[key] = officehrs.get(key) + "W"
            if pd.notna(row['Thursday']):
                key = clean_oh(row['Thursday'])
                if key:
                    if key not in officehrs:
                        officehrs[key] = "R"
                    else:
                        officehrs[key] = officehrs.get(key) + "R"
            if pd.notna(row['Friday']):
                key = clean_oh(row['Friday'])
                if key: 
                    if key not in officehrs:
                        officehrs[key] = "F"
                    else:
                        officehrs[key] = officehrs.get(key) + "F"

            # create string from dict -> {'3:00-4:00pm': 'MWF', '10:00-12:00pm': 'TR'} -> "MWF 3:00-4:00pm, TR 10:00-12:00pm"
            oh_string = ""
            for key, value in officehrs.items():
                text = value + " " + key + ", "
                oh_string += text
            oh_string = oh_string.rstrip(', ')
            row['OfficeHours'] = oh_string
      
        df.drop(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], axis=1, inplace=True)
        df.rename(columns={'How to Connnect':'HowToConnect'}, inplace=True)

        # add title column
        df = add_title(df, "https://schedules.calpoly.edu/all_person_52-CENG_curr.htm", True)

        return df

def clean_oh(txt):
        clean_txt = txt.replace(" ", "").replace(":00", "")
        # remove certain strings
        clean_txt = clean_txt.replace("orbyappt.", "").replace("NoScheduledOfficeHours", "").replace("orbyappointment", "")
        # add space after "M" -> '92-333:10-11AM14-213:3-4PM ' -> '92-333:10-11AM 14-213:3-4PM'
        clean_txt = clean_txt.replace("M", "M ").strip()
        return clean_txt            

def add_title(df, url, updateNames):
        myRequest = requests.get(url)
        soup = BeautifulSoup(myRequest.text,"html.parser")
        table = soup.find_all('table')[0]
         
        # Store titles in two dictionaries: 1 were the keys are the names
        # and the 2nd were keys are the emails
        # majority works just by email
        # but can't just do by email since there is a discreptancy for Eckhardt,
        # Christian -> eckhardt vs cekhardt
        titlesByName = {}
        titlesByAlias = {}

        rows = table.find_all('tr')
        for row in rows:
            personNameHTML = row.find('td', attrs={'class':'personName'})
            if personNameHTML is not None:
                personName = " ".join(personNameHTML.string.strip().split())
            else:
                continue

            personTitle = row.find('td', attrs={'class':'personTitle'}).string
          
            personAlias = row.find('td', attrs={'class':'personAlias'}).string.strip()
            
            titlesByName[personName] = personTitle
            titlesByAlias[personAlias] = personTitle
        
        # add titles to df (either by name or by email)
        df["Title"] = ""
        for index, row in df.iterrows():
            if row['Email'] in titlesByAlias.keys():
                row['Title'] = titlesByAlias.get(row['Email'])
            if row['Name'] in titlesByName.keys():
                row['Title'] = titlesByName.get(row['Name'])
            else:
                continue
        
        if updateNames:
            df['Name'] = df['Name'].apply(lambda x: " ".join(x.split(", ")[::-1]) if isinstance(x, str) else x)

        # see which teachers weren't included in the Instructors list and don't have a title
        # print(df.loc[df['Title'] == ""])      
        return df            

def sqlquote(value):
    """Naive SQL quoting
    All values except NULL are returned as SQL strings in single quotes,
    with any embedded quotes doubled.
    """
    if value is None:
         return 'NULL'
    return "'{}'".format(str(value).replace("'", "''")) 

 
def populate_teacher(connection, df):
        df = df.replace([np.nan], [None])
        df = df.replace([''], [None])
        with connection.cursor() as cursor:
            # create Teacher table if it doesn't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS Teacher (Name VARCHAR(45) PRIMARY KEY, Room VARCHAR(5), Building VARCHAR(5), Phone VARCHAR(10), Email VARCHAR(45), Title VARCHAR(45), OfficeHours VARCHAR(65), HowToConnect VARCHAR(65) );")
            
            # iterate through df and insert row by row
            for i, row in df.iterrows():
                building, room = row['Office'].split("-")
                sql = "INSERT INTO Teacher VALUES (" + sqlquote(row['Name']) + ", " + sqlquote(room) + ", " + sqlquote(building) + ", " + sqlquote(row['Phone']) + ", " + sqlquote(row['Email']) + ", " + sqlquote(row['Title']) + ", " + sqlquote(row['OfficeHours']) + ", " + sqlquote(row['HowToConnect']) + ");"
                cursor.execute(sql)
            
            connection.commit()


def main():
        # Scrape professor info into a pandas df
        stat_df = read_stat_prof()
        print(stat_df)
        cs_df = read_cs_prof()
        all_df = pd.concat([stat_df, cs_df], ignore_index=True)
        print(all_df)
        
        # Connect to the database (using Joao's database)
        '''connection = pymysql.connect(host='localhost',
                                 user='aarsky466',
                                 password='aarsky466985',
                                 database='aarsky466',
                                 cursorclass=pymysql.cursors.DictCursor)'''
        
        connection = pymysql.connect(
                user     = "jcavalca466",
                password = "jcavalca466985",
                host     = "localhost",
                db       = "jcavalca466")

        # Populate Teacher SQL table
        with connection:
            populate_teacher(connection, all_df)


if __name__ == '__main__':
        main()
