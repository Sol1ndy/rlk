# One 달빛 이슬 (still debuffed during the groggy): it stays until it is taken, the next transformation's
# sphere or the next butterfly form's end; #bfDew1 = it is offered (a /reload brings it back, fix S4).
function rlk:mboss/butterfly/dew/clear
scoreboard players set #bfDew1 mb 1
scoreboard players set #bfDewP mb 0
execute store result score #bfX mb run random value 0..359
function rlk:mboss/butterfly/dew/one
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
