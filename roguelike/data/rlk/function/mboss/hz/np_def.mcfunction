# @s = a new hazard without an explicit #hzNoParry (combat overhaul C; the user's 11-10 choice: only some big boss attacks
# are unparriable - area attacks and grabs; review B-01). Unparriable by default only what a parry cannot answer by its
# nature: a no-dodge hazard (#hzNoDodge: a jump / safe-zone / position check), a per-mille hit (#hzPm), a re-arming one
# (#hzRearm: a lingering field or beam), the full arena (kind 5) and a mask (kind 6). Everything else - a line, sector, disc
# or ring of any size - is parryable unless its module says mboss_lib.hz_opts(noparry=1) (the module's short list of big
# hits); every projectile is parryable unless it is no-dodge or says pj_opts(noparry=1).
scoreboard players set @s mbHzNP 0
execute if score @s mbHzND matches 1 run return run scoreboard players set @s mbHzNP 1
execute if score @s mbHzPm matches 1.. run return run scoreboard players set @s mbHzNP 1
execute if score @s mbHzRA matches 1.. run return run scoreboard players set @s mbHzNP 1
execute if score @s mbHzK matches 5..6 run scoreboard players set @s mbHzNP 1
