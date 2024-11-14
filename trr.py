import trr_fileio

if __name__ != '__main__': print("Import of trr successful")
report_file = "C:\\Users\\kubak\\Desktop\\Škola\\Navazující\\1.ZS\\PNAC\\Projekty\\report_extract.txt"
temp_file = "C:\\Users\\kubak\\Desktop\\Škola\\Navazující\\1.ZS\\PNAC\\Projekty\\report.RPT"
VOLUME_INDEX = 1
PH_INDEX = 3


def process_line(line, titration_data):
    s = line.split()
    titration_data.append((float(s[VOLUME_INDEX]), float(s[PH_INDEX])))

def calc_n_der(data, n = 1):
    if n == 0:
        return data

    output = []
    for i in range(len(data)-1):
        (volume0, ph0) = data[i]
        (volume1, ph1) = data[i+1]

        x = (ph1 - ph0) / (volume1 - volume0)
        output.append(((volume1 + volume0) / 2, x))

    return calc_n_der(output, n - 1)

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
        # vezme vždy druhou hodnotu v daném a za ním následujícím tuplu, vynásobí a pokud je hodnota záporná,
        # došlo k překročení osy x
        if data[i][1] * data[i + 1][1] < 0:
            break
    x1, y1 = data[i]
    x2, y2 = data[i + 1]
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    extrap = -b / m
    return extrap

def get_titration_curve(report_file):
    titration_data = []
    lines = trr_fileio.read_file(report_file)

    line_interesting = False

    for line in lines:
        if line_interesting:
            if line == "":
                line_interesting = False
            else:
                process_line(line, titration_data)
        else:
            if ("Volume" in line and "pH" in line):
                line_interesting = True
                # print(line.split())

    return titration_data
    #print(titration_data)
    #trr_fileio.write_file(titration_data, temp_file)

def secder_eqpoint(data):
    parameters = []
    titration_curve = get_titration_curve(data) # vytvoření titrační křivky
    sec_derivation = calc_n_der(titration_curve, 2) # výpočet druhé derivace
    eq_point = find_eq_point(sec_derivation) # výpočet bodu titrace
    parameters.append([titration_curve, sec_derivation, eq_point]) # vytvoření seznamu trojic hodnot
    
    return parameters