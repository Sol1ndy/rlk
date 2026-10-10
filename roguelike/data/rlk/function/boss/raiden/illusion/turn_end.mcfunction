execute as @e[tag=rlk_rd_ilact,limit=1] run function rlk:boss/raiden/illusion/pose {model:"illusion_ready"}
tag @e[tag=rlk_rd_ilact] remove rlk_rd_ilact
scoreboard players add #rdIlTurn rd 1
scoreboard players set #rdIlClock rd 0
# Five slashes (three fakes once, the real one twice) without finding her: over.
execute if score #rdIlSlash rd matches 5.. run return run function rlk:boss/raiden/illusion/fail
execute if score #rdIlTurn rd matches 5.. run function rlk:boss/raiden/illusion/fail
