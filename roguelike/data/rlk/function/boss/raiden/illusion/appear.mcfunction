# As the boss: the four clones (object kind 2, 1 hit) on the spots, facing the player; one is real.
execute as @e[tag=rlk_rd_ilspot,scores={rdObjId=1},limit=1] at @s run function rlk:boss/raiden/object/create {kind:2,model:"prop/clone_slash_dark",hp:1,id:1,y:1.375}
execute as @e[tag=rlk_rd_ilspot,scores={rdObjId=2},limit=1] at @s run function rlk:boss/raiden/object/create {kind:2,model:"prop/clone_slash_dark",hp:1,id:2,y:1.375}
execute as @e[tag=rlk_rd_ilspot,scores={rdObjId=3},limit=1] at @s run function rlk:boss/raiden/object/create {kind:2,model:"prop/clone_slash_dark",hp:1,id:3,y:1.375}
execute as @e[tag=rlk_rd_ilspot,scores={rdObjId=4},limit=1] at @s run function rlk:boss/raiden/object/create {kind:2,model:"prop/clone_slash_dark",hp:1,id:4,y:1.375}
execute as @e[tag=rlk_rd_object,scores={rdObjKind=2},tag=!rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/adopt
execute as @e[tag=rlk_rd_illusion,sort=random,limit=1] run scoreboard players set @s rdReal 1
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~1 ~ 1 1.15 0.2
