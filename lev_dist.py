# smaller number out put means closer distance
def lev_dist(str1, str2):
    if len(str1) < len(str2):
        return lev_dist(str2, str1)
    if len(str2) == 0:
        return len(str1)
    prev_row = range(len(str2) + 1)
    for i, chr1 in enumerate(str1):
        curr_row = [i + 1]
        for j, chr2 in enumerate(str2):
            curr_row.append(min(
            prev_row[j + 1] + 1,
            curr_row[j] + 1,
            prev_row[j] + (1 if chr1 != chr2 else 0)))
        prev_row = curr_row
    
    return prev_row[-1]

print(lev_dist("Nico", "Naco"))