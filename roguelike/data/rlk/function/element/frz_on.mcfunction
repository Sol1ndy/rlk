execute unless score #k44 snd matches 1 run function rlk:snd/f46
particle minecraft:snowflake ~ ~1 ~ 0.3 0.5 0.3 0.02 20
execute if entity @s[type=minecraft:player] run return run function rlk:element/frz_on_player
# 몹: AI 정지 + 얼음 표시 (원래 NoAI 였던 몹은 해제 때 되돌리지 않음)
execute if data entity @s {NoAI:1b} run tag @s add rlk_noai
data merge entity @s {NoAI:1b}
# 얼음 크기 = 몹의 히트박스에 맞춤: 폭 = 몹 폭 + 0.3, 높이 = 몹 키 + 0.2. 얼음은 몹에 탑승(머리 위 기준점)하므로 키만큼 아래로 내려 발밑부터 덮는다
function rlk:element/frz_measure
scoreboard players operation #fzS tmp = #fzW tmp
scoreboard players operation #fzS tmp += #fzW tmp
scoreboard players add #fzS tmp 300
execute store result storage rlk:st fz.w float 0.001 run scoreboard players get #fzS tmp
scoreboard players operation #fzT tmp = #fzW tmp
scoreboard players add #fzT tmp 150
scoreboard players operation #fzT tmp *= #neg1 tmp
execute store result storage rlk:st fz.tx float 0.001 run scoreboard players get #fzT tmp
scoreboard players operation #fzT tmp = #fzH tmp
scoreboard players add #fzT tmp 200
execute store result storage rlk:st fz.h float 0.001 run scoreboard players get #fzT tmp
scoreboard players operation #fzT tmp = #fzH tmp
scoreboard players add #fzT tmp 80
scoreboard players operation #fzT tmp *= #neg1 tmp
execute store result storage rlk:st fz.ty float 0.001 run scoreboard players get #fzT tmp
tag @s add rlk_frz_owner
function rlk:element/frz_ice with storage rlk:st fz
execute as @e[tag=rlk_frz_new] run ride @s mount @e[tag=rlk_frz_owner,limit=1,sort=nearest]
tag @e[tag=rlk_frz_new] remove rlk_frz_new
tag @s remove rlk_frz_owner
# 탑승 기준점은 몹마다 조금씩 달라서, 다음 틱에 실제 위치로 얼음 바닥을 발밑에 맞춘다
tag @s add rlk_frz_fix
