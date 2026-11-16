# entrance tick 71
execute positioned ~ ~2.1 ~ run function rlk:mboss/butterfly/fx/p/whiteout
function rlk:mboss/butterfly/fx/hud/flash_white
particle minecraft:dust{color:[0.973f,1f,0.753f],scale:2.6} ~ ~2.1 ~ 0.7 1.2 0.7 0 30 force @a[tag=player]
particle minecraft:end_rod ~ ~2.1 ~ 0.3 0.6 0.3 0.12 16 force @a[tag=player]
particle minecraft:flash{color:[0.97,1.0,0.75,1.0]} ~ ~2.1 ~ 0 0 0 0 1 force @a[tag=player]
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.6 1.8 0.2
