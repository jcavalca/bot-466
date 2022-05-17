import subprocess


subprocess.run("python3 ./drop_tables.py".split())
subprocess.run("python3 ./create_table.py".split(),stdout=subprocess.DEVNULL)
print('Tables created.')
subprocess.run("python3 ./populateTeacher.py".split(),stdout=subprocess.DEVNULL)
print('Teacher information populated.')
subprocess.run("python3 ./populate_courses.py".split(),stdout=subprocess.DEVNULL)
print('Course information populated.')
subprocess.run("python3 ./populate_sections.py".split(),stdout=subprocess.DEVNULL)
print('Section information populated.')
print('Finished!')
