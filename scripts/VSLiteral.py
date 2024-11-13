vs_literal_start0 = "void compute"
vs_literal_start1 = "Op(RIF::OperatorBase *op) {\n"
vs_literal_nonmask_body = '''
  assert(b->length == 1);

  auto length = a->length;

  auto dataA = getRawPointer(a);
  auto dataOut = getRawPointer(b);

  auto sew = op->typeInfo->sew.to_int();

  for (int i = 0; i < length; ++i) {
'''

vs_ta_literal_nonmask_body = '''
  assert(a->length == b->length);

  auto length = a->length;

  auto dataA = getRawPointer(a);
  auto dataOut = getRawPointer(b);

  auto sew = op->typeInfo->sew.to_int();

  for (int i = 0; i < length; ++i) {
'''

vs_ta_literal_nonmask_reduction_body = '''
  assert(a->length == b->length);

  auto length = a->length;

  auto dataA = getRawPointer(a);  // vs1
  auto dataB = getRawPointer(b);  // vs2
  auto dataOut = getRawPointer(c); // vd

  auto sew = op->typeInfo->sew.to_int();

  for (int i = 0; i < length; ++i) {
'''

vs_tu_literal_nonmask_body = '''
  assert(a->length == b->length);

  auto length = a->length;

  auto dataPassthru = getRawPointer(a);
  auto dataA = getRawPointer(b);
  auto dataOut = getRawPointer(c);

  auto sew = op->typeInfo->sew.to_int();

  for (int i = 0; i < length; ++i) {
'''

def include_literal(filename):
    return "#include\"" + filename + "\""

vs_literal_nonmask_end = '''
  }
}
'''

vs_ta_literal_nonmask_end = '''
  }
  for (int i = 1; i < length; ++i) {
    memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
  }
}
'''

vs_tu_literal_nonmask_end = '''
  }
  for (int i = 1; i < length; ++i) {
    dataOut[i] = dataPassthru[i];
  }
}
'''

vs_literal_mask_body = '''
  // scripts/VSLiteral.py vs_literal_mask_body \n
  assert(a->length == b->length && c->length == 1);

  auto length = a->length;

  auto dataM = getRawPointer(a);
  auto dataA = getRawPointer(b);
  auto dataOut = getRawPointer(c);

  auto sew = op->typeInfo->sew.to_int();

  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''

vs_literal_mask_frm_body = '''
  // scripts/VSLiteral.py vs_literal_mask_frm_body \n
  
  assert(a->length == b->length && a->length == c->length && 
         a->length == f->length && a->length == e->length && d->length == 1);

  auto length = a->length;

  auto dataM = getRawPointer(a);  // mask
  auto dataA = getRawPointer(b);   // operand 1
  auto dataB = getRawPointer(c);   // operand 2
  // d means frm
  auto dataOut = getRawPointer(e);   // result
  auto dataMO = getRawPointer(f);   // default result

  auto sew = op->typeInfo->sew.to_int();
  auto dataASew = c->typeInfo->sew.to_int(); // for index load / store only
  P.VU.vsew = sew;

  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''

vs_tam_literal_mask_body = '''
  assert(a->length == b->length && a->length == c->length);

  auto length = a->length;

  auto dataM = getRawPointer(a);
  auto dataA = getRawPointer(b);
  auto dataOut = getRawPointer(c);

  auto sew = op->typeInfo->sew.to_int();

  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''

vs_tum_literal_mask_body = '''
  // generated by scripts/VSLiteral.py vs_tum_literal_mask_body
  assert(a->length == b->length && a->length == c->length && a->length == d->length);

  auto length = a->length;

  auto dataM = getRawPointer(a);
  auto dataPassthru = getRawPointer(b);
  auto dataA = getRawPointer(c);
  auto dataOut = getRawPointer(d);

  auto sew = op->typeInfo->sew.to_int();

  for (int i = 0; i < length; ++i) {
    if (dataM[i]) {
'''

def include_literal(filename):
    return "#include\"" + filename + "\""

vs_literal_mask_end = '''
    }
  }
}
'''

vs_tam_literal_mask_end = '''
    }
  }
  for (int i = 1; i < length; ++i) {
    memset(&dataOut[i], 0xff, sizeof(dataOut[i]));
  }
}
'''

vs_tum_literal_mask_end = '''
    }
  }
  for (int i = 1; i < length; ++i) {
    dataOut[i] = dataPassthru[i];
  }
}
'''

def create_vs_op(op_type, op_id, op_attr, output_type, input_num, input_types) :
  ret = ""
  ret += vs_literal_start0 + op_type + vs_literal_start1
  for i in range(input_num) :
    var = chr(ord('a') + i)
    ret += "  auto " + var + " = static_cast<RIF::" + input_types[i] + "Val *>(op->inputs[" + str(i) + "]); // scripts/VSLiteral.py create_vs_op \n"
  var = chr(ord('a') + input_num)
  ret += "  auto " + var + " = static_cast<RIF::" + output_type + "Val *>(op->outputs[0]); // scripts/VSLiteral.py create_vs_op \n"
  if "MaskedOperation" in op_attr :
    var = chr(ord('a') + input_num + 1)
    ret += "  auto " + var + " = static_cast<RIF::" + output_type + "Val *>(op->inputs[" + str(input_num) + "]); // masked op default vd scripts/VSLiteral.py create_vs_op \n"
    if "TailAgnostic" in op_attr : # tam
      ret += vs_tam_literal_mask_body + include_literal("v" + op_id + ".h") + vs_tam_literal_mask_end
    elif "RoundingMode" in op_attr :
      ret += vs_literal_mask_frm_body + "\t" +include_literal("v" + op_id + ".h") + vs_literal_mask_end
    elif "TailUndisturbed" in op_attr : # tum
      ret += vs_tum_literal_mask_body + include_literal("v" + op_id + ".h") + vs_tum_literal_mask_end
    else :
      ret += vs_literal_mask_body + include_literal("v" + op_id + ".h") + vs_literal_mask_end
  else :
    if "TailUndisturbed" in op_attr :
      ret += vs_tu_literal_nonmask_body + include_literal("v" + op_id + ".h") + vs_tu_literal_nonmask_end
    elif "TailAgnostic" in op_attr :
      ret += vs_ta_literal_nonmask_body + include_literal("v" + op_id + ".h") + vs_ta_literal_nonmask_end
    elif "ReductionOperation" in op_attr :
      ret += vs_ta_literal_nonmask_reduction_body + include_literal("v" + op_id + ".h") + vs_ta_literal_nonmask_end
    else :
      ret += vs_literal_nonmask_body + include_literal("v" + op_id + ".h") + vs_literal_nonmask_end
  return ret
