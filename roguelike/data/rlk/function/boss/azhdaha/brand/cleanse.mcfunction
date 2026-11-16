# @s = player: the brand and its stacks end (the butterfly-style cure fx and a chime).
execute at @s run function rlk:boss/azhdaha/fx/p/cure
function rlk:boss/azhdaha/fx/snd/cleanse
execute at @s run playsound minecraft:block.amethyst_block.chime hostile @s ~ ~ ~ 1 1.4 0.33
function rlk:boss/azhdaha/brand/clear
