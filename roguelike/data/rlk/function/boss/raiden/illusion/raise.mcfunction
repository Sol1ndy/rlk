execute as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/raise_one
function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"ready",d:6,look:"dark"}
playsound minecraft:item.trident.return hostile @a[tag=player] ~ ~ ~ 0.6 1.25 0.2
