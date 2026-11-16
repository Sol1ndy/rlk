# 죽는 큰 슬라임(@s)의 레벨을 리그 뿌리에 남김(분열한 작은 슬라임이 같은 레벨)
scoreboard players operation #c2kid tmp = @s cmId
scoreboard players operation #c2klv tmp = @s mlv
execute as @e[tag=rlk_sl_body,distance=..6] if score @s cmId = #c2kid tmp run scoreboard players operation @s mlv = #c2klv tmp
