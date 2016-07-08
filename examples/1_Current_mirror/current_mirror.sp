*$ 
*$ Example 1 - Current mirror
*$
*$ 
*$
.include 'examples\library\mos.sp'
.param i0 VL n gds
i0   b   0   i0
xmn0 b   b 0 mos_s gds = 'gds' m = 1
xmn1 out b 0 mos_s gds = 'gds' m = n
VL out 0 VL
.print vb v(b)
.print iout 'i(VL)'
.print multiplication 'i(VL)/i(i0)' VL='i0/(gds + gm)'
.print output_resistance '-VL/i(VL)' i0=0

.ends