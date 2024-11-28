import trr
import trr_fileio
import user_specific_paths


working_folder = user_specific_paths.report_directory

rpt_files = trr_fileio.read_directory(working_folder)
if len(rpt_files) == 0:
    print(f"No rpt files found in {working_folder}")

for rpt_file in rpt_files:
    eq_data = trr.secder_eqpoint(rpt_file)
    if eq_data is None:
        print(f"Equivalence point not found in {rpt_file}")
        continue
    trr_fileio.chart(eq_data)

