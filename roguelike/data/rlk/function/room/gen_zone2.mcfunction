execute store result score @s zid run data get storage rlk:room it.id
execute store result score @s zkind run data get storage rlk:room it.kind
scoreboard players operation #zid tmp = @s zid
# 상태: 0 미건설, 1 건설됨(아직 안 들어감), 2 진입(전투 중 포함), 3 완료
scoreboard players set @s zst 0
tag @s remove rlk_new
