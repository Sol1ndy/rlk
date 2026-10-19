# 21 absorb 1 (WORKING STUB, S1-MOD): cine + untargetable; burst 47: the legs look, the arena, the push ring;
# 94: phase 2 (floor F2, music 2, the brand banner), roar_rear + the leg special; roar 114: cine ends.
function rlk:mboss/azhdaha/svc/cine_on
function rlk:mboss/azhdaha/px/inv
function rlk:mboss/azhdaha/rig_stub/glow/gold_on
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/kstub/p/vortex/1
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/kstub/p/vortex/2
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/kstub/snd/absorb_vortex/1
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/kstub/snd/absorb_vortex/2
