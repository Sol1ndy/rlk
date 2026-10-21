# The orbs appear (cast clock = roar_rear drop - 2): base angle = the facing + 45 (two orbs per side),
# one volley group for all four, the yaw scratch marker, the cue.
function rlk:mboss/azhdaha/p/orbs/kill
scoreboard players set #aq31E mb 600
scoreboard players set #aq31K mb 36000
scoreboard players set #aq31W mb 0
scoreboard players set #aq31C mb 0
execute store result score #aq31A mb run data get entity @s Rotation[0] 100
scoreboard players add #aq31A mb 4500
function rlk:mboss/grp_new
function rlk:mboss/azhdaha/p/orbs/mk0
function rlk:mboss/azhdaha/p/orbs/mk1
function rlk:mboss/azhdaha/p/orbs/mk2
function rlk:mboss/azhdaha/p/orbs/mk3
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p31","rlk_mb_az_p31y"]}
function rlk:mboss/azhdaha/fx/snd/orb_spawn
function rlk:mboss/azhdaha/fx/p/splash
