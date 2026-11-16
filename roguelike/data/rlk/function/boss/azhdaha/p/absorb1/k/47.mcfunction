# absorb1 #azPT 47
function rlk:boss/azhdaha/look/legs
function rlk:boss/azhdaha/arena/look_leg
function rlk:mboss/push/ring {r:80,to:85,kb:4}
function rlk:boss/azhdaha/svc/banner_ab
execute if score #azLeg mb matches 1 run function rlk:boss/azhdaha/fx/snd/absorb_burst/1
execute if score #azLeg mb matches 2 run function rlk:boss/azhdaha/fx/snd/absorb_burst/2
function rlk:boss/azhdaha/fx/p/shock_dome {r:80}
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azLeg mb matches 1 run function rlk:boss/azhdaha/fx/p/impact/1
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azLeg mb matches 2 run function rlk:boss/azhdaha/fx/p/impact/2
