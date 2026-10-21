# At the socket: facing the Heart, the melee loop (the first lean 20 t later).
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
function rlk:boss/apep/om/face
scoreboard players set @s apS 4
scoreboard players set @s apT 20
