# Hook reload (@s = body after /reload; every aux entity is gone: rig parts, props, heal orbs, fx).
# HP is kept. A transformation past its sphere finishes into butterfly form (the cocoon was applied); a
# release goes straight to the groggy in human form; a groggy goes on; otherwise idle in the same form.
# #bfRl = what to resume (its own score: the helpers below use #bfX as scratch, e.g. dew/spawn1's random
# angle, which used to land on 2 / 3 now and then and start a second groggy).
function rlk:mboss/butterfly/ai/consts
execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end
execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop
scoreboard players set #bfRl mb 0
execute if score #bfPat mb matches 20 if score #bfPT mb matches 6.. run scoreboard players set #bfRl mb 1
execute if score #bfPat mb matches 15 run scoreboard players set #bfRl mb 2
execute if score #bfSt mb matches 4 run scoreboard players set #bfRl mb 3
function rlk:mboss/butterfly/p/cancel
scoreboard players set #mbNoLeash mb 0
scoreboard players set #bfDewN mb 0
scoreboard players set #bfMv mb 0
tag @s remove rlk_mb_inv
function rlk:mboss/butterfly/rig/init
function rlk:mboss/butterfly/rig/spawn
execute if score #bfRl mb matches 1 run function rlk:mboss/butterfly/form/set_b
execute if score #bfRl mb matches 2 run function rlk:mboss/butterfly/form/set_h
execute if score #bfForm mb matches 2 run function rlk:mboss/butterfly/form/rig_b
execute if score #bfForm mb matches 1 run function rlk:mboss/butterfly/form/rig_h
function rlk:mboss/butterfly/coc/assert
execute if score #bfCoc mb matches 1 if score #bfForm mb matches 2 run function rlk:mboss/butterfly/dew/spawn
# the groggy's single 달빛 이슬 (offered while debuffed after 달빛 해제) comes back too (review fix S4)
execute if score #bfDew1 mb matches 1 if score #bfForm mb matches 1 unless score #bfRl mb matches 2 run function rlk:mboss/butterfly/dew/spawn1
execute if score #bfRl mb matches 2 run return run function rlk:mboss/butterfly/groggy/begin
execute if score #bfRl mb matches 3 run return run function rlk:mboss/butterfly/groggy/end
execute if score #bfSt mb matches 3 run return run function rlk:mboss/butterfly/rig/play/groggy_h
scoreboard players set #bfCool mb 20
function rlk:mboss/butterfly/ai/enter
