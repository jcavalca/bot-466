r_fd = open('test.out', 'r')
responses = r_fd.read()
r_fd.close
responses = responses.split("\n")
res = []
for r in responses[2:]:
    if r != "" and r != "Ask another question!":
        res.append(r)

a_fd = open('test_cases.txt', 'r')
answers = a_fd.read()
a_fd.close()
answers = answers.split("\n")[:-1]
ans = [x.split("|")[1] for x in answers]

assert len(res) == len(res)

correct = 0
for i in range(len(res)):
    if res[i] == ans[i]:
        correct += 1
    else:
        print("query:",answers[i].split("|")[0])
        print("expected:",ans[i])
        print("actual:",res[i])
        print()

print(correct, "correct out of ", len(res))
print("accuracy:", round(correct/len(res), 2))
