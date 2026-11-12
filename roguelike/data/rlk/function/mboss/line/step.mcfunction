scoreboard players add #mbLnN mb 2
execute if score #mbLnN mb > #mbLnLen mb run scoreboard players operation #mbLnN mb = #mbLnLen mb
execute store result storage rlk:mboss ln.n int 1 run scoreboard players get #mbLnN mb
function rlk:mboss/line/cut with storage rlk:mboss ln
scoreboard players operation #mbLnStay mb = #mbLnGap mb
scoreboard players add #mbLnStay mb 6
execute if score #mbLnN mb >= #mbLnLen mb run scoreboard players operation #mbLnStay mb = #mbLnHold mb
execute store result storage rlk:mboss ln.stay int 1 run scoreboard players get #mbLnStay mb
scoreboard players operation #mbLnTtl mb = #mbLnStay mb
scoreboard players add #mbLnTtl mb 12
function rlk:mboss/line/show with storage rlk:mboss ln
scoreboard players operation @a[tag=player] ttlT = #mbLnTtl mb
execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ 0.3 1 0
execute if score #mbLnN mb >= #mbLnLen mb run scoreboard players set #mbLn mb 0
