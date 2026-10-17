# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end).
# 16: ground telegraph (24 t) + glint; 26: entrance clip (impact at clip tick 14 = intro 40); 66: fight.
# The rig is not ticked before the clip starts, so the hidden parts stay hidden.
execute if score #mbT mb matches 16 run function rlk:mboss/guardian/intro/tell
execute if score #mbT mb matches 26 run function rlk:mboss/guardian/rig/play/entrance
execute if score #mbT mb matches 26 run function rlk:mboss/guardian/intro/fall
execute if score #mbT mb matches 26..999 run function rlk:mboss/guardian/rig/tick
execute if score #mbT mb matches 27..39 run function rlk:mboss/guardian/intro/trail
execute if score #mbT mb matches 40 run function rlk:mboss/guardian/intro/impact
execute if score #mbT mb matches 52 run playsound minecraft:item.armor.equip_netherite hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.3
execute if score #mbT mb matches 60 run function rlk:mboss/guardian/intro/pullout
execute if score #mbT mb matches 66..999 run function rlk:mboss/guardian/intro/done
