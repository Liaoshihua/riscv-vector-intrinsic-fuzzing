// vfabs.v vd,vs = vfsgnjx.vv vd,vs,vs
VI_VFP_V_LOOP
({
  vd = fsgnj16(vs2.v, vs2.v, false, true);
},
{
  vd = fsgnj32(vs2.v, vs2.v, false, true);
},
{
  vd = fsgnj64(vs2.v, vs2.v, false, true);
})
