# 맑은물 술사 (@s, at @s): 몸과 7~10칸을 둠(7칸 안이면 물러남). 8칸 안에 다친 커스텀 몹(어느 챕터든, 나 말고)이 있으면 제자리에서 영창:
# 2초마다 그 몹들의 체력을 최대 체력의 10 %씩(최대 체력을 넘지 않음), 술사에서 각 몹까지 물줄기. 맞으면 3초 동안 끊김. 직접 공격은 없음
execute if score @s c3I matches 1.. run scoreboard players remove @s c3I 1
function rlk:cm/cw/keep
execute if score #free tmp matches 0 run return run function rlk:cm/cw/stop
execute if score @s c3I matches 1.. run return 0
scoreboard players set #c3w tmp 0
execute as @e[tag=rlk_cmb,distance=..8] unless score @s cmId = #cid tmp if score @s mhpC < @s mhpM run scoreboard players set #c3w tmp 1
execute if score #c3w tmp matches 0 run return run function rlk:cm/cw/stop
execute if score @s cmS matches 0 run function rlk:cm/cw/begin
scoreboard players set #hold tmp 1
scoreboard players remove @s c3H 1
execute if score @s c3H matches ..0 run function rlk:cm/cw/pulse
