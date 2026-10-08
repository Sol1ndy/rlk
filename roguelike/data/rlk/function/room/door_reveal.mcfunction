# @s = 닫힌 문(검은 콘크리트), 플레이어가 다가옴 → 건너편 구역을 짓고 문을 연다
scoreboard players operation #za tmp = @s da
scoreboard players operation #zc tmp = @s db
execute as @e[tag=rlk_zone,scores={zst=0}] if score @s zid = #za tmp run function rlk:room/zone_build
execute as @e[tag=rlk_zone,scores={zst=0}] if score @s zid = #zc tmp run function rlk:room/zone_build
playsound minecraft:block.stone.break master @a ~ ~ ~ 0.8 0.6
playsound minecraft:block.iron_door.open master @a ~ ~ ~ 0.6 0.8
