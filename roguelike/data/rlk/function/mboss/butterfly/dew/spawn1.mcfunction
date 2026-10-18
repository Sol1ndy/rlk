# One 달빛 이슬 (still debuffed during the groggy).
execute store result score #bfX mb run random value 0..359
function rlk:mboss/butterfly/dew/one
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
