# pause (as every living boss, without a position; runs on every paused tick). The pattern ends with the
# pause (rdPat 0 after this): the rig goes back to idle once, the guard / counter / stun state goes.
execute unless score @s rdPat matches 0 run function rlk:boss/raiden/sg/idle_clip
scoreboard players set @s rdSgGs 0
scoreboard players set @s rdSgCt 0
scoreboard players set @s rdSgStun 0
scoreboard players set @s rdSgRearQ 0
scoreboard players set @s rdSgFxT 0
kill @e[tag=rlk_rd_sgfx]
execute if entity @a[tag=player,scores={hudHold=1..}] run scoreboard players set @a[tag=player] hudHold 0
