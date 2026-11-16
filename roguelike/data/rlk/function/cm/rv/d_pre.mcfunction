execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rv_tsel","rlk_rv_pre"]}
execute as @e[tag=rlk_rv_pre] run function rlk:cm/rv/lib/drop
execute store result score #ok2 tmp run function rlk:cm/rv/d_check
kill @e[tag=rlk_rv_pre]
return run scoreboard players get #ok2 tmp
