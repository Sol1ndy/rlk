# @s = 플레이어, at 몸(player/dash_go: 일반 닷지의 스텝과 더블 닷지의 두 번째 동작 모두 — 동작마다 새 도장). 닷지 시각 도장: dgAt = 지금, 퍼펙트 창의 끝 #dgEnd = 지금 + #dgPW - 1, 그 다음 틱에
# 표식을 지움(#dgKill; rlk:tick → player/def/box_end, #dgBox cb 1 = 지울 표식이 있음). 표식 rlk_dgo = 시작한 자리의 몸 크기 상자
# (interaction 0.6 × 1.8, 클릭을 받지 않는 자리 표시, 몸이 보던 쪽을 봄: 붉은 잔상의 방향): 창이 열린 동안 커스텀 몹 · 보스 위험 지대 ·
# 투사체 · 나루카미는 몸 대신 이 자리로도 판정한다(player/def/ghost_on)
# 시각 도장이 없는 플레이어(전투 개편 전 저장)의 첫 닷지: 도장을 쓰기 전에 비운다(판정이 나중에 비우면 이 닷지가 지워진다)
execute unless score @s parHit matches -2147483648.. run function rlk:player/def/reset
execute store result score #now cb run time query gametime
scoreboard players operation #now cb -= #btAdj cb
scoreboard players operation @s dgAt = #now cb
scoreboard players operation #dgEnd cb = #now cb
scoreboard players operation #dgEnd cb += #dgPW tmp
scoreboard players remove #dgEnd cb 1
scoreboard players operation #dgKill cb = #dgEnd cb
scoreboard players add #dgKill cb 1
scoreboard players set #dgOpen cb 1
scoreboard players set #dgBox cb 1
kill @e[tag=rlk_dgo]
summon minecraft:interaction ~ ~ ~ {Tags:["rlk_dgo","rlk_pet"],width:0.6f,height:1.8f,response:false}
# summon 은 방향을 물려받지 않는다: 몸이 보던 쪽(yaw)을 준다
execute rotated as @e[tag=rlk_body,limit=1] as @e[tag=rlk_dgo,limit=1] run rotate @s ~ 0
