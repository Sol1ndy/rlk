# @s = the player, at it: a heal filled the cure meter but not to the target: a small rising chime, a short salmon /
# gold dust swirl at the feet (no cards at the eyes: first person, fix PL-1) and the meter on the actionbar.
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.8 1.5 0.27
playsound minecraft:block.note_block.chime hostile @a[tag=player] ~ ~ ~ 0.45 1.8 0.15
particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1} ~ ~0.4 ~ 0.45 0.25 0.45 0 8 force @a[tag=player]
particle minecraft:dust{color:[0.878f,0.867f,0.612f],scale:0.9} ~ ~0.8 ~ 0.35 0.3 0.35 0 6 force @a[tag=player]
function rlk:mboss/butterfly/fx/hud/ab_cure
