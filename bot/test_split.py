fd = open('test_cases.txt', 'r')
tests = fd.read()
fd.close

q_fd = open('test.in', 'w')

for test in tests.split("\n"):
    if test != "":
        q_fd.write(test.split("|")[0]+"\n")

q_fd.write('exit\n')
q_fd.close()
        
