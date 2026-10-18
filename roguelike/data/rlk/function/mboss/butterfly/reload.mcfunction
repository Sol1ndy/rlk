# Hook reload (@s = body after /reload; every aux entity is gone: rig parts, props, heal orbs, fx).
# HP is kept. A transformation past its sphere finishes into butterfly form (the cocoon was applied); a
# release goes straight to the groggy in human form; a groggy goes on; otherwise idle in the same form.
function rlk:mboss/butterfly/ai/consts
execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end
execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop
scoreboard players set #bfX mb 0
execute if score #bfPat mb matches 20 if score #bfPT mb matches 6.. run scoreboard players set #bfX mb 1
execute if score #bfPat mb matches 15 run scoreboard players set #bfX mb 2
execute if score #bfSt mb matches 4 run scoreboard players set #bfX mb 3
function rlk:mboss/butterfly/p/cancel
scoreboard players set #mbNoLeash mb 0
scoreboard players set #bfDewN mb 0
scoreboard players set #bfMv mb 0
tag @s remove rlk_mb_inv
function rlk:mboss/butterfly/rig_stub/init
function rlk:mboss/butterfly/rig_stub/spawn
execute if score #bfX mb matches 1 run function rlk:mboss/butterfly/form/set_b
execute if score #bfX mb matches 2 run function rlk:mboss/butterfly/form/set_h
execute if score #bfForm mb matches 2 run function rlk:mboss/butterfly/form/rig_b
execute if score #bfForm mb matches 1 run function rlk:mboss/butterfly/form/rig_h
function rlk:mboss/butterfly/coc/assert
execute if score #bfCoc mb matches 1 if score #bfForm mb matches 2 run function rlk:mboss/butterfly/dew/spawn
execute if score #bfX mb matches 2 run return run function rlk:mboss/butterfly/groggy/begin
execute if score #bfX mb matches 3 run return run function rlk:mboss/butterfly/groggy/end
execute if score #bfSt mb matches 3 run return run function rlk:mboss/butterfly/rig_stub/play/groggy_h
scoreboard players set #bfCool mb 20
function rlk:mboss/butterfly/ai/enter
