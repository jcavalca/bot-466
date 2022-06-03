def fetch_teacher_answer(var_map, intent_class):
    ''' value:
        0 --> Room
        1 --> Building
        7 --> OfficeHours
        11 --> Email
        12 --> Phone
        13 --> HowToConnect
        18 --> Title '''
    name = var_map.get('[CSSE-Faculty]')

    if intent_class == 0:
        var = 'Room'
    if intent_class == 1:
        var = 'Building'
    if intent_class == 7:
        var = 'OfficeHours'
    if intent_class == 11:
        var = 'Email'
    if intent_class == 12:
        var = 'Phone'
    if intent_class == 13:
        var = 'HowToConnect'
    if intent_class == 18:
        var = 'Title'

    sql = f"""SELECT {var} FROM Teacher WHERE Name = '{name}'"""
    return executeSelect(sql)
  
  

def fetch_section_answer(var_map, intent_class):
    # determine quarter
    if var_map.get('[Quarter]') is None:
        Quarter = 'Spring'
    else:
        Quarter = var_map.get('[Quarter]')

    if intent_class == 3:
        sql = f"""SELECT CoursePrefix, CourseNumberPrefix, Number FROM Section 
                    WHERE Teacher = '{var_map.get('[CSSE-Faculty]')}'
                    AND Quarter = '{Quarter}'"""
    else:
        PREFIX = var_map.get('[PREFIX]')

        if intent_class == 4 or intent_class == 5 or intent_class == 6:
            generic_sql = f"""SELECT DISTINCT CoursePrefix, CourseNumberPrefix FROM Section 
                                    WHERE CoursePrefix = '{PREFIX}'
                                    AND Quarter = '{Quarter}'"""
            add = ""
            if intent_class == 5:
                add = f"""AND StartTime = '{var_map.get('[Time]')}'"""
            if intent_class == 6:
                add = f"""AND EndTime = '{var_map.get('[Time]')}'"""
            sql = f"""{generic_sql}\t{add}"""

        CourseNum = var_map.get('[CourseNum]')

        if intent_class == 2:
            sql = f"""SELECT DISTINCT Teacher FROM Section 
                            WHERE Quarter = '{Quarter}'
                            AND CoursePrefix = '{PREFIX}'
                            AND CourseNumberPrefix = '{CourseNum}'"""

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

        if intent_class == 8 or intent_class == 15:
            if intent_class == 8
                var = 'Days, StartTime, EndTime'
            if intent_class == 15:
                var = 'COUNT(*)'
            sql = f"""SELECT {var} FROM Section 
                            WHERE Quarter = '{Quarter}'
                            AND CoursePrefix = '{PREFIX}'
                            AND CourseNumberPrefix = '{CourseNum}'"""

    return executeSelect(sql)
  
  

def fetch_course_answer(var_map, intent_class):
    PREFIX = var_map.get('[PREFIX]')
    CourseNum = var_map.get('[CourseNum]')

    if intent_class == 9:
        var = 'Prereq'
    if intent_class == 10:
        var = 'Units'
    if intent_class == 14:
        var = 'CourseDesc'

    sql = f"""SELECT {var} FROM Course 
                        WHERE Prefix = '{PREFIX}'
                        AND Number = '{CourseNum}'"""
    
    return executeSelect(sql)
