# @s = 플레이어. 방어막 #amt 획득(더 클 때만 교체), 15초 유지. 결정이면 #shEl = 원소(그 원소 피해를 250% 효율로 막고 색이 바뀜), 아니면 0
execute unless score @s shieldHP >= #amt tmp run scoreboard players operation @s shieldHP = #amt tmp
scoreboard players operation @s shieldEl = #shEl tmp
scoreboard players set #shEl tmp 0
scoreboard players set @s shieldT 300
execute unless score #k38 snd matches 1 run function rlk:snd/f40
execute unless score #k39 snd matches 1 run function rlk:snd/f41
