# 육참골단 중첩 +1 (@s = 플레이어): 최대 #hwStkMax, 중첩 시간을 지금부터 #hwStkDur 틱으로 새로 고침(#hwTEnd = 끝나는 시각,
# 다음 할 일 #hwNext · #hwWait 도 그보다 늦지 않게)
# 공격력 % = 중첩 × #hwStkAtk (#hwAtk, items/proc/hw_stat 이 2틱마다 더함). 사이드바 '육참골단' = 중첩 수
scoreboard players add #hwStk itv 1
execute if score #hwStk itv > #hwStkMax tmp run scoreboard players operation #hwStk itv = #hwStkMax tmp
execute store result score #hwNow itv run time query gametime
scoreboard players operation #hwTEnd itv = #hwNow itv
scoreboard players operation #hwTEnd itv += #hwStkDur tmp
scoreboard players operation #hwNext itv < #hwTEnd itv
scoreboard players operation #hwWait itv < #hwStkDur tmp
scoreboard players operation #hwAtk itv = #hwStk itv
scoreboard players operation #hwAtk itv *= #hwStkAtk tmp
scoreboard players operation 육참골단 stacks = #hwStk itv
scoreboard players display name 육참골단 stacks {text:"육참골단",color:"#F28CB1"}
execute unless score #k352 snd matches 1 run function rlk:snd/f422
execute if score #hwStk itv >= #hwStkMax tmp unless score #k353 snd matches 1 run function rlk:snd/f423
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.79f,0.63f,1.0f],scale:1.0f} ~ ~1.1 ~ 0.35 0.45 0.35 0 3
execute at @e[tag=rlk_body,limit=1] run particle minecraft:cherry_leaves ~ ~1.3 ~ 0.4 0.3 0.4 0 2
