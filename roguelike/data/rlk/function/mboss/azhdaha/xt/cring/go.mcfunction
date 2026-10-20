# 1 t before the strike (as the body at the ring centre): the kit's travelling Cryo front, the sound,
# then the growth chain from the strike + 1.
function rlk:mboss/azhdaha/fx/p/front/4 {r0:15,r1:60,w:15,dur:6}
playsound minecraft:block.powder_snow.break hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
scoreboard players set #azAftF mb 2
scoreboard players set #azAftD mb 2
function rlk:mboss/azhdaha/aft/new
