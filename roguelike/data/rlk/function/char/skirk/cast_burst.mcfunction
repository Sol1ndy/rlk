# 원소폭발 (@s = 플레이어, at 몸). 일곱빛 섬광 중 = 진, 평소 = 멸(뱀의 계략 50pt 이상을 모두 소모)
execute if score @s skBurst matches 1.. run return 0
execute if score @s burstCd matches 1.. run return run function rlk:char/deny {t:"원소폭발 재사용 대기 중"}
execute if score @s skM matches 1.. run return run function rlk:char/skirk/ruin
execute if score @s energy < #skBurstMin tmp run return run function rlk:char/deny {t:"뱀의 계략 부족 (50pt 필요)"}
execute if score @s skDash matches 1.. run function rlk:char/skirk/dash_end
# 50pt 를 넘긴 만큼(최대 #skPtMax)
scoreboard players operation @s skPts = @s energy
scoreboard players operation @s skPts -= #skBurstMin tmp
scoreboard players operation @s skPts /= #100 tmp
execute if score @s skPts matches ..-1 run scoreboard players set @s skPts 0
execute if score @s skPts > #skPtMax tmp run scoreboard players operation @s skPts = #skPtMax tmp
scoreboard players set @s energy 0
scoreboard players operation @s burstCd = #burstCdT tmp
scoreboard players set @s skBurst 1
# 벨 자리와 방향을 고정
kill @e[tag=rlk_skb]
execute rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_skb"]}
execute rotated ~ 0 run tp @e[tag=rlk_skb] ~ ~ ~ ~ ~
execute if entity @e[tag=rlk_pm_basis,limit=1] rotated as @e[tag=rlk_pm_basis,limit=1] rotated ~ 0 run tp @e[tag=rlk_skb] ~ ~ ~ ~ 0
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
function rlk:items/hook/on_cast_burst
function rlk:combat/on_skill
