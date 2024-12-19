import os
from pathlib import Path
from XLiteral import *
from VLiteral import *
from VVLiteral import *
from VXLiteral import *
from VSLiteral import *
from VVMLiteral import *
from VXMLiteral import *
from MiscMaskLiteral import *
from HeaderLiteral import *
from MiscellaneousLiteral import *
from SegLSLiteral import *
import sys

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__)))] + sys.path

import OpDefParser

# python3 GenerateOperatorComputeHeaders.py ${SOURCE_CODE_ROOT_DIR}
assert(len(sys.argv) == 2)

source_dir = sys.argv[1]

autogen_dir = source_dir + "/include/autogen"
include_dir = source_dir + "/include"
print("Create " + autogen_dir)
Path(autogen_dir).mkdir(parents=True, exist_ok=True)

# This list will collect files created include/AutoGenComputeOp.h
# The header will include all files created under include/autogen/
created_files = []

# CUSTOM_OP_TYPE(OP_TYPE, OP_ID, SEW, TYPE_CLASS, OP_ATTR, OUTPUT_TYPE,
# NUM_OF_INPUTS, INPUT_TYPE(S)...)
def parseCustomOperatorDefinitions(filename) :
  opdef_infos = OpDefParser.parse(filename)
  for opdef_info in opdef_infos:
    op_id = opdef_info.op_id
    op_type = opdef_info.op_type
    op_attr = opdef_info.op_attr
    output_type = opdef_info.output_type
    input_num = opdef_info.input_num
    input_nfield = opdef_info.input_nfield
    output_nfield = opdef_info.output_nfield
    input_types = opdef_info.input_types
    if op_id[-2:] == "vx" or op_id[-2:] == "wx" or op_id[-2:] == "vf" or op_id[-2:] == "wf":
      if "MulAddOperation" in op_attr :
        code_gen_func = create_destructive_vx_op
      elif "MaskAgnostic" in op_attr and "TailAgnostic" not in op_attr and "TailUndisturbed" not in op_attr:
        code_gen_func = create_masked_no_maskedoff_vx_op
      else :
        code_gen_func = create_vx_op
    elif "Miscellaneous" in op_attr :
      code_gen_func = create_temp_op
    elif "SegLoadOperation" in op_attr or "SegStoreOperation" in op_attr:
      if "MaskedOperation" in op_attr:
        code_gen_func = create_seg_load_mask_op
      elif "NonmaskedOperation" in op_attr :
        code_gen_func = create_seg_load_no_mask_op
    elif op_id[-2:] == "vv" or op_id[-2:] == "wv" or op_id[-2:] == "mm":
      if "MulAddOperation" in op_attr :
        code_gen_func = create_destructive_vv_op
      elif "MaskAgnostic" in op_attr and "TailAgnostic" not in op_attr and "TailUndisturbed" not in op_attr:
        code_gen_func = create_masked_no_maskedoff_vv_op
      else :
        code_gen_func = create_vv_op
    elif op_id[-2:] == "vs" :
      code_gen_func = create_vs_op
    elif op_id[-2:] == "_v" or op_id[-3:] == "vf2" or op_id[-3:] == "vf4" \
      or op_id[-3:] == "vf8" or op_id[-5:] == "x_x_v" or op_id[-5:] == "x_x_w" \
      or op_id[-2:] == "_w" or op_id[-2:] == "_m" :
      if "NoInputOperation" in op_attr :
        code_gen_func = create_no_input_v_op
      elif op_id == "id_v" :
        code_gen_func = create_id_op
      elif op_id == "cpop_m" :
        code_gen_func = create_cpop_op
      elif op_id == "first_m" :
        code_gen_func = create_vfirst_op
      elif op_id == "msbf_m" or op_id == "msif_m" or op_id == "msof_m":
        code_gen_func = create_msbf_msif_msof_op
      elif op_id == "iota_m" :
        code_gen_func = create_iota_op
      elif op_id[:5] == "loxei" or op_id[:5] == "luxei" :
        code_gen_func = create_vv_op
      elif op_id == "lse8_v" or op_id == "lse16_v" or op_id == "lse32_v" or op_id == "lse64_v" :
        code_gen_func = create_strided_load_op
      elif op_id == "sse8_v" or op_id == "sse16_v" or op_id == "sse32_v" or op_id == "sse64_v" :
        code_gen_func = create_strided_store_op
      elif "StoreOperation" in op_attr :
        if op_type[-2:] == "_m" :
          if op_id[:5] == "soxei" or op_id[:5] == "suxei" :
            code_gen_func = create_masked_no_maskedoff_vv_op
          else :
            code_gen_func = create_masked_no_maskedoff_v_op
        else:
          if op_id[:5] == "soxei" or op_id[:5] == "suxei" :
            code_gen_func = create_vv_op
          else :
            code_gen_func = create_v_op
      else :
        code_gen_func = create_v_op
    elif op_id[-2:] == "_x" or op_id[-3:] == "v_f":
      if op_type[-2:] == "_m" :
        print("code emit for mask operator of _x is not implemented...XD")
      else :
        code_gen_func = create_x_op
    elif op_id[-3:] == "vvm" :
      code_gen_func = create_vvm_op
    elif op_id[-3:] == "vxm" or op_id[-3:] == "vfm" :
      code_gen_func = create_vxm_op
    else :
      raise Exception("unrecognized id %s of type %s" % (op_id, op_type))

    code = code_gen_func(opdef_info.op_type,
                         opdef_info.op_id, 
                         opdef_info.op_attr,
                         opdef_info.output_type,
                         opdef_info.input_num,
                         opdef_info.input_nfield,
                         opdef_info.output_nfield,
                         opdef_info.input_types)

    if len(code) == 0 :
      continue

    write_filename = "compute" + op_type + "Op.h"
    print("Create " + autogen_dir + "/" + write_filename + "...")
    file = open(autogen_dir + "/" + write_filename, "w")

    file.write('''// This is a header file auto-generated by scripts/GenerateOperatorCompute.py
// Parameters:
''')
    file.write("// CUSTOM_OP_TYPE: " + str(opdef_info) + "\n")
    file.write(header_literal)

    file.write(code)
    created_files.append(write_filename)

parseCustomOperatorDefinitions(include_dir + "/CustomOperator.def")

# Create include/AutoGenComputeOp.h
# The header will include all files created under include/autogen/
file = open(include_dir + "/" + "AutoGenComputeOp.h", "w")
file.write(
  "// This is a header file auto-generated by scripts/GenerateOperatorCompute.py\n\n")
for filename in created_files:
  file.write("#include \"autogen/" + filename + "\"\n")
