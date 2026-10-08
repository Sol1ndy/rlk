# 로노바 투사체 (위치·방향 = 실행 위치·방향, @s = 플레이어). 입력: #pKind(7 붉은 시선 구체 / 8 잔향) #pEl(원소) #pBig(1 = 큰 구체) #pIcd #pSub(틱당 0.5칸 횟수) #pLife(틱) + #dmg #crit
# 화살 틀(char/bow/arrow_*)이 날려 보내고, 맞으면 char/ronova/proj_hit
execute if score #pKind tmp matches 7 unless score #pBig tmp matches 1 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:redstone_block"},transformation:{translation:[-0.080f,-0.080f,-0.080f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.160f,0.160f,0.160f]}}
execute if score #pKind tmp matches 7 if score #pBig tmp matches 1 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:redstone_block"},transformation:{translation:[-0.135f,-0.135f,-0.135f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.270f,0.270f,0.270f]}}
execute if score #pKind tmp matches 8 if score #pEl tmp matches 1 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:shroomlight"},transformation:{translation:[-0.120f,-0.120f,-0.120f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.240f,0.240f,0.240f]}}
execute if score #pKind tmp matches 8 if score #pEl tmp matches 2 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:light_blue_concrete"},transformation:{translation:[-0.120f,-0.120f,-0.120f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.240f,0.240f,0.240f]}}
execute if score #pKind tmp matches 8 if score #pEl tmp matches 3 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:amethyst_block"},transformation:{translation:[-0.120f,-0.120f,-0.120f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.240f,0.240f,0.240f]}}
execute if score #pKind tmp matches 8 if score #pEl tmp matches 4 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:packed_ice"},transformation:{translation:[-0.120f,-0.120f,-0.120f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.240f,0.240f,0.240f]}}
execute if score #pKind tmp matches 8 if score #pEl tmp matches 5 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:gold_block"},transformation:{translation:[-0.120f,-0.120f,-0.120f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.240f,0.240f,0.240f]}}
execute if score #pKind tmp matches 8 if score #pEl tmp matches 6 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:oxidized_copper"},transformation:{translation:[-0.120f,-0.120f,-0.120f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.240f,0.240f,0.240f]}}
execute if score #pKind tmp matches 8 if score #pEl tmp matches 7 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:lime_concrete"},transformation:{translation:[-0.120f,-0.120f,-0.120f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.240f,0.240f,0.240f]}}
execute if score #pKind tmp matches 8 if score #pEl tmp matches 8 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_arrow","rlk_arrnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:redstone_block"},transformation:{translation:[-0.120f,-0.120f,-0.120f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.240f,0.240f,0.240f]}}
tp @e[tag=rlk_arrnew] ~ ~ ~ ~ ~
scoreboard players operation @e[tag=rlk_arrnew] jdmg = #dmg tmp
scoreboard players operation @e[tag=rlk_arrnew] jcrit = #crit tmp
scoreboard players operation @e[tag=rlk_arrnew] aKind = #pKind tmp
scoreboard players operation @e[tag=rlk_arrnew] aEl = #pEl tmp
scoreboard players operation @e[tag=rlk_arrnew] aSub = #pSub tmp
scoreboard players operation @e[tag=rlk_arrnew] aLife = #pLife tmp
scoreboard players operation @e[tag=rlk_arrnew] aIcd = #pIcd tmp
scoreboard players set @e[tag=rlk_arrnew] life 0
execute as @e[tag=rlk_arrnew] at @s run function rlk:char/bow/assist
tag @e[tag=rlk_arrnew] remove rlk_arrnew
