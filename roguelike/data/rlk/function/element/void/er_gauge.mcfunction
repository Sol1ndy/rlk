# 잠식 게이지 (@s = 몹). 잠식이 없으면 치우고, 있으면(없으면 만들고) 길이·위치를 맞춘다
execute unless score @s rnEr matches 1.. run return run execute on passengers if entity @s[tag=rlk_hb_er] run kill @s
scoreboard players set #eg tmp 0
execute on passengers if entity @s[tag=rlk_hb_er] run scoreboard players add #eg tmp 1
execute if score #eg tmp matches ..3 run function rlk:element/void/er_gauge_new
# 길이(띠) = 잠식 × 0.016, 눈금 x = -0.8 + 잠식 × 0.016
scoreboard players operation #egw tmp = @s rnEr
scoreboard players operation #egw tmp *= #c160 tmp
execute store result storage rlk:st eg.w float 0.0001 run scoreboard players get #egw tmp
scoreboard players remove #egw tmp 8000
execute store result storage rlk:st eg.x float 0.0001 run scoreboard players get #egw tmp
scoreboard players remove #egw tmp 150
execute store result storage rlk:st eg.tx float 0.0001 run scoreboard players get #egw tmp
function rlk:element/void/er_gauge_set with storage rlk:st eg
