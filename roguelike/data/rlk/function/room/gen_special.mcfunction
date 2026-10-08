# 중간 구역(1 ~ n-2번째) 중 하나를 #special 종류로
execute store result score #n tmp run data get storage rlk:room cur.n
scoreboard players remove #n tmp 2
execute if score #n tmp matches ..0 run return 0
execute store result score #r tmp run random value 0..999
scoreboard players operation #r tmp %= #n tmp
scoreboard players add #r tmp 1
execute store result storage rlk:room a.si int 1 run scoreboard players get #r tmp
execute store result storage rlk:room a.sk int 1 run scoreboard players get #special tmp
function rlk:room/gen_special2 with storage rlk:room a
