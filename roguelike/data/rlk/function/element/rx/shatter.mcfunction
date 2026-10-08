# 쇄빙 (빙결+바위): 빙결 해제 + 물리 피해 300%
function rlk:element/frz_end
function rlk:element/calc {m:300}
scoreboard players set @s rxQ 7
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 0
scoreboard players set #rx tmp 7
