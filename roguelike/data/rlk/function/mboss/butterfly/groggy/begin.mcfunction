# @s = body, after 달빛 해제 (she has just landed in human form): 300 t of groggy: motionless idle, back
# turned to the player, no tracking, no attacks; then the turn and the chain re-form (recover). No damage bonus.
scoreboard players set #bfSt mb 3
scoreboard players set #bfT mb 0
scoreboard players set #mbNoLeash mb 0
scoreboard players set #bfMv mb 0
execute if score #bfForm mb matches 2 run function rlk:mboss/butterfly/form/now_h
function rlk:mboss/butterfly/rig_stub/play/groggy_h
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~180 0
playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
function rlk:mboss/butterfly/hud/refresh
