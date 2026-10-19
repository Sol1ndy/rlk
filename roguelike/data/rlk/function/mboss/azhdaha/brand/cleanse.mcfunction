# @s = player: the brand and its stacks end (the butterfly-style cure fx and a chime).
execute at @s run function rlk:mboss/azhdaha/kstub/p/cure
function rlk:mboss/azhdaha/kstub/snd/cleanse
execute at @s run playsound minecraft:block.amethyst_block.chime hostile @s ~ ~ ~ 1 1.4 0.33
function rlk:mboss/azhdaha/brand/clear
