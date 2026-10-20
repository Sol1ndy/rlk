scoreboard players set #aq31K mb 36000
scoreboard players set #aq31W mb 0
scoreboard players operation #aq31C mb = #azBgLT mb
scoreboard players add #aq31C mb 1
function rlk:mboss/grp_new
function rlk:mboss/azhdaha/p/orbs/mk0
function rlk:mboss/azhdaha/p/orbs/mk1
function rlk:mboss/azhdaha/p/orbs/mk2
function rlk:mboss/azhdaha/p/orbs/mk3
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p31","rlk_mb_az_p31y"]}
execute if score #azBgLT mb matches 10.. as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d] run data merge entity @s {transformation:{scale:[2.6f,2.6f,2.6f]}}
