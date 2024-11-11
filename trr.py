import trr_fileio

titration_data = []
report_file = "D:\\python_projects\\report.rpt"
temp_file = "D:\\python_projects\\report_extract.txt"
VOLUME_INDEX = 1
PH_INDEX = 3


def process_line(line):
    s = line.split()
    titration_data.append((float(s[VOLUME_INDEX]), float(s[PH_INDEX])))




def calc_n_der(data, n = 1):
    if n>1: return calc_n_der(calc_n_der(data, 1), n-1)
    else:
        output=[]
        for i in range(len(data)-1):
            (x0, y0) = data[i]
            (x1, y1) = data[i+1]
            d = ((y1-y0)/(x1-x0))
            output.append(((x1+x0)/2, d))
        return output

def CalcFirstDer(data):
    output = []
    for i in range(len(data)-1):
        (volume0, ph0) = data[i]
        (volume1, ph1) = data[i+1]
        d = ((ph1-ph0)/(volume1-volume0))
        output.append(((volume1+volume0)/2, d))
    return output


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
            # print(line.split())

print(titration_data)
trr_fileio.write_file(titration_data, temp_file)

#sd = CalcSecondDer(CalcFirstDer(titration_data))
#print(find_eq_point(CalcSecondDer(CalcFirstDer(titration_data))))

acc = 0

#for i in range(len(sd) - 1):
#    if sd[i][1] * sd[i + 1][1] < 0: acc += 1

print(calc_n_der(titration_data, 2))
