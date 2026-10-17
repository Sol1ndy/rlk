# Fail spears tick (@s = body, #gdPT = ticks since T0). Spear j (0, 1) for every surviving star:
# decal + locked target at 25 + 31j, impact 24 t later, cylinder r 2.8 (K12).
execute if score #gdPT mb matches 25 if score #gdFailN mb matches 1.. run function rlk:mboss/guardian/p/fail/lock0
execute if score #gdPT mb matches 26..48 if score #gdFailN mb matches 1.. at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] run particle minecraft:dust{color:[0.75f,0.1f,0.18f],scale:1.4} ~ ~0.15 ~ 1.8 0.02 1.8 0 4 force @a[tag=player]
execute if score #gdPT mb matches 38 if score #gdFailN mb matches 1.. run function rlk:mboss/guardian/p/fail/tint0
execute if score #gdPT mb matches 45 if score #gdFailN mb matches 1.. run playsound minecraft:item.trident.riptide_3 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.3
execute if score #gdPT mb matches 49 if score #gdFailN mb matches 1.. run function rlk:mboss/guardian/p/fail/drop0
execute if score #gdPT mb matches 79 if score #gdFailN mb matches 1.. run function rlk:mboss/guardian/p/fail/fade0
execute if score #gdPT mb matches 56 if score #gdFailN mb matches 2.. run function rlk:mboss/guardian/p/fail/lock1
execute if score #gdPT mb matches 57..79 if score #gdFailN mb matches 2.. at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[0.75f,0.1f,0.18f],scale:1.4} ~ ~0.15 ~ 1.8 0.02 1.8 0 4 force @a[tag=player]
execute if score #gdPT mb matches 69 if score #gdFailN mb matches 2.. run function rlk:mboss/guardian/p/fail/tint1
execute if score #gdPT mb matches 76 if score #gdFailN mb matches 2.. run playsound minecraft:item.trident.riptide_3 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.3
execute if score #gdPT mb matches 80 if score #gdFailN mb matches 2.. run function rlk:mboss/guardian/p/fail/drop1
execute if score #gdPT mb matches 110 if score #gdFailN mb matches 2.. run function rlk:mboss/guardian/p/fail/fade1
execute if score #gdFailN mb matches 1 if score #gdPT mb matches 80 run function rlk:mboss/guardian/p/end
execute if score #gdFailN mb matches 2.. if score #gdPT mb matches 111 run function rlk:mboss/guardian/p/end
execute unless score #gdFailN mb matches 1.. run function rlk:mboss/guardian/p/end
