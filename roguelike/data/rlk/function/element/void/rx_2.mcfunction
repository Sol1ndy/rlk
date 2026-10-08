# 심연 (공허+물): 반경 3.5칸의 적을 대상 쪽으로 끌어당김(최대 2.5칸) + 물 피해 80%
function rlk:element/calc {m:80}
scoreboard players set @s rxQ 18
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 2
