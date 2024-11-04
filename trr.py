import trr_fileio

titration_data = []
report_file = "D:\\python_projects\\report.rpt"
temp_file = "D:\\python_projects\\report_extract.txt"
VOLUME_INDEX = 1
PH_INDEX = 3


def process_line(line):
    s = line.split()
    titration_data.append((float(s[VOLUME_INDEX]), float(s[PH_INDEX])))
    


def Calc_n_Der(data, n):
    if n == 0:
        return data

    output = []
    for i in range(len(data)-1):
        (volume0, ph0) = data[i]
        (volume1, ph1) = data[i+1]

        x = (ph1 - ph0) / (volume1 - volume0)
        output.append(((volume1 + volume0) / 2, x))

    return Calc_n_Der(output, n-1)



def find_eq_point(sec_derivative):
    for i in range(len(sec_derivative) - 1):
        # vezme vždy druhou hodnotu v daném a za ním následujícím tuplu, vynásobí a pokud je hodnota záporná, došlo k překročení osy x
        if sec_derivative[i][1] * sec_derivative[i + 1][1] < 0:
            break
    x1, y1 = sec_derivative[i]
    x2, y2 = sec_derivative[i + 1]
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return -b / m


lines = trr_fileio.read_file(report_file)

line_interesting = False

for line in lines:
    if line_interesting:
        if line == "":
            line_interesting = False
        else:
            process_line(line)
    else:
        if ("Volume" in line and "pH" in line):
            line_interesting = True
            #print(line.split())

print(titration_data)
trr_fileio.write_file(titration_data, temp_file)
