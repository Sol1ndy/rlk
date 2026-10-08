# 등급 굴리기 → #g tmp (0 일반, 1 레어, 2 유니크, 3 레전더리, 4 신화), #gMax tmp = 지금 챕터에서 나올 수 있는 가장 높은 등급
# 기준 = 진행 중인 런의 챕터(#chapter room). 런 밖에서는 1챕터로 침
scoreboard players set #rc tmp 1
execute if score #active room matches 1 run scoreboard players operation #rc tmp = #chapter room
execute if score #rc tmp matches ..0 run scoreboard players set #rc tmp 1
execute if score #rc tmp matches 7.. run scoreboard players set #rc tmp 6
execute store result storage rlk:pick ci int 1 run scoreboard players get #rc tmp
function rlk:items/roll_rarity2 with storage rlk:pick
execute store result score #rr tmp run random value 1..1000
scoreboard players set #g tmp 4
execute if score #rr tmp <= #t4 tmp run scoreboard players set #g tmp 3
execute if score #rr tmp <= #t3 tmp run scoreboard players set #g tmp 2
execute if score #rr tmp <= #t2 tmp run scoreboard players set #g tmp 1
execute if score #rr tmp <= #t1 tmp run scoreboard players set #g tmp 0
scoreboard players set #gMax tmp 4
execute if score #rc tmp matches 2 run scoreboard players set #gMax tmp 3
execute if score #rc tmp matches 1 run scoreboard players set #gMax tmp 2
