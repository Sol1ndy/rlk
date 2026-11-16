# 22 absorb 2 (S2-S; plan 5 T3, 4.4): cine + untargetable; the element gathers over the back; burst 42:
# the tail look, phase 3, #mbFloor 1, the shard rain, the push ring; 52: roar_rear (no cast); roar 72: the
# line, the dome rings, cine ends; then the B3 frame.
function rlk:boss/azhdaha/svc/cine_on
function rlk:boss/azhdaha/px/inv
function rlk:boss/azhdaha/rig/glow/gold_on
execute if score #azTail mb matches 3 run function rlk:boss/azhdaha/fx/p/vortex/3 {t:42}
execute if score #azTail mb matches 4 run function rlk:boss/azhdaha/fx/p/vortex/4 {t:42}
execute if score #azTail mb matches 3 run function rlk:boss/azhdaha/fx/p/sigils/3
execute if score #azTail mb matches 4 run function rlk:boss/azhdaha/fx/p/sigils/4
execute if score #azTail mb matches 3 run function rlk:boss/azhdaha/fx/snd/absorb_vortex/3
execute if score #azTail mb matches 4 run function rlk:boss/azhdaha/fx/snd/absorb_vortex/4
