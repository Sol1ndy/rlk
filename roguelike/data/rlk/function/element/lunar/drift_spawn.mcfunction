# 월광 결정 (위치 = 몹): 몹 위에 떠서 6초 동안 1.5초마다 가까운 적(6칸) 하나에게 달 결정 피해(반응 기준 × #lnCR%, 바위). 최대 3개
summon minecraft:item_display ~ ~2.2 ~ {Tags:["rlk_lndrift","rlk_lnd_new"],Glowing:1b,glow_color_override:16772016,billboard:"center",brightness:{sky:15,block:15},item:{id:"minecraft:amethyst_shard",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f],translation:[0f,0f,0f]}}
scoreboard players set @e[tag=rlk_lnd_new] life 120
scoreboard players set @e[tag=rlk_lnd_new] lnI 10
scoreboard players operation @e[tag=rlk_lnd_new] rxDmg = #qDmg tmp
scoreboard players operation @e[tag=rlk_lnd_new] rxDmg *= #lnCR tmp
scoreboard players operation @e[tag=rlk_lnd_new] rxDmg /= #c130 tmp
tag @e[tag=rlk_lnd_new] remove rlk_lnd_new
execute unless score #k42 snd matches 1 run function rlk:snd/f72
scoreboard players set #lnT tmp 3
function rlk:element/lunar/count
execute store result score #cc tmp if entity @e[tag=rlk_lndrift]
execute if score #cc tmp matches 4.. run kill @e[tag=rlk_lndrift,limit=1]
