# 소각 (공허+불): 대상의 잠식을 모두 태워 불 피해로. 피해 = 반응 기준 × 잠식 1%당 25% (최소 100%). 잠식은 0이 된다
scoreboard players operation #t tmp = @s rnEr
scoreboard players operation #t tmp *= #c25 tmp
execute if score #t tmp matches ..99 run scoreboard players set #t tmp 100
execute store result storage rlk:rn m int 1 run scoreboard players get #t tmp
function rlk:element/calc with storage rlk:rn
scoreboard players set @s rnEr 0
scoreboard players set @s rxQ 17
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 1
