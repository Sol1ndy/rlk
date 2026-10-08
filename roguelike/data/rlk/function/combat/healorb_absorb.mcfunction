# @s = 회복구슬. 가장 가까운 플레이어 흡수 → 체력 2 회복
execute as @a[tag=player,limit=1] run function rlk:combat/healorb_heal
particle minecraft:heart ~ ~0.5 ~ 0.3 0.3 0.3 0 10
playsound minecraft:entity.player.levelup master @a ~ ~ ~ 0.5 1.9
kill @s
