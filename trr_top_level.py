import trr
import trr_fileio

rpt_files = trr_fileio.read_directory(trr_fileio.report_directory)

for rpt_file in rpt_files:
    trr_fileio.chart(trr.secder_eqpoint(rpt_file))