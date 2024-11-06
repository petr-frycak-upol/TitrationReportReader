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

def min_max_index(data):
    min_index, max_index = 0, 0
    for i in range(len(data)):
        if data[i][1] < data[min_index][1]:
            min_index = i
        if data[i][1] > data[max_index][1]:
            max_index = i
    return min_index, max_index


def find_eq_point(sec_derivative):
    (min_index, max_index) = min_max_index(sec_derivative)
    data = sec_derivative[min_index:max_index]
    for i in range(len(data) - 1):
        # vezme vždy druhou hodnotu v daném a za ním následujícím tuplu, vynásobí a pokud je hodnota záporná, došlo k překročení osy x
        if data[i][1] * data[i + 1][1] < 0:
            break
    x1, y1 = data[i]
    x2, y2 = data[i + 1]
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    extrap = -b / m
    return extrap

print(find_eq_point(Calc_n_Der(titration_data, 2)))