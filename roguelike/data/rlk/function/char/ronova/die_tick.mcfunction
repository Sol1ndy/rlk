# 쓰러져 있는 중 (@s = 플레이어): 체력 바 = 목표 체력 × 지난 시간 비율, 끝나면 되살아남
scoreboard players remove @s rnDie 1
# 몹이 쓰러진 몸을 노리지 않게(몸과 같은 팀 = 어그로 풀림)
team join rlk_stun @e[tag=rlk_mob,team=!rlk_stun]
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
execute if score @s rnDie matches 36 at @e[tag=rlk_body,limit=1] unless score #k264 snd matches 1 run function rlk:snd/f296
execute if score @s rnDie matches 14 at @e[tag=rlk_body,limit=1] unless score #k265 snd matches 1 run function rlk:snd/f297
execute if score @s rnDie matches ..0 run function rlk:char/ronova/die_end
