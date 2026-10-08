# 과부하 (불+번개): 주변 폭발(불 피해 275%). macro: e(소모할 부착 원소)
$function rlk:element/use {e:"$(e)",m:100}
function rlk:element/calc {m:275}
scoreboard players set @s rxQ 3
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 1
scoreboard players set #rx tmp 3
