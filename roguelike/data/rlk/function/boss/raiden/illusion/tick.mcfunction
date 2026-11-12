# patterns/5: as the boss at its feet every tick of rdPat 5 (rdTime 0 = the choose tick).
# #rdIlStep: 1 clones out (hidden), 2 dissolving (hidden), 3 reformed, 4 found.
execute if score @s rdTime matches 0 run function rlk:boss/raiden/illusion/start
execute if score @s rdTime matches 4 run scoreboard players set #rdIlStep rd 1
execute if score @s rdTime matches 8 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/pillars
execute if score @s rdTime matches 12 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/appear
execute if score @s rdTime matches 26 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/raise
execute if score @s rdTime matches 36 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"high_r",d:3,look:"dark"}
execute if score @s rdTime matches 39 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/volley
execute if score @s rdTime matches 40 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"low_l",d:2,look:"dark"}
execute if score @s rdTime matches 40 if score #rdIlStep rd matches 1 as @e[tag=rlk_rd_illusion] at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 0.8 0.8 0.2
execute if score @s rdTime matches 40 if score #rdIlStep rd matches 1 as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/fx/snd/wave_slab
execute if score @s rdTime matches 41 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"high_l",d:2,look:"dark"}
execute if score @s rdTime matches 43 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"cross_x",d:1,look:"dark"}
execute if score @s rdTime matches 44 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"low_r",d:2,look:"dark"}
execute if score @s rdTime matches 44 if score #rdIlStep rd matches 1 as @e[tag=rlk_rd_illusion,scores={rdReal=1}] at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 0.9 1.1 0.2
execute if score @s rdTime matches 52 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"rest",d:6,look:"dark"}
execute if score @s rdTime matches 82 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/raise
execute if score @s rdTime matches 92 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"high_r",d:3,look:"dark"}
execute if score @s rdTime matches 95 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/volley
execute if score @s rdTime matches 96 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"low_l",d:2,look:"dark"}
execute if score @s rdTime matches 96 if score #rdIlStep rd matches 1 as @e[tag=rlk_rd_illusion] at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 0.8 0.8 0.2
execute if score @s rdTime matches 96 if score #rdIlStep rd matches 1 as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/fx/snd/wave_slab
execute if score @s rdTime matches 97 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"high_l",d:2,look:"dark"}
execute if score @s rdTime matches 99 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"cross_x",d:1,look:"dark"}
execute if score @s rdTime matches 100 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"low_r",d:2,look:"dark"}
execute if score @s rdTime matches 100 if score #rdIlStep rd matches 1 as @e[tag=rlk_rd_illusion,scores={rdReal=1}] at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 0.9 1.1 0.2
execute if score @s rdTime matches 108 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"rest",d:6,look:"dark"}
execute if score @s rdTime matches 138 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/raise
execute if score @s rdTime matches 148 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"high_r",d:3,look:"dark"}
execute if score @s rdTime matches 151 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/volley
execute if score @s rdTime matches 152 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"low_l",d:2,look:"dark"}
execute if score @s rdTime matches 152 if score #rdIlStep rd matches 1 as @e[tag=rlk_rd_illusion] at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 0.8 0.8 0.2
execute if score @s rdTime matches 152 if score #rdIlStep rd matches 1 as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/fx/snd/wave_slab
execute if score @s rdTime matches 153 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"high_l",d:2,look:"dark"}
execute if score @s rdTime matches 155 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"cross_x",d:1,look:"dark"}
execute if score @s rdTime matches 156 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_clreal",p:"low_r",d:2,look:"dark"}
execute if score @s rdTime matches 156 if score #rdIlStep rd matches 1 as @e[tag=rlk_rd_illusion,scores={rdReal=1}] at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 0.9 1.1 0.2
execute if score @s rdTime matches 164 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/clone/pose {sel:"tag=rlk_rd_ilvis",p:"rest",d:6,look:"dark"}
execute if score @s rdTime matches 174 if score #rdIlStep rd matches 1 run function rlk:boss/raiden/illusion/fail
execute if score @s rdTime matches 176 if score #rdIlStep rd matches 2 run function rlk:boss/raiden/illusion/reform
# Lost state (e.g. a reload mid-pattern): end visibly instead of hiding her forever.
execute if score @s rdTime matches 5.. unless score #rdIlStep rd matches 1..3 run return run function rlk:boss/raiden/illusion/lost
execute if score @s rdTime matches 182.. run function rlk:boss/raiden/illusion/end
