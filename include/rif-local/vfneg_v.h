// vfneg.v vd,vs = vfsgnjn.vv vd,vs,vs
VI_VFP_V_LOOP
({
  vd = fsgnj16(vs2.v, vs2.v, true, false);
},
{
  vd = fsgnj32(vs2.v, vs2.v, true, false);
},
{
  vd = fsgnj64(vs2.v, vs2.v, true, false);
})
