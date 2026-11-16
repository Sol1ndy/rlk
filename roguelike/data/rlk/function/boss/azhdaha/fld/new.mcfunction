# N6 (s2.md 9): a lingering field here (rotated as the context), args in storage az.nf {fam r len w life dmg sh
# area rule yaw el}: a free slot (else the oldest overall is cancelled), the family cap, the 220 b2 total (the
# oldest of the family first, else the oldest overall), the clear melee points (pattern fields only), the hazard
# (#hzAct = life, #hzRearm 10, the family's volley group, quiet, NoRx), the kit field card, the table.
execute store result score #azNfF mb run data get storage rlk:mboss az.nf.fam
execute store result score #azNfA mb run data get storage rlk:mboss az.nf.area
function rlk:boss/azhdaha/fld/cap_fam
function rlk:boss/azhdaha/fld/cap_area
scoreboard players set #azNfI mb -1
execute if score #azF7 mb matches 0 run scoreboard players set #azNfI mb 7
execute if score #azF6 mb matches 0 run scoreboard players set #azNfI mb 6
execute if score #azF5 mb matches 0 run scoreboard players set #azNfI mb 5
execute if score #azF4 mb matches 0 run scoreboard players set #azNfI mb 4
execute if score #azF3 mb matches 0 run scoreboard players set #azNfI mb 3
execute if score #azF2 mb matches 0 run scoreboard players set #azNfI mb 2
execute if score #azF1 mb matches 0 run scoreboard players set #azNfI mb 1
execute if score #azF0 mb matches 0 run scoreboard players set #azNfI mb 0
execute if score #azNfI mb matches -1 run function rlk:boss/azhdaha/fld/cancel_oldest
execute if score #azNfI mb matches -1 if score #azF7 mb matches 0 run scoreboard players set #azNfI mb 7
execute if score #azNfI mb matches -1 if score #azF6 mb matches 0 run scoreboard players set #azNfI mb 6
execute if score #azNfI mb matches -1 if score #azF5 mb matches 0 run scoreboard players set #azNfI mb 5
execute if score #azNfI mb matches -1 if score #azF4 mb matches 0 run scoreboard players set #azNfI mb 4
execute if score #azNfI mb matches -1 if score #azF3 mb matches 0 run scoreboard players set #azNfI mb 3
execute if score #azNfI mb matches -1 if score #azF2 mb matches 0 run scoreboard players set #azNfI mb 2
execute if score #azNfI mb matches -1 if score #azF1 mb matches 0 run scoreboard players set #azNfI mb 1
execute if score #azNfI mb matches -1 if score #azF0 mb matches 0 run scoreboard players set #azNfI mb 0
kill @e[type=minecraft:marker,tag=rlk_mb_az_fnew]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_fnew"]}
execute rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run tp @s ~ ~ ~ ~ 0
execute unless data storage rlk:mboss az.nf{rule:1} unless data storage rlk:mboss az.nf{sh:1} as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/fld/clear_pts
execute as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/u/clamp_w
execute if score #azNfI mb matches 0 at @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/fld/make_0
execute if score #azNfI mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/fld/make_1
execute if score #azNfI mb matches 2 at @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/fld/make_2
execute if score #azNfI mb matches 3 at @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/fld/make_3
execute if score #azNfI mb matches 4 at @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/fld/make_4
execute if score #azNfI mb matches 5 at @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/fld/make_5
execute if score #azNfI mb matches 6 at @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/fld/make_6
execute if score #azNfI mb matches 7 at @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run function rlk:boss/azhdaha/fld/make_7
kill @e[type=minecraft:marker,tag=rlk_mb_az_fnew]
