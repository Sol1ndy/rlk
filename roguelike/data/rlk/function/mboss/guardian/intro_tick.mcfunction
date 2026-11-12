# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end).
# 16: sky glint + the plant hazard (quiet, 18 t); 20: entrance clip (impact at clip tick 14 = intro 34); 60: fight.
# The rig is not ticked before the clip starts, so the hidden parts stay hidden.
execute if score #mbT mb matches 16 run function rlk:mboss/guardian/intro/tell
execute if score #mbT mb matches 20 run function rlk:mboss/guardian/rig/play/entrance
execute if score #mbT mb matches 20 run function rlk:mboss/guardian/intro/fall
execute if score #mbT mb matches 20..999 run function rlk:mboss/guardian/rig/tick
execute if score #mbT mb matches 21..33 run function rlk:mboss/guardian/intro/trail
execute if score #mbT mb matches 34 run function rlk:mboss/guardian/intro/impact
execute if score #mbT mb matches 46 run playsound minecraft:item.armor.equip_netherite hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.2
execute if score #mbT mb matches 54 run function rlk:mboss/guardian/intro/pullout
execute if score #mbT mb matches 60..999 run function rlk:mboss/guardian/intro/done
