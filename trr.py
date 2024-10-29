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

print(titration_data)
trr_fileio.write_file(titration_data, temp_file)

def CalcFirstDer(data):
    output = []
    for i in range(len(data)-2):
        (volume0, ph0) = data[i]
        (volume1, ph1) = data[i+1]
        d = ((ph1-ph0)/(volume1-volume0))
        output.append((volume1-volume0)/2, abs(d))
    return output