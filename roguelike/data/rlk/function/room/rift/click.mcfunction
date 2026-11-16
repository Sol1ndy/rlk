# From room/obj/click (oact 17; @s = the rift's hover object, at it; clicks during combat are refused there): the
# rift of this zone is entered.
scoreboard players operation #riftZid room = @s zid
execute as @e[type=minecraft:marker,tag=rlk_rift] if score @s zid = #riftZid room at @s run function rlk:room/rift/enter
