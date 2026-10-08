# 감전 (물+번개): 두 원소가 함께 붙어 1초마다 번개 피해 200%, 틱마다 양쪽 0.4U 소모. macro: e(이번에 닿은 원소)
$function rlk:element/attach {e:"$(e)"}
function rlk:element/calc {m:200}
scoreboard players operation @s ecDmg = #rdmg tmp
execute unless score @s ecI matches 1.. run scoreboard players set @s ecI 19
scoreboard players set #rx tmp 5
# 달 감전(달의 징조): 감전 피해가 달 피해로
function rlk:element/lunar/sign
execute if score #lnAll tmp matches 1 run function rlk:element/lunar/ec_on
