// reuse vmv.v.v vd, vs # vd[i] = vs[i]
// Spec:The vreinterpret intrinsics are provided for users to transition across the strongly-typed scheme.
// The intrinsic is limited to conversion between types operating upon the same number of registers.
// These intrinsics are not mapped to any instruction because reinterpretation of registers is a no-
// operation.
VI_V_LOOP({ vd = vs; })