execute store result storage rlk:room ret.x double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result storage rlk:room ret.y double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[1] 100
execute store result storage rlk:room ret.z double 0.01 run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
data modify storage rlk:room ret.dim set from entity @s Dimension
# 던전이 월드 스폰 위에 있어서, 죽으면 던전 바닥판 위에서 부활하지 않도록 부활 지점을 시작한 자리로 잡아 둔다
execute at @e[tag=rlk_body,limit=1] run spawnpoint @s ~ ~ ~
