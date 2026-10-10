# @s = 닫힌 문(검은 콘크리트), 플레이어가 다가옴 → 건너편 구역을 짓고 문을 연다
scoreboard players operation #za tmp = @s da
scoreboard players operation #zc tmp = @s db
execute as @e[tag=rlk_zone,scores={zst=0}] if score @s zid = #za tmp run function rlk:room/zone_build
execute as @e[tag=rlk_zone,scores={zst=0}] if score @s zid = #zc tmp run function rlk:room/zone_build
execute unless score #k8 snd matches 1 run function rlk:snd/f8
execute unless score #k9 snd matches 1 run function rlk:snd/f9
