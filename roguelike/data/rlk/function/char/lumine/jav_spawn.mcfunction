# 투창 하나 생성 (@s = 플레이어, 위치 = 생성 지점). 피해 = 공격력의 130% × (1 + 별빛 보너스), 치명타는 투창마다 판정
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_jav","rlk_javnew"],teleport_duration:1,brightness:{sky:15,block:15},block_state:{id:"minecraft:blue_ice"},transformation:{translation:[-0.08f,-0.08f,-1.1f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.16f,0.16f,2.2f]}}
function rlk:char/dmg_calc {coef:130}
scoreboard players operation #jb tmp = @s javBonus
scoreboard players add #jb tmp 1000
scoreboard players operation #dmg tmp *= #jb tmp
scoreboard players operation #dmg tmp /= #1000 tmp
function rlk:items/hook/burst_dmg
scoreboard players operation @e[tag=rlk_javnew] jdmg = #dmg tmp
scoreboard players operation @e[tag=rlk_javnew] jcrit = #crit tmp
scoreboard players set @e[tag=rlk_javnew] life 0
execute as @e[tag=rlk_javnew] at @s facing entity @e[tag=rlk_aimpt,limit=1] feet run tp @s ~ ~ ~ ~ ~
tag @e[tag=rlk_javnew] remove rlk_javnew
playsound minecraft:item.trident.throw master @a ~ ~ ~ 0.9 1.5
particle minecraft:snowflake ~ ~ ~ 0.15 0.15 0.15 0.03 6
