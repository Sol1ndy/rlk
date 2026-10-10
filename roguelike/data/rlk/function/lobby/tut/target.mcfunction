# 2단계 허수아비 (쓰러뜨릴 수 있음, 체력 = 공격력 × 5)
summon minecraft:zombie ~ ~ ~ {Tags:["rlk_lobby","rlk_tutE","rlk_tutT","rlk_dnew"],NoAI:1b,Silent:1b,PersistenceRequired:1b,IsBaby:0b,CanPickUpLoot:0b,Rotation:[180f,0f],equipment:{head:{id:"minecraft:hay_block",count:1},chest:{id:"minecraft:leather_chestplate",count:1}}}
scoreboard players operation #t lob = @a[tag=player,limit=1] atk
scoreboard players operation #t lob *= #c5 lob
execute if score #t lob matches ..49 run scoreboard players set #t lob 50
scoreboard players set @e[tag=rlk_dnew] mhp0 1
scoreboard players set @e[tag=rlk_dnew] mlv 1
scoreboard players operation @e[tag=rlk_dnew] mhpM = #t lob
scoreboard players operation @e[tag=rlk_dnew] mhpC = #t lob
execute as @e[tag=rlk_dnew] run function rlk:mob/vhp_pin
tag @e[tag=rlk_dnew] remove rlk_dnew
