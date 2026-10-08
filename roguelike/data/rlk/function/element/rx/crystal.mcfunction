# 결정 (바위+불/물/번개/얼음): 결정 조각 생성 → 주우면 방어막. macro: e, n
$function rlk:element/use {e:"$(e)",m:50}
# 방어막량 = 반응 기준 × 130% × (1 + 원소 마스터리 보정 #emC%)
scoreboard players set #rdmg tmp 130
scoreboard players operation #rdmg tmp *= #rBase tmp
scoreboard players operation #rdmg tmp /= #100 tmp
scoreboard players set #t tmp 100
scoreboard players operation #t tmp += #emC tmp
scoreboard players operation #rdmg tmp *= #t tmp
scoreboard players operation #rdmg tmp /= #100 tmp
execute if score #rdmg tmp matches ..0 run scoreboard players set #rdmg tmp 1
scoreboard players set @s rxQ 9
scoreboard players operation @s rxDmg = #rdmg tmp
$scoreboard players set @s rxEl $(n)
scoreboard players set #rx tmp 9
