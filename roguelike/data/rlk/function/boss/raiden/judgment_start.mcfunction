function rlk:boss/raiden/object/clear
scoreboard players set @s rdUltUsed 1
scoreboard players set @s rdWalk 0
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/judgment_rig/start
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/vfx/judgment_warning
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~ ~ ~3 run function rlk:boss/raiden/object/create {kind:3,model:"remembrance_flower",hp:4,id:1,y:0.05}
# She stays in view: lightning gathers around her and she rises (patterns/15 lifts her).
function rlk:boss/raiden/vfx/judgment_ascend
function rlk:boss/raiden/line/mangeop
playsound minecraft:entity.wither.ambient hostile @a[tag=player] ~ ~ ~ 0.7 0.5 0.3
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.9 0.5 0.3
