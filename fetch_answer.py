import calpass


def fetch_teacher_answer(var_map, intent_class):
    name = var_map.get('[CSSE-Faculty]')

    # 0: "What's the room for [CSSE-Faculty] office hours?"
    if intent_class == 0:
        var = 'Room'
    # 1: "What building is [CSSE-Faculty] office hours?"
    if intent_class == 1:
        var = 'Building'
    # 7: "What time is [CSSE-Faculty] office hours?"
    if intent_class == 7:
        var = 'OfficeHours'
    # 11: "What is [CSSE-Faculty]'s email?"
    if intent_class == 11:
        var = 'Email'
    # 12: "What is [CSSE-Faculty]'s phone?"
    if intent_class == 12:
        var = 'Phone'
    # 13: "How can I reach [CSSE-Faculty]?"
    if intent_class == 13:
        var = 'HowToConnect'
    # 18: "What's the title of [CSSE-Faculty]?"
    if intent_class == 18:
        var = 'Title'

    # sql query
    sql = f"""SELECT {var} FROM Teacher WHERE Name = '{name}'"""
    answer = list(map(lambda d: d[0], calpass.executeSelect(sql)))

    # print output
    if len(answer) == 0:
        print("Sorry, I don't know the answer.")
    else:
        if intent_class == 0 or intent_class == 1:
            print(f"""{name}'s {var.lower()} for office hours is {var} {answer[0]}.""")
        if intent_class == 7:
            print(f"""{name}'s office hours are {answer[0]}.""")
        if intent_class == 11:
            print(f"""{name}'s {var.lower()} is {answer[0]}@calpoly.edu.""")
        if intent_class == 12 or intent_class == 18:
            print(f"""{name}'s {var.lower()} is {answer[0]}.""")
        if intent_class == 13:
            print(f"""The best way to connect with {name} is {answer[0].lower()}.""")


