*$ 
*$ Example 2 - Cascode Current Mirror
*$
*$ 
*$
.include 'examples\library\mos.sp'
.param i0 r0 gm0 gm1 rds0 rds1 VL
i0   c   0   i0
r0   c   b   r0
xmnc0 b   c x mos_s gm = 'gm0' gds = '1/rds0'
xmnb0 x   b 0 mos_s gm = 'gm1' gds = '1/rds1'
xmnbc out c y mos_s gm = 'gm0' gds = '1/rds0'
xmnb1 y   b 0 mos_s gm = 'gm1' gds = '1/rds1'

VL out 0 VL

.print vb v(b)
.print iout0 i(VL) VL='1.0*i0*(-gm0*r0*rds0 + gm0*rds0*rds1 + rds0 + rds1)/((gm0*rds0 + 1)*(gm1*rds1 + 1))'
.print output_resistance '-VL/i(VL)' i0=0
.ends