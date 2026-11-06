scoreboard players set @s apT 0
function rlk:boss/apep/om/basic/play/basic_melee
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:boss/apep/org/basic/m_hz
