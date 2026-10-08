# 쓰러져 있는 중 (@s = 플레이어): 체력 바 = 목표 체력 × 지난 시간 비율, 끝나면 되살아남
scoreboard players remove @s rnDie 1
scoreboard players operation #t1 tmp = @s maxHealth
scoreboard players operation #t1 tmp *= #rnRevPct tmp
scoreboard players operation #t1 tmp /= #100 tmp
scoreboard players operation #t2 tmp = #rnDieT tmp
scoreboard players operation #t2 tmp -= @s rnDie
scoreboard players operation #t1 tmp *= #t2 tmp
scoreboard players operation #t1 tmp /= #rnDieT tmp
execute if score #t1 tmp matches ..0 run scoreboard players set #t1 tmp 1
scoreboard players operation @s curHealth = #t1 tmp
function rlk:view/stop_h
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.0} ~ ~0.3 ~ 0.5 0.1 0.5 0 2
# 심장 박동 두 번 → 되살아남
execute if score @s rnDie matches 36 at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.warden.heartbeat master @a ~ ~ ~ 1.0 0.9
execute if score @s rnDie matches 14 at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.warden.heartbeat master @a ~ ~ ~ 1.0 1.1
execute if score @s rnDie matches ..0 run function rlk:char/ronova/die_end
