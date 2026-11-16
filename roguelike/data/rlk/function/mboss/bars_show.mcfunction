# Order matters: a bar made visible later is drawn below the others.
bossbar set rlk:mboss players @a[tag=player]
bossbar set rlk:mboss_state players @a[tag=player]
bossbar set rlk:mboss_sub players @a[tag=player]
bossbar set rlk:mboss visible true
bossbar set rlk:mboss_state visible true
bossbar set rlk:mboss_sub visible true
scoreboard players set #mbBar mb 1
