import trr_fileio

titration_data = []
report_file = "D:\\python_projects\\report.rpt"
temp_file = "D:\\python_projects\\report_extract.txt"
VOLUME_POS = 1
PH_POS = 3

def process_line(line):
    s = line.split()
    titration_data.append((float(s[VOLUME_POS]), float(s[PH_POS])))
    

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
