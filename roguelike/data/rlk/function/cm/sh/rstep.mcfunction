function rlk:cm/sh/blk
# 막혔으면 앞을 부숴 봄(3×3, 발~머리 위)
execute if score #bF tmp matches 1 at @s rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^0.5 ^1.3 run function rlk:cm/brk_here {r:1,yl:0,yh:2}
execute if score #bF tmp matches 0 if score #bH tmp matches 1 at @s rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^0.5 ^1.3 run function rlk:cm/brk_here {r:1,yl:0,yh:2}
execute if score #bF tmp matches 1 run function rlk:cm/sh/blk
execute if score #bF tmp matches 0 if score #bH tmp matches 1 run function rlk:cm/sh/blk
# 한 칸 턱이면 올라섬
execute if score #bF tmp matches 1 if score #bH tmp matches 0 at @s rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^3.0 ^0.9 if block ~ ~ ~ #rlk:cm_pass at @s run tp @s ~ ~1 ~
execute if score #bF tmp matches 1 if score #bH tmp matches 0 at @s rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^3.0 ^0.9 if block ~ ~ ~ #rlk:cm_pass run scoreboard players set #bF tmp 0
execute if score #bF tmp matches 1 run return run function rlk:cm/sh/rend
execute if score #bH tmp matches 1 run return run function rlk:cm/sh/rend
execute at @s rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 run tp @s ^ ^ ^0.35
# Player contact does not consume movement distance or restart the rush animation.
execute unless entity @s[tag=rlk_sh_rhit] at @s if entity @e[tag=rlk_body,distance=..1.9] run function rlk:cm/sh/rcontact
scoreboard players remove #rs tmp 1
execute if score #rs tmp matches 1.. run function rlk:cm/sh/rstep
