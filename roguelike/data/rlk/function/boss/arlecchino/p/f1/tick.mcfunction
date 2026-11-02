# F1 붉은 피의 연회: one pattern tick (#pt kn = 1..232); events in k/<t>.
execute if score #pt kn matches 57..152 run function rlk:mboss/mv/turn {max:6}
execute if score #pt kn matches 6 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.8 0.05 1.8 0 12 force @a[tag=player]
execute if score #pt kn matches 8 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.61 0.05 1.61 0 12 force @a[tag=player]
execute if score #pt kn matches 10 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.43 0.05 1.43 0 12 force @a[tag=player]
execute if score #pt kn matches 12 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.24 0.05 1.24 0 12 force @a[tag=player]
execute if score #pt kn matches 14 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.05 0.05 1.05 0 12 force @a[tag=player]
execute if score #pt kn matches 16 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.86 0.05 0.86 0 12 force @a[tag=player]
execute if score #pt kn matches 18 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.67 0.05 0.67 0 12 force @a[tag=player]
execute if score #pt kn matches 20 at @e[tag=rlk_body,limit=1] positioned ~ ~0.2 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.49 0.05 0.49 0 12 force @a[tag=player]
execute if score #pt kn matches 22 run function rlk:boss/arlecchino/bond/force
execute if score #pt kn matches 40 positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:16}
execute if score #pt kn matches 110 run function rlk:boss/arlecchino/p/f1/k/110
execute if score #pt kn matches 114 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 118 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 122 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 126 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 130 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 134 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 138 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 142 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 146 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 150 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 154 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 158 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 159 run function rlk:boss/arlecchino/p/f1/k/159
execute if score #pt kn matches 160 run function rlk:boss/arlecchino/p/f1/k/160
execute if score #pt kn matches 166 run function rlk:boss/arlecchino/p/f1/k/166
execute if score #pt kn matches 170 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 174 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 178 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 182 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 186 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 190 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 194 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
execute if score #pt kn matches 195 run function rlk:boss/arlecchino/p/f1/k/195
execute if score #pt kn matches 196 run function rlk:boss/arlecchino/p/f1/k/196
execute if score #pt kn matches 200 at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:10}
execute if score #pt kn matches 222 run function rlk:boss/arlecchino/rig_stub/look/wings/off
execute if score #pt kn matches 232 run scoreboard players set #done kn 1
