# 포자로 터진 버섯은 새 주머니를 남기지 않음(뿌리 부품에 표시)
scoreboard players operation #c3k tmp = @s cmId
execute as @e[tag=rlk_fu_stem,distance=..4] if score @s cmId = #c3k tmp run tag @s add rlk_c3nopod
