# 21 absorb 1 (S2-S; plan 5 T2, 4.4): cine + untargetable; the vortex and sigils of the leg element; burst
# 47: the legs look, the arena, the push ring r 8; 94: phase 2 (floor F2, music 2), roar_rear + the
# leg special; roar 114: the line, the brand banner, the dome rings, cine ends.
function rlk:mboss/azhdaha/svc/cine_on
function rlk:mboss/azhdaha/px/inv
function rlk:mboss/azhdaha/rig/glow/gold_on
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/p/vortex/1 {t:47}
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/p/vortex/2 {t:47}
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/p/sigils/1
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/p/sigils/2
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/snd/absorb_vortex/1
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/snd/absorb_vortex/2
