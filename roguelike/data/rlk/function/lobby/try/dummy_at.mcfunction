# 죽지 않는 더미 하나 (위치 = 실행 위치). 체력 1억, 받은 피해는 매 틱 다시 채움(lobby/dummy)
summon minecraft:zombie ~ ~ ~ {Tags:["rlk_lobby","rlk_dummy","rlk_dnew"],NoAI:1b,Silent:1b,PersistenceRequired:1b,IsBaby:0b,CanPickUpLoot:0b,Rotation:[180f,0f],equipment:{head:{id:"minecraft:carved_pumpkin",count:1},chest:{id:"minecraft:leather_chestplate",count:1},legs:{id:"minecraft:leather_leggings",count:1}}}
scoreboard players set @e[tag=rlk_dnew] mhp0 1
scoreboard players set @e[tag=rlk_dnew] mlv 1
scoreboard players set @e[tag=rlk_dnew] mhpM 100000000
scoreboard players set @e[tag=rlk_dnew] mhpC 100000000
execute as @e[tag=rlk_dnew] run function rlk:mob/vhp_pin
tag @e[tag=rlk_dnew] remove rlk_dnew
