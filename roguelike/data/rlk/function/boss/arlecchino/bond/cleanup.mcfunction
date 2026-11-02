# The end of the fight (cleanup / won / cancel / defeat; any executor): what she bonded is taken back
# (min(bol, #given): a Clorinde / Arlecchino player keeps the bond of her own kit; no on_clear hooks), the
# shock and her heal orbs are gone.
execute as @a[tag=player,limit=1] run function rlk:boss/arlecchino/bond/remove
scoreboard players set #given kn 0
scoreboard players set #bonded kn 0
scoreboard players set #shock kn 0
scoreboard players set #shk_hit kn 0
scoreboard players set #dot_t kn 0
scoreboard players set #mbBolRe mb 100
scoreboard players set #mbHitBol mb 0
kill @e[type=minecraft:item,tag=rlk_kn_orb]
