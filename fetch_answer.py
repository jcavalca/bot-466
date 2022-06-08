import db


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
    answer = list(map(lambda d: d[0], db.executeSelect(sql)))

    # print output
    if len(answer) == 0 or answer[0] is None:
        print("Sorry, I don't know the answer.")
    else:
        if intent_class == 0 or intent_class == 1:
            print(f"""{name}'s {var.lower()} for office hours is {var} {answer[0]}.""")
        if intent_class == 7:
            print(f"""{name}'s office hours are {answer[0]}.""")
        if intent_class == 11:
            print(f"""{name}'s {var.lower()} is {answer[0]}@calpoly.edu.""")
        if intent_class == 12 or intent_class == 18:
            print(f"""{name}'s {var.lower()} number is {answer[0]}.""")
        if intent_class == 13:
            print(f"""The best way to connect with {name} is {answer[0].lower()}.""")


def fetch_section_answer(var_map, intent_class):
    # Determine quarter
    if var_map.get('[Quarter]') is None:
        quarter = 'Spring'
    else:
        quarter = var_map.get('[Quarter]')

    # 3: "Which courses are [CSSE-Faculty] teaching [Quarter] quarter?"
    if intent_class == 3:
        faculty = var_map.get('[CSSE-Faculty]')
        print(quarter, faculty)
        sql = f"""SELECT CoursePrefix, CourseNumberPrefix FROM Section 
                    WHERE Teacher = '{faculty}'
                    AND Quarter = '{quarter}'"""
        print(sql)
        answer = list(map(lambda d: (d[0], d[1], d[2]), db.executeSelect(sql)))

        if len(answer) == 0:
            print("Sorry, I don't know the answer.")
        elif answer is None:
            print(f"{faculty} does not teach any courses {quarter} quarter.")
        else:
            if len(answer) > 1:
                courses = ", ".join([f"{item[0]} {item[1]}-{item[2]}" for item in answer[:-1]]) + " and " + answer[-1]
            else:
                courses = answer[0]
            print(f"""{faculty} is teaching the following courses in {quarter} quarter: {courses}.""")

    else:
        prefix = var_map.get('[PREFIX]')

        # 4: "What [PREFIX] courses are offered [Quarter] quarter?"
        # 5: "Which [PREFIX] courses start at [Time] [Quarter] quarter?"
        # 6: "Which [PREFIX] courses end at [Time] [Quarter] quarter?"
        if intent_class == 4 or intent_class == 5 or intent_class == 6:
            generic_sql = f"""SELECT DISTINCT CoursePrefix, CourseNumberPrefix FROM Section 
                                    WHERE CoursePrefix = '{prefix}'
                                    AND Quarter = '{quarter}'"""
            time = var_map.get('[Time]')
            if intent_class == 5:
                add = f"""AND StartTime = '{time}'"""
            elif intent_class == 6:
                add = f"""AND EndTime = '{time}'"""
            else:
                add = ""
            sql = f"""{generic_sql}\t{add}"""
            answer = list(map(lambda d: (d[0], d[1]), db.executeSelect(sql)))
            #answer = list()
            #for row in db.executeSelect(sql):
            #    answer.append(tuple(row['CoursePrefix'], row['CourseNumberPrefix']))
            if len(answer) == 0:
                print("Sorry, I don't know the answer.")
            elif answer is None:
                print(f"""No {prefix.upper()} courses {quarter} quarter follow that criteria.""")
            else:
                if len(answer) > 1:
                    courses = ", ".join([f"{item[0]} {item[1]}" for item in answer[:-1]]) + " and " + answer[-1]
                else:
                    courses = answer[0]
                if intent_class == 4:
                    print(f"""The following {prefix.upper()} courses are offered {quarter} quarter: {courses}.""")
                if intent_class == 5:
                    print(f"""The following {prefix.upper()} courses start at {time} {quarter} quarter: {courses}.""")
                if intent_class == 6:
                    print(f"""The following {prefix.upper()} courses end at {time} {quarter} quarter: {courses}.""")

        course_num = var_map.get('[CourseNum]')

        # 2: "Who is teaching [PREFIX] [CourseNum] [Quarter] quarter?"
        if intent_class == 2:
            sql = f"""SELECT DISTINCT Teacher FROM Section 
                            WHERE Quarter = '{quarter}'
                            AND CoursePrefix = '{prefix}'
                            AND CourseNumberPrefix = '{course_num}'"""
            answer = list(map(lambda d: d[0], db.executeSelect(sql)))
            if len(answer) == 0:
                print("Sorry, I don't know the answer.")
            elif answer is None:
                print(f"""No faculty teach {prefix.upper()} {course_num} {quarter} quarter.""")
            else:
                if len(answer) > 1:
                    teachers = ", ".join(answer[:-1]) + " and " + answer[-1]
                else:
                    teachers = answer[0]
                print(f"""The following faculty teach {prefix.upper()} {course_num} {quarter} quarter: {teachers}.""")

        # 16: "What's the room for [PREFIX][CourseNum]-[Section] [Quarter] quarter?"
        # 17: "What's the building for [PREFIX][CourseNum]-[Section] [Quarter] quarter?"
        # 19: "What's the type of [PREFIX][CourseNum]-[Section] [Quarter] quarter?"
        if intent_class == 16 or intent_class == 17 or intent_class == 19:
            section = var_map.get('[Section]')
            if intent_class == 16:
                var = 'Room'
            if intent_class == 17:
                var = 'Building'
            if intent_class == 19:
                var = 'Type'
            sql = f"""SELECT {var} FROM Section 
                            WHERE Quarter = '{quarter}'
                            AND CoursePrefix = '{prefix}'
                            AND CourseNumberPrefix = '{course_num}'
                            AND Number = '{section}'"""
            answer = list(map(lambda d: d[0], db.executeSelect(sql)))
            if len(answer) == 0:
                print("Sorry, I don't know the answer.")
            else:
                if intent_class == 16 or intent_class == 17:
                    print(f"""The {var.lower()} for {prefix.upper()} {course_num}-{section} is {var} {answer[0]}.""")
                if intent_class == 19:
                    print(f"""{prefix.upper()} {course_num}-{section} is a {answer[0]}.""")

        # 8: "When is [PREFIX] [CourseNum] [CourseType] offered [Quarter] quarter?"
        if intent_class == 8:
            course_type = var_map.get('[CourseType]')
            sql = f"""SELECT Days, StartTime, EndTime FROM Section 
                                        WHERE Quarter = '{quarter}'
                                        AND CoursePrefix = '{prefix}'
                                        AND CourseNumberPrefix = '{course_num}'
                                        AND Type = '{course_type}'"""
            print(sql)
            answer = list(map(lambda d: (d[0], d[1], d[2]), db.executeSelect(sql)))
            # answer = list()
            # for row in db.executeSelect(sql):
            #    answer.append(tuple(row['Days'], row['StartTime'], row['EndTime']))
            if len(answer) == 0 or answer[0] is None:
                print("Sorry, I don't know the answer.")
            else:
                if len(answer) > 1:
                    times = ", ".join([f"{item[0]} {item[1]}-{item[2]}" for item in answer[:-1]]) + " and " + answer[-1]
                else:
                    times = answer[0]
                print(
                    f"""{prefix.upper()} {course_num} {course_type}s {quarter} quarter are offered during the following times: {times}.""")

        # 15: "How many sections of [PREFIX] [CourseNum] are offered [Quarter] quarter?"
        if intent_class == 15:
            sql = f"""SELECT COUNT(*) AS Count FROM Section 
                            WHERE Quarter = '{quarter}'
                            AND CoursePrefix = '{prefix}'
                            AND CourseNumberPrefix = '{course_num}'"""
            answer = list(map(lambda d: d[0], db.executeSelect(sql)))
            if len(answer) == 0 or answer[0] is None:
                print("Sorry, I don't know the answer.")
            else:
                print(f"""There are {answer[0]} sections of {prefix.upper()} {course_num} offered {quarter} quarter.""")


def fetch_course_answer(var_map, intent_class):
    prefix = var_map.get('[PREFIX]')
    course_num = var_map.get('[CourseNum]')

    if intent_class == 9:
        var = 'Prereq'
    if intent_class == 10:
        var = 'Units'
    if intent_class == 14:
        var = 'CourseDesc'

    # sql query
    sql = f"""SELECT {var} FROM Course 
                        WHERE Prefix = '{prefix}'
                        AND Number = '{course_num}'"""
    answer = list(map(lambda d: d[0], db.executeSelect(sql)))

    # print output
    if len(answer) == 0 or answer[0] is None:
        print("Sorry, I don't know the answer.")
    else:
        # 9: "What are the pre requisites for [PREFIX] [CourseNum]?"
        if intent_class == 9:
            print(f"""The pre-requisites for {prefix.upper()} {course_num} are {answer[0]}""")
        # 10: "How many units is [PREFIX] [CourseNum]?"
        if intent_class == 10:
            print(f"""{prefix.upper()} {course_num} is {answer[0]} units.""")
        # 14: "What is the course description for [PREFIX] [CourseNum]?"
        if intent_class == 14:
            print(f"""The course description for {prefix.upper()} {course_num} is {answer[0]}.""")
