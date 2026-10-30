# @s = the body (px/tick): proxy-held target state moves to the body (cm.md 9.6 audit).
execute as @e[type=minecraft:interaction,tag=rlk_mb_px,scores={scT=1..}] run function rlk:mboss/px/db/sct
execute as @e[type=minecraft:interaction,tag=rlk_mb_px,scores={rnNoE=1..}] run function rlk:mboss/px/db/rnnoe
execute as @e[type=minecraft:interaction,tag=rlk_mb_px,scores={mirEnd=1..}] run function rlk:mboss/px/db/mirend
execute as @e[type=minecraft:interaction,tag=rlk_mb_px,scores={aurEnd=1..}] run function rlk:mboss/px/db/aurend
