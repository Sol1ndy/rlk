# 이 구역(@s)의 칸 표식 지우기(이미 들어갔으므로 더 볼 필요 없음)
scoreboard players operation #zb tmp = @s zid
execute as @e[tag=rlk_zcell] if score @s zid = #zb tmp run kill @s
