# absorb1 #azPT 47
function rlk:mboss/azhdaha/look/legs
function rlk:mboss/azhdaha/arena/look_leg
function rlk:mboss/push/ring {r:80,to:85,kb:4}
function rlk:mboss/azhdaha/svc/banner_ab
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/snd/absorb_burst/1
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/snd/absorb_burst/2
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/p/recolour/1 {r:280,t:20}
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/p/recolour/2 {r:280,t:20}
execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/p/dust_ring/1 {r:80}
execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/p/dust_ring/2 {r:80}
function rlk:mboss/azhdaha/fx/p/shock_dome {r:80}
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azLeg mb matches 1 run function rlk:mboss/azhdaha/fx/p/impact/1
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azLeg mb matches 2 run function rlk:mboss/azhdaha/fx/p/impact/2
