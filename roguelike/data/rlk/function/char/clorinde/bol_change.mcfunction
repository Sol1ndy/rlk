# 고유 특성: 생명의 계약 값이 변할 때마다 치명타 확률 +#clPCrit% (#clPDur 틱, 최대 2스택)
execute if score @s clP matches ..1 run scoreboard players add @s clP 1
scoreboard players operation @s clPT = #clPDur tmp
