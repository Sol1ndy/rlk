# @s = 플레이어, at 몸(player/dash_go). 닷지 시각 도장: dgAt = 지금, 퍼펙트 창의 끝 #dgEnd = 지금 + #dgPW - 1, 그 다음 틱에
# 표식을 지움(#dgKill). 표식 rlk_dgo = 시작한 자리의 몸 크기 상자(interaction 0.6 × 1.8, 클릭을 받지 않는 자리 표시):
# 창이 열린 동안 커스텀 몹 · 보스 위험 지대 · 투사체 · 나루카미는 몸 대신 이 자리로도 판정한다(player/def/ghost_on)
execute store result score #now cb run time query gametime
scoreboard players operation @s dgAt = #now cb
scoreboard players operation #dgEnd cb = #now cb
scoreboard players operation #dgEnd cb += #dgPW tmp
scoreboard players remove #dgEnd cb 1
scoreboard players operation #dgKill cb = #dgEnd cb
scoreboard players add #dgKill cb 1
scoreboard players set #dgOpen cb 1
kill @e[tag=rlk_dgo]
summon minecraft:interaction ~ ~ ~ {Tags:["rlk_dgo","rlk_pet"],width:0.6f,height:1.8f,response:false}
