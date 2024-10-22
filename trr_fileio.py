import os.path

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

    if underscore_rindex == -1:
        root_head = rootname + "_"
    elif underscore_rindex == len(rootname)-1: #tj. jméno končí podtržítkem
        root_head = rootname
    else:
        root_tail = rootname[underscore_rindex + 1:]
        root_head = rootname[:underscore_rindex - 1]
        for char in root_tail:
            if not char in ZERO_TO_NINE: is_zero_to_nine = False
        if is_zero_to_nine:
            root_tail_number = int(root_tail)
        else:
            root_head = rootname + "_"

    new_root_tail = str(root_tail_number)
    valid_filename = os.path.join(folder, root_head + new_root_tail + extension)
    while os.path.exists(valid_filename):
        root_tail_number += 1
        new_root_tail = str(root_tail_number)
        valid_filename = os.path.join(folder, root_head + new_root_tail + extension)

    return valid_filename

def read_file(fullname):
    lines = []
    with open(fullname, "rt", encoding="ansi") as f:
        for line in f:
            lines.append(line.strip())
    return lines
