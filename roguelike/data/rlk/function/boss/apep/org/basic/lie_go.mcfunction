# A ranged basic on its ring: it lies down (basic_lie 10 t: bell -> bag), facing the Heart.
scoreboard players set @s apS 5
scoreboard players set @s apT 0
tag @s add rlk_mb_ap_lie
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
function rlk:boss/apep/om/face
function rlk:boss/apep/om/basic/play/basic_lie
