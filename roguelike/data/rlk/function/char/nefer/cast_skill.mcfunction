# 대국 · 천일 밤의 춤 (@s = 플레이어, at 몸). 충전 2회. 좌·우클릭 모두 같음
execute if score @s nfFcd matches 1.. run return 0
execute unless score @s nfC matches 1.. run return run function rlk:char/deny {t:"대국 · 천일 밤의 춤 충전 중"}
scoreboard players remove @s nfC 1
scoreboard players set @s nfFcd 6
execute if score @s nfC matches 1 run scoreboard players set @s nfCT 0
scoreboard players operation @s skillCd = #nfCd tmp
function rlk:char/cd_reduce
scoreboard players operation @s nfCdE = @s skillCd
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
# 돌진: 보는 방향(수평)으로 1칸씩 2번, 막히면 멈춤. 지나간 자리 주변 1.8칸의 적에게 한 번씩
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #nfDs tmp 2
execute rotated ~ 0 run function rlk:char/nefer/dash_step
function rlk:char/nefer/dash_hit
# 그림자 춤 9초(환영극 3번)
scoreboard players operation @s nfSD = #nfSDT tmp
scoreboard players set @s nfPh 0
# 달빛 승부사: 지금 있는 풀 씨앗 → 기만의 핵, 15초 동안 달 개화가 기만의 핵을 만든다
execute as @e[tag=rlk_core] at @s run function rlk:char/nefer/core_to_dec
scoreboard players operation #nfDecT tmp = #nfDecDur tmp
execute unless score #k131 snd matches 1 run function rlk:snd/f401
execute unless score #k340 snd matches 1 run function rlk:snd/f402
function rlk:items/hook/on_cast_skill
function rlk:combat/on_skill
