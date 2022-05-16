import subprocess


subprocess.run("python3 ./drop_tables.py".split())
subprocess.run("python3 ./create_table.py".split())
subprocess.run("python3 ./populateTeacher.py".split())
subprocess.run("python3 ./populate_courses.py".split())
subprocess.run("python3 ./populate_sections.py".split())