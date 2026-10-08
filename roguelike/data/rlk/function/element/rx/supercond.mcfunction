# 초전도 (얼음+번개): 주변 얼음 피해 150% + 12초간 물리 피해 +40%. macro: e
$function rlk:element/use {e:"$(e)",m:100}
function rlk:element/calc {m:150}
scoreboard players set @s rxQ 4
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 4
scoreboard players set #rx tmp 4