def fetch_section_answer(var_map, intent_class):
    # Determine quarter
    if var_map.get('[Quarter]') is None:
        Quarter = 'Spring'
    else:
        Quarter = var_map.get('[Quarter]')

    # 3: "Which courses are [CSSE-Faculty] teaching [Quarter] quarter?"
    if intent_class == 3:
        Faculty = var_map.get('[CSSE-Faculty]')
        sql = f"""SELECT CoursePrefix, CourseNumberPrefix, Number FROM Section 
                    WHERE Teacher = '{Faculty}'
                    AND Quarter = '{Quarter}'"""
        # answer = list(map(lambda d: (d['CoursePrefix'], d['CourseNumberPrefix'], d['Number']), calpass.executeSelect(sql)))
        answer = list()
        for row in calpass.executeSelect(sql):
            answer.append(tuple(row['CoursePrefix'], row['CourseNumberPrefix'], row['Number']))
        if len(answer) == 0:
            print("Sorry, I don't know the answer.")
        else:
            courses = ", ".join([f"{item[0]} {item[1]}-{item[2]}" for item in answer])
            print(f"""{Faculty} is teaching the following courses in {Quarter} quarter: {courses}.""")

    else:
        PREFIX = var_map.get('[PREFIX]')

        # 4: "What [PREFIX] courses are offered [Quarter] quarter?"
        # 5: "Which [PREFIX] courses start at [Time] [Quarter] quarter?"
        # 6: "Which [PREFIX] courses end at [Time] [Quarter] quarter?"
        if intent_class == 4 or intent_class == 5 or intent_class == 6:
            generic_sql = f"""SELECT DISTINCT CoursePrefix, CourseNumberPrefix FROM Section 
                                    WHERE CoursePrefix = '{PREFIX}'
                                    AND Quarter = '{Quarter}'"""
            add = ""
            Time = var_map.get('[Time]')
            if intent_class == 5:
                add = f"""AND StartTime = '{Time}'"""
            if intent_class == 6:
                add = f"""AND EndTime = '{Time}'"""
            sql = f"""{generic_sql}\t{add}"""
            # answer = list(map(lambda d: (int(d['CoursePrefix']), int(d['CourseNumberPrefix'])), calpass.executeSelect(sql)))
            answer = list()
            for row in calpass.executeSelect(sql):
                answer.append(tuple(row['CoursePrefix'], row['CourseNumberPrefix']))
            if len(answer) == 0:
                print("Sorry, I don't know the answer.")
            else:
                courses = ", ".join([f"{item[0]} {item[1]}" for item in answer])
                if intent_class == 4:
                    print(f"""The following {PREFIX} courses are offered {Quarter} quarter: {courses}.""")
                if intent_class == 5:
                    print(f"""The following {PREFIX} courses start at {Time} {Quarter} quarter: {courses}.""")
                if intent_class == 6:
                    print(f"""The following {PREFIX} courses end at {Time} {Quarter} quarter: {courses}.""")

        CourseNum = var_map.get('[CourseNum]')

        # 2: "Who is teaching [PREFIX] [CourseNum] [Quarter] quarter?"
        if intent_class == 2:
            sql = f"""SELECT DISTINCT Teacher FROM Section 
                            WHERE Quarter = '{Quarter}'
                            AND CoursePrefix = '{PREFIX}'
                            AND CourseNumberPrefix = '{CourseNum}'"""
            answer = list(map(lambda d: d[0], calpass.executeSelect(sql)))
            if len(answer) == 0:
                print("Sorry, I don't know the answer.")
            else:
                print(f"""The following faculty teach {PREFIX} {CourseNum} {Quarter} quarter: {", ".join(answer)}.""")

        # 16: "What's the room for [PREFIX][CourseNum]-[Section] [Quarter] quarter?"
        # 17: "What's the building for [PREFIX][CourseNum]-[Section] [Quarter] quarter?"
        # 19: "What's the type of [PREFIX][CourseNum]-[Section] [Quarter] quarter?"
        if intent_class == 16 or intent_class == 17 or intent_class == 19:
            Section = var_map.get('[Section]')
            if intent_class == 16:
                var = 'Room'
            if intent_class == 17:
                var = 'Building'
            if intent_class == 19:
                var = 'CourseType'
            sql = f"""SELECT {var} FROM Section 
                            WHERE Quarter = '{Quarter}'
                            AND CoursePrefix = '{PREFIX}'
                            AND CourseNumberPrefix = '{CourseNum}'
                            AND Number = '{Section}'"""
            answer = list(map(lambda d: d[0], calpass.executeSelect(sql)))
            if len(answer) == 0:
                print("Sorry, I don't know the answer.")
            else:
                if intent_class == 16 or intent_class == 17:
                    print(f"""The {var.lower()} for {PREFIX} {CourseNum}-{Section} is {var} {answer[0]}.""")
                if intent_class == 19:
                    print(f"""{PREFIX} {CourseNum}-{Section} is a {answer[0]}.""")

        # 8: "When is [PREFIX] [CourseNum] [CourseType] offered [Quarter] quarter?"
        if intent_class == 8:
            CourseType = var_map.get('[CourseType]')
            sql = f"""SELECT Days, StartTime, EndTime FROM Section 
                                        WHERE Quarter = '{Quarter}'
                                        AND CoursePrefix = '{PREFIX}'
                                        AND CourseNumberPrefix = '{CourseNum}'
                                        AND CourseType == '{CourseType}'"""
            # answer = list(map(lambda d: (d['Days'], d['StartTime'], d['EndTime']), calpass.executeSelect(sql)))
            answer = list()
            for row in calpass.executeSelect(sql):
                answer.append(tuple(row['Days'], row['StartTime'], row['EndTime']))
            if len(answer) == 0:
                print("Sorry, I don't know the answer.")
            else:
                times = ", ".join([f"{item[0]} {item[1]}-{item[2]}" for item in answer])
                print(
                    f"""{PREFIX} {CourseNum} {CourseType} {Quarter} quarter are offered during the following times: {times}.""")

        # 15: "How many sections of [PREFIX] [CourseNum] are offered [Quarter] quarter?"
        if intent_class == 15:
            sql = f"""SELECT COUNT(*) AS Count FROM Section 
                            WHERE Quarter = '{Quarter}'
                            AND CoursePrefix = '{PREFIX}'
                            AND CourseNumberPrefix = '{CourseNum}'"""
            answer = list(map(lambda d: d[0], calpass.executeSelect(sql)))
            if len(answer) == 0:
                print("Sorry, I don't know the answer.")
            else:
                print(f"""There are {answer[0]} sections of {PREFIX} {CourseNum} offered {Quarter} quarter.""")


def fetch_course_answer(var_map, intent_class):
    PREFIX = var_map.get('[PREFIX]')
    CourseNum = var_map.get('[CourseNum]')

    if intent_class == 9:
        var = 'Prereq'
    if intent_class == 10:
        var = 'Units'
    if intent_class == 14:
        var = 'CourseDesc'

    # sql query
    sql = f"""SELECT {var} FROM Course 
                        WHERE Prefix = '{PREFIX}'
                        AND Number = '{CourseNum}'"""
    answer = list(map(lambda d: d[0], calpass.executeSelect(sql)))

    # print output
    if len(answer) == 0:
        print("Sorry, I don't know the answer.")
    else:
        # 9: "What are the pre requisites for [PREFIX] [CourseNum]?"
        if intent_class == 9:
            print(f"""The pre-requisites for {PREFIX}-{CourseNum} are {", ".join(answer)}.""")
        # 10: "How many units is [PREFIX] [CourseNum]?"
        if intent_class == 10:
            print(f"""{PREFIX}-{CourseNum} is {answer[0]} units.""")
        # 14: "What is the course description for [PREFIX] [CourseNum]?"
        if intent_class == 14:
            print(f"""The course description for {PREFIX}-{CourseNum} is {answer[0]}.""")
