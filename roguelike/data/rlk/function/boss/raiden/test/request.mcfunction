# #rdReq = requested id. Starts a test if needed, aborts the current attack and switches
# phase so the request can run next. Returns 1 when accepted.
scoreboard players set #rdOk rd 0
execute if score #rdReq rd matches 1..7 run scoreboard players set #rdOk rd 1
execute if score #rdReq rd matches 11..20 run scoreboard players set #rdOk rd 1
execute if score #rdOk rd matches 0 run tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"패턴 번호는 1~7(일반) 또는 11~20(갑주)입니다.",color:"red",bold:false}]
execute if score #rdOk rd matches 0 run return 0
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run function rlk:boss/raiden/test/start
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run return 0
execute as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/test/apply
return 1
