import trr_fileio


lines = []
titration_data = []
report_file = "d:\\python_projects\\report.rpt"
temp_file = "D:\\python_projects\\report_extract.txt"

def process_line(line):
    s = line.split()
    titration_data.append((float(s[1]), float(s[3])))
    



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
