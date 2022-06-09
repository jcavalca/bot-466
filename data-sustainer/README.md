# Data Sustainer - CSC 466 Project Calpass

Data sustainer scrapes data from Cal Poly website pages and populates our MySQL DB.

### Code Structure

* **DB_create.sql** : SQL queries for creation of all tables for our DB.
* **DB_drop.sql** : SQL queries for drop of all tables for our DB.
* **create_table.py** : Using DB_create.sql, this script creates all tables.
* **drop_tables.py** : Using DB_drop.sql, this script drops all tables.
* **getData.py** : Driver file, it puts everything together. I.e., performs all scraping and population of DB. 
* **populateTeacher.py** : Scrapes pages associated with teachers and populates Teacher table. 
* **populate_courses.py** : Scrapes pages associated with courses and populates Courses table.
* **populate_sections.py** : Scrapes pages associated with sections and populates Sections table. 


### Usage

```python 
python3 getData.py
```
