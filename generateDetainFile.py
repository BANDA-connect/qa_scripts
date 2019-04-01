import dcmstack, dicom
import re
from glob import glob
src_paths = glob('/space/erebus/1/users/data/PANDA027/MR.1.3.12.2.1107.5.2.43.67026.2016082618315273841897405')
my_stack = dcmstack.DicomStack()
for src_path in src_paths:
	src_dcm = dicom.read_file(src_path)
	my_stack.add_dcm(src_dcm)

nw = my_stack.to_nifti_wrapper()
bwp = nw.meta_ext.get_values('CsaImage.BandwidthPerPixelPhaseEncode')

matrix = int(re.match('\d+', nw.meta_ext.get_values('CsaImage.AcquisitionMatrixText').split('*')[0]).group(0))
print bwp
echospacing = 1000./(bwp * matrix)
print "epi factor",matrix

print "echospacing",echospacing

print "datain c4", echospacing*matrix/1000

