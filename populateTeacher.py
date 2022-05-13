import pandas as pd, requests, sys
from bs4 import BeautifulSoup

def read_stat_oh():
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

                # 3) GET PHONE
                phone = values[2].text.strip()

                # 4) GET EMAIL
                email = values[3].text.strip()

                # 5) GET OFFICE HOURS                  
                oh = values[4].find_all('strong')
                oh = ", ".join([item.strip() for items in oh for item in items])

                # Add to datafame 
                df.loc[len(df.index)] = [name, office, phone, email, oh]

        # remove '@calpoly.edu' from Email column
        df['Email'] = df['Email'].str.replace('@calpoly.edu', '') 
        return df


def read_cs_oh():
        url = "http://frank.ored.calpoly.edu/CSSESpring2022.htm"
        df = pd.read_html(url, skiprows = 2, header=0)[0]

        # clean dataframe 
        df = df.dropna(axis=1, how='all')
        df = df.dropna(axis=0, how='all')
        df = df.iloc[:-3]

        # clean dataframe values
        df = df.applymap(lambda x: " ".join(x.strip().split()) if isinstance(x, str) else x)
        df['Email'] = df['Email'].str.replace('@', '')
        
        # convert Monday, Tuesday, Wednesday, ... to Office Hours
        df['OfficeHours'] = ""
        for i, row in df.iterrows():
            officehrs = ""
            if pd.notna(row['Monday']):
                text = "M " + row['Monday'].replace(" ", "") + ", "
                officehrs += text
            if pd.notna(row['Tuesday']):
                text = "T " + row['Tuesday'].replace(" ", "") + ", "
                officehrs += text
            if pd.notna(row['Wednesday']):
                text = "W " + row['Wednesday'].replace(" ", "") + ", "
                officehrs += text
            if pd.notna(row['Thursday']):
                text = "R " + row['Thursday'].replace(" ", "") + ", "
                officehrs += text
            if pd.notna(row['Friday']):
                officehrs += "F " + row['Friday'].replace(" ", "")
            officehrs = officehrs.rstrip(', ')
            row['OfficeHours'] = officehrs
        df.drop(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], axis=1, inplace=True)       
 
        return df

def add_title(df, url):
        myRequest = requests.get(url)
        soup = BeautifulSoup(myRequest.text,"html.parser")
        table = soup.find_all('table')[0]
         
        # Store titles in two dictionaries: 1 were the keys are the names
        # and the 2nd were keys are the emails
        # majority works just by name
        # but also do by email since there are discreptancies in the names
        # ie Chris Lupo vs Christopher Lupo
        # can't just do by email since there is a discreptancy for Eckhardt,
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
            if row['Name'] in titlesByName.keys():
                row['Title'] = titlesByName.get(row['Name'])
            if row['Email'] in titlesByAlias.keys():
                row['Title'] = titlesByAlias.get(row['Email'])
            else:
                continue
        
        # see which teachers weren't included in the Instructors list and don't have a title
        # print(df.loc[df['Title'] == ""])      
        return df            
  

        

def main():
        stat_df = read_stat_oh()
        stat_df = add_title(stat_df, "https://schedules.calpoly.edu/all_person_76-CSM_curr.htm")
        print(stat_df)
        cs_df = read_cs_oh()
        cs_df = add_title(cs_df, "https://schedules.calpoly.edu/all_person_52-CENG_curr.htm")
        print(cs_df)

if __name__ == '__main__':
        main()
