# 법구가 아바타 오른쪽 앞 위에 떠 있다 (@s = 플레이어): 1인칭이거나 아바타가 없으면 치운다. 천천히 돌고 위아래로 떠다닌다
execute if entity @s[tag=rlk_body] run return run kill @e[tag=rlk_nfcat]
execute unless entity @e[tag=rlk_av,limit=1] run return run kill @e[tag=rlk_nfcat]
execute unless entity @e[tag=rlk_nfcat_c,limit=1] run return run function rlk:char/nefer/cat_spawn
execute store result score #t1 tmp run time query gametime
scoreboard players operation #t2 tmp = #t1 tmp
scoreboard players operation #t2 tmp %= #c40 tmp
scoreboard players remove #t2 tmp 20
execute if score #t2 tmp matches ..-1 run scoreboard players operation #t2 tmp *= #neg1 tmp
scoreboard players add #t2 tmp 265
execute store result storage rlk:nf cat.dy double 0.005 run scoreboard players get #t2 tmp
scoreboard players operation #t1 tmp *= #c2 tmp
scoreboard players operation #t1 tmp %= #c360 tmp
execute store result storage rlk:nf cat.yaw int 1 run scoreboard players get #t1 tmp
function rlk:char/nefer/cat_tp with storage rlk:nf cat
