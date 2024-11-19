import glob
import os.path
import matplotlib.pyplot as plt


DEFAULT_ROOT_TAIL_LENGTH = 3


def write_file(data, fullname):
    final_fullname = ""
    folder = os.path.split(fullname)[0]
    filename = os.path.split(fullname)[1]
    rootname = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]

    if os.path.exists(fullname):
        acceptable_answer = False

        while not acceptable_answer:

            answer = input(f"File {filename} exists! Overwrite (O), Rename manually (R), Append number (A), Cancel (C):\n")

            if answer.upper() == "O":
                final_fullname = fullname
                acceptable_answer = True

            elif answer.upper() == "R":
                newname = input("Enter new file name (do not include full path and extension):\n")
                newname += extension
                final_fullname = os.path.join((os.path.split(fullname))[0], newname)
                if not os.path.exists(final_fullname): acceptable_answer = True

            elif answer.upper() == "A":
                final_fullname = provide_valid_filename(folder, rootname, extension)
                acceptable_answer = True

            elif answer.upper() == "C":
                acceptable_answer = True
                print("Cancelled, file not written.")
                return

    with open(final_fullname, mode="w") as f:
        for (volume, ph) in data:
            f.write(str(volume))
            f.write(",")
            f.write(str(ph))
            f.write("\n")
    print(f"File written to {final_fullname}")
        
def provide_valid_filename(folder, rootname, extension):
    is_zero_to_nine = True
    is_valid_filename = False
    ZERO_TO_NINE = "0123456789"

    underscore_rindex = rootname.rfind("_")

    root_head = ""
    root_tail_number = 0
    root_tail_length = DEFAULT_ROOT_TAIL_LENGTH

    if underscore_rindex == -1: #jméno neobsahuje podtržítko
        root_head = rootname + "_"
    elif underscore_rindex == len(rootname)-1: #tj. jméno končí podtržítkem
        root_head = rootname
    else: #jméno obsahuje alespoň jedno podtržítko; žádné není na konci
        root_tail = rootname[underscore_rindex + 1:]
        root_head = rootname[:underscore_rindex - 1]
        for char in root_tail:
            if not char in ZERO_TO_NINE: is_zero_to_nine = False
        if is_zero_to_nine:
            root_tail_length = len(root_tail)
            root_tail_number = int(root_tail)
        else:
            root_head = rootname + "_"

    while True:
        new_root_tail = str(root_tail_number)
        if len(new_root_tail) < root_tail_length:
            new_root_tail = (root_tail_length - len(new_root_tail)) * "0" + new_root_tail
        valid_filename = os.path.join(folder, root_head + new_root_tail + extension)
        if os.path.exists(valid_filename): root_tail_number += 1
        else: break

    return valid_filename


report_directory = "D:\\Python_projects\\HI_931_reports"  # !Nutno změnit pro každé z našich zařízení


def read_directory(report_directory):
    # Tímto se zadefinuje podle čeho má glob hledat soubory v adresáři
    pattern = os.path.join(report_directory, "*.rpt")
    # Použijeme glob aby nám našel všechny rpt soubory v adresáři
    rpt_files = glob.glob(pattern)
    return rpt_files


def read_file(fullname):
    lines = []
    with open(fullname, "rt", encoding="ansi") as f:
        for line in f:
            lines.append(line.strip())
    return lines


def chart(data):
    curve, sec_derivation, eq_point = data
    x1 = [curve[i][0] for i in range(len(curve))]
    y1 = [curve[i][1] for i in range(len(curve))]
    x2 = [sec_derivation[i][0] for i in range(len(sec_derivation))]
    y2 = [sec_derivation[i][1] for i in range(len(sec_derivation))]
    # vytvoří dvě křivky dle indexů jak jsou data v listu vycházejícího z finkce "x"
    plt.plot(x1, y1, label='Titration Curve', color='blue')
    plt.plot(x2, y2, color='green', label='Second Derivative')
    plt.axhline(y=0, color='black', linewidth=0.5)
    plt.scatter(eq_point, 0, color="red", zorder=5, s=100)
    plt.title(" Titration Curve with second derivative")
    plt.xlabel("Volume")
    plt.ylabel("pH")
    # Přidá popisek do grafu s informací o bodu ekvivalence; indexově vybráno z listu vycházejícího z funkce "x"
    plt.annotate(f"Equivalence point by volume: {eq_point}",
                 xy=(eq_point, 0),
                 xytext=(0, -16),
                 arrowprops=None,
                 fontsize=12, color="red")
    plt.legend()
    plt.show()


# test2
