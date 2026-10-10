scoreboard players operation #rdOvOwner rd = @s rdOvId
scoreboard players set #rdOvExists rd 0
execute as @e[tag=rlk_rd_object] if score @s rdOvId = #rdOvOwner rd run scoreboard players set #rdOvExists rd 1
