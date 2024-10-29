import trr_fileio

titration_data = []
report_file = "D:\\python_projects\\report.rpt"
temp_file = "D:\\python_projects\\report_extract.txt"
VOLUME_INDEX = 1
PH_INDEX = 3

def process_line(line):
    s = line.split()
    titration_data.append((float(s[VOLUME_INDEX]), float(s[PH_INDEX])))
    

lines = trr_fileio.read_file(report_file)

line_interesting = False

for line in lines:
    if line_interesting:
        if line == "": line_interesting = False
        else:
            process_line(line)
    else:
        if ("Volume" in line and "pH" in line):
            line_interesting = True
            #print(line.split())

def CalcSeconder(data):
    output=[]
    for i in range(len(data)-1):
        (volume0, derivation0) = data[i]
        (volume1, derivation1) = data[i+1] 
        x = ((derivation1-derivation0)/(volume1-volume0))
        output.append(((volume1-volume0)/2, x))
        return output

print(titration_data)
trr_fileio.write_file(titration_data, temp_file)

def find_eq_point(numbers):
    pos_closest = min(x for x in numbers if x >= 0)
    neg_closest = max(x for x in numbers if x < 0)

    pos_index = numbers.index(pos_closest)
    neg_index = numbers.index(neg_closest)

    print(pos_closest, neg_closest)
    
    if pos_index < neg_index:
        x1, y1 = neg_closest, numbers[neg_index]
        x2, y2 = pos_closest, numbers[pos_index]
    else:
        x1, y1 = pos_closest, numbers[pos_index]
        x2, y2 = neg_closest, numbers[neg_index]

    y = y1 + (0 - x1) * (y2 - y1) / (x2 - x1)
    return y