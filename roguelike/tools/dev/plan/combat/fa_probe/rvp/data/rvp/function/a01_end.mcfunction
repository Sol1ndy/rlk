data modify storage rvp:log a01 append value {p:0,acc:0}
execute store result storage rvp:log a01[-1].p int 1 run scoreboard players get #per rvp
execute store result storage rvp:log a01[-1].acc int 1 run scoreboard players get @s rvpAcc
scoreboard players set #mode rvp 0
kill @s
