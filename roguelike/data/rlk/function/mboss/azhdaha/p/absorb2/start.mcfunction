# 22 absorb 2 (WORKING STUB, S1-MOD): burst 42: the tail look, phase 3, #mbFloor 1; 52: roar_rear
# (no cast); roar 72: cine ends; then the B3 frame.
function rlk:mboss/azhdaha/svc/cine_on
function rlk:mboss/azhdaha/px/inv
function rlk:mboss/azhdaha/rig/glow/gold_on
execute if score #azTail mb matches 3 run function rlk:mboss/azhdaha/fx/snd/absorb_vortex/3
execute if score #azTail mb matches 4 run function rlk:mboss/azhdaha/fx/snd/absorb_vortex/4
