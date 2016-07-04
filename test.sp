.include 'test_include.sp'
.param Vin RL CL Rtail



Vinp vinp tail 'Vin*0.5'
Vinm vinm tail '-Vin*0.5'


Rrail vtail 0 Rtail
xmp	voutp vinp tail pmos 
xmm	voutm vinm tail pmos 
RLP voutp 0 RL
CLP voutp 0 CL
RLM voutm 0 RL
CLM voutm 0 CL

.print v(voutp,voutm)
.print '(v(voutp)+v(voutm))*0.5'
.print v(tail)
.ends 