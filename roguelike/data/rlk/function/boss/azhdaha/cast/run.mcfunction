# @s = body: the cast slot clock and the special's ctick.
scoreboard players add #azCT mb 1
execute if score #azCast mb matches 31 run return run function rlk:boss/azhdaha/p/orbs/ctick
execute if score #azCast mb matches 32 run return run function rlk:boss/azhdaha/p/meteor/ctick
