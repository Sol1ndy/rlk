# 육참골단 체력 소모 (@s = 플레이어): 체력이 최대 체력의 #hwFloor % 를 넘을 때만 현재 체력의 #hwCost %(버림), 1 아래로는 내려가지 않음
# (살롱의 초대장 items/proc/salon_pay 와 같은 규칙. 빼기는 operation -= 로만)
scoreboard players operation #hwA itv = @s curHealth
scoreboard players operation #hwA itv *= #100 tmp
scoreboard players operation #hwB itv = @s maxHealth
scoreboard players operation #hwB itv *= #hwFloor tmp
execute unless score #hwA itv > #hwB itv run return 0
scoreboard players operation #hwA itv = @s curHealth
scoreboard players operation #hwA itv *= #hwCost tmp
scoreboard players operation #hwA itv /= #100 tmp
scoreboard players operation @s curHealth -= #hwA itv
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 1
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.75f,0.12f,0.25f],scale:1.0f} ~ ~1.0 ~ 0.25 0.35 0.25 0 2
