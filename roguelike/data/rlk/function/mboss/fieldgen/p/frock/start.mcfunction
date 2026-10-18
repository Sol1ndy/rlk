# F2 파쇄 (clip frock; @s = body at the centre): bursts strike from 25 every 6 t (arc onto the
# player, 7-8 one group), throws from 65 every 8 t (at most 2 slab hits), crumble 100, end 110.
scoreboard players set #fq12SH mb 0
scoreboard players set #fq12P mb 0
execute store result score #fq12S mb run random value 0..1
execute if score #fq12S mb matches 0 run scoreboard players set #fq12S mb -1
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p12w]
execute positioned ~ ~6.5 ~ run function rlk:mboss/fieldgen/fx/p/vent_flare
function rlk:mboss/fieldgen/fx/snd/vent_flare
