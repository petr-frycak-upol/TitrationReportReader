import trr_fileio

if __name__ != '__main__': print("Import of trr successful")
report_file = "D:\\python_projects\\report.rpt"
temp_file = "D:\\python_projects\\report_extract.txt"

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
        if volume0 == volume1: continue #např. v Ti_0002 je jeden řádek zapsaný dvakrát - chyba firmwaru titrátoru
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
    data = sec_derivative[min(min_index, max_index):max(min_index, max_index)]
    j = 0
    for i in range(len(data) - 1):
        # vezme vždy druhou hodnotu v daném a za ním následujícím tuplu, vynásobí a pokud je hodnota záporná,
        # došlo k překročení osy x
        if data[i][1] * data[i + 1][1] < 0:
            j = i
            break
    if len(data) < 2: return 0 #následující kód potřebuje alespoň dvě hodnoty v seznamu; pokud neobsahuje
    #vracíme nulu
    x1, y1 = data[j]
    x2, y2 = data[j + 1]
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    extrap = -b / m
    return extrap

def get_titration_curve(report_file: str) -> list[float]:
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
    titration_curve = get_titration_curve(data) # vytvoření titrační křivky
    sec_derivation = calc_n_der(titration_curve, 2) # výpočet druhé derivace
    eq_point = find_eq_point(sec_derivation) # výpočet bodu titrace
    if eq_point == 0: return None
    return (titration_curve, sec_derivation, eq_point)

