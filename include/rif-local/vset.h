// spec:The vset intrinsics allow users to combine small LMUL values into larger LMUL ones. The vset
// intrinsics also allows users to combine non-tuple (NFIELD=1) types to tuple (NFIELD>1) types for
// segment store intrinsics. The index provided must be a constant known at compile time.