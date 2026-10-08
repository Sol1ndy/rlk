# 개화 (물+풀): 풀 씨앗 생성(6초 뒤 폭발 200%, 불→발화 300%, 번개→만개 300%). macro: e(소모할 원소), use(%)
$function rlk:element/use {e:"$(e)",m:$(use)}
function rlk:element/calc {m:300}
scoreboard players operation @s rxDmg3 = #rdmg tmp
function rlk:element/calc {m:200}
scoreboard players set @s rxQ 11
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 7
scoreboard players set #rx tmp 11
# 달 개화(달의 징조)
function rlk:element/lunar/sign
execute if score #lnBl tmp matches 1 run function rlk:element/lunar/bloom_on
