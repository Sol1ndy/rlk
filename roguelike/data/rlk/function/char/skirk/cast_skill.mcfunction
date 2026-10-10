# 극악기 · 섬 (@s = 플레이어, at 몸). #skBtn: 1 = 좌클릭(일곱빛 섬광), 2 = 우클릭(빠른 이동). 빠른 이동 중에 다시 누르면 멈춘다
execute if score @s skDash matches 1.. run return run function rlk:char/skirk/dash_end
execute if score @s skBurst matches 1.. run return 0
execute if score @s skM matches 1.. run return run function rlk:char/deny {t:"일곱빛 섬광 중입니다"}
execute if score @s skillCd matches 1.. run return run function rlk:char/deny {t:"원소전투 스킬 재사용 대기 중"}
# 뱀의 계략 획득
execute if score #skBtn tmp matches 2 run scoreboard players operation @s energy += #skGain tmp
execute if score #skBtn tmp matches 2 if score @s energy > #burstCost100 tmp run scoreboard players operation @s energy = #burstCost100 tmp
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
execute if score #skBtn tmp matches 2 run function rlk:char/skirk/dash_start
execute unless score #skBtn tmp matches 2 run function rlk:char/skirk/mode_start
function rlk:items/hook/on_cast_skill
function rlk:combat/on_skill
