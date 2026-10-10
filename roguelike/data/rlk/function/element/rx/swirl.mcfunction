# 확산 (바람+불/물/번개/얼음/공허): 주변에 그 원소 피해 60% + 원소 전파. macro: e, n(원소 번호)
$function rlk:element/use {e:"$(e)",m:50}
function rlk:element/calc {m:60}
scoreboard players set @s rxQ 8
scoreboard players operation @s rxDmg = #rdmg tmp
$scoreboard players set @s rxEl $(n)
scoreboard players set #rx tmp 8
