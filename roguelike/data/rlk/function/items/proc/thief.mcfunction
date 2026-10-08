scoreboard players operation #thiefCd itv = #thiefCdT tmp
scoreboard players operation @a[tag=player,limit=1] gold += #thiefGold tmp
execute as @a[tag=player,limit=1] at @s run playsound minecraft:block.chain.place master @s ~ ~ ~ 0.4 1.8
