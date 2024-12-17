// The vget intrinsics allow users to obtain small LMUL values from larger LMUL ones. The vget
// intrinsics also allows users to extract non-tuple (NFIELD=1) types from tuple (NFIELD>1) types after
// segment load intrinsics. The index provided must be a constant known at compile time