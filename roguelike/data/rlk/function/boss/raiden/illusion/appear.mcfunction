# As the boss: the four clones (object kind 2, 1 hit) on the spots, facing the player; one is real (its parts are
# tagged rlk_rd_clreal, the others rlk_rd_clfake: the real one alone cuts the X).
execute as @e[tag=rlk_rd_ilspot,scores={rdObjId=1},limit=1] at @s run function rlk:boss/raiden/object/create {kind:2,model:"prop/clone_ready_dark",hp:1,id:1,y:1.375}
execute as @e[tag=rlk_rd_ilspot,scores={rdObjId=2},limit=1] at @s run function rlk:boss/raiden/object/create {kind:2,model:"prop/clone_ready_dark",hp:1,id:2,y:1.375}
execute as @e[tag=rlk_rd_ilspot,scores={rdObjId=3},limit=1] at @s run function rlk:boss/raiden/object/create {kind:2,model:"prop/clone_ready_dark",hp:1,id:3,y:1.375}
execute as @e[tag=rlk_rd_ilspot,scores={rdObjId=4},limit=1] at @s run function rlk:boss/raiden/object/create {kind:2,model:"prop/clone_ready_dark",hp:1,id:4,y:1.375}
execute as @e[tag=rlk_rd_object,scores={rdObjKind=2},tag=!rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/adopt
execute as @e[tag=rlk_rd_illusion,sort=random,limit=1] run scoreboard players set @s rdReal 1
execute as @e[tag=rlk_rd_illusion,scores={rdReal=1},limit=1] run scoreboard players operation #rdIlId rd = @s rdObjId
execute as @e[type=minecraft:item_display,tag=rlk_rd_clp] if score @s rdObjId = #rdIlId rd run tag @s add rlk_rd_clreal
tag @e[type=minecraft:item_display,tag=rlk_rd_clp,tag=!rlk_rd_clreal] add rlk_rd_clfake
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~1 ~ 1 1.15 0.2
