# 직격(#pj 1) = 직격 + 폭발 피해를 한 번에 / 바닥(#pj 2) = 폭발 범위 안이면 폭발 피해만
scoreboard players operation #cmDmg tmp = @s cmD2
execute if score #pj tmp matches 1 run scoreboard players operation #cmDmg tmp += @s cmD
scoreboard players set #ok tmp 0
execute if score #pj tmp matches 1 run scoreboard players set #ok tmp 1
execute if score #pj tmp matches 2 positioned ~ ~0.4 ~ if entity @e[tag=rlk_body,distance=..2.3] run scoreboard players set #ok tmp 1
scoreboard players operation #cmEl tmp = @s cmEl
scoreboard players operation #cmLv tmp = @s cmLv
execute if score #ok tmp matches 1 run function rlk:cm/hit_pl
particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~0.4 ~ 0.9 0.3 0.9 0.1 40
particle minecraft:snowflake ~ ~0.5 ~ 1.2 0.3 1.2 0.06 30
particle minecraft:dust{color:[0.7,0.95,1.0],scale:1.6} ~ ~0.3 ~ 1.4 0.1 1.4 0 20
execute unless score #k84 snd matches 1 run function rlk:snd/f91
execute unless score #k85 snd matches 1 run function rlk:snd/f92
function rlk:cm/wd_kill
kill @s
