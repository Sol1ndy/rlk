# As the boss: not found. The fakes scatter, the real clone glows; she reforms there 2 t later.
scoreboard players set #rdIlStep rd 2
execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run function rlk:boss/raiden/illusion/dissolve
function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"rest",d:4,look:"glow"}
