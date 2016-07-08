*$ 
*$ Example 6 - Differential pair with resistive load
*$
*$ 
*$
.include 'examples\library\mos.sp'
.param Vin RL CL Rt gds

Vp inp 0 'Vin/2'
Vm inm 0 '-Vin/2'

xmnp outm inp tail mos_s gds = 'gds' 
xmnm outp inm tail mos_s gds = 'gds' 

RLP outp 0 RL
CLP outp 0 CL
RLM outm 0 RL
CLM outm 0 CL
.print gain 'v(outp,outm)/v(inp,inm)'  s = 0 
.print vout 'v(outp,outm)'
.print vtail v(tail)
.print T 'v(outp,outm)/v(inp,inm)'
.plot T RL=1k CL=1n gds = 0.1m gm = 1m 

.ends