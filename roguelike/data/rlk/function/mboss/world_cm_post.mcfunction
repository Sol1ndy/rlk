# From mboss/world in a chapter fight (#mbMode 1), after the module tick (and the rig tick inside it): the proxies
# follow the shown pose, the body push (#mbPushOn set by the module this tick), the music clock.
execute if score #mbPx mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/px/tick
execute if score #mbPushOn mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s rotated as @s run function rlk:mboss/push/capsule
execute if score #mbMusPh mb matches 1.. run function rlk:mboss/music/tick
