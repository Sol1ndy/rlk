# 일반 닷지로 몸을 낮춘 마네킹 아바타를 다시 세운다(player/def/box_end; 아바타가 그사이 새로 만들어졌어도 해가 없다)
scoreboard players set #dgCr cb 0
data merge entity @e[type=minecraft:mannequin,tag=rlk_av,limit=1] {pose:"standing"}
