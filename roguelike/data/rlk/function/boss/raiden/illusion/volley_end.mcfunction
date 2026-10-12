execute as @e[tag=rlk_rd_illusion] run function rlk:boss/raiden/illusion/pose {model:"illusion_ready"}
scoreboard players add #rdIlTurn rd 1
scoreboard players set #rdIlClock rd 0
# Three volleys without finding her: over.
execute if score #rdIlTurn rd matches 3.. run function rlk:boss/raiden/illusion/fail
