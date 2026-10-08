# 핏값 표식 만들기 (@s = 핏값이 새겨진 몹, at @s): 몸통 가운데(키의 절반) · 화면 쪽으로 (몸 반폭 + 0.3칸) 앞에. 처음엔 크기 0 → 다음 틱에 커짐(char/arlecchino/mk_grow)
tag @s add rlk_armd
tag @s add rlk_armo
function rlk:element/frz_measure
# 탑승 기준점(키 + 0.08칸)에서 몸통 가운데까지: y = -(키/2 + 0.08), z = 반폭 + 0.3
scoreboard players operation #mkY tmp = #fzH tmp
scoreboard players operation #mkY tmp /= #st2 tmp
scoreboard players add #mkY tmp 80
scoreboard players operation #mkY tmp *= #neg1 tmp
scoreboard players operation #mkZ tmp = #fzW tmp
scoreboard players add #mkZ tmp 300
execute store result storage rlk:st arm.y float 0.001 run scoreboard players get #mkY tmp
execute store result storage rlk:st arm.z float 0.001 run scoreboard players get #mkZ tmp
function rlk:char/arlecchino/mk_spawn2 with storage rlk:st arm
scoreboard players operation @e[tag=rlk_armk_n2] armY = #mkY tmp
scoreboard players operation @e[tag=rlk_armk_n2] armZ = #mkZ tmp
execute as @e[tag=rlk_armk_n2] run ride @s mount @e[tag=rlk_armo,limit=1]
tag @e[tag=rlk_armk_n2] remove rlk_armk_n2
tag @s remove rlk_armo
