# @s = body: the cue clock, the hint expiry, the floor popups, the lines every 4 t or on request.
execute if score #azCue mb matches 1.. run scoreboard players remove #azCue mb 1
execute if score #azCue mb matches 0 if score #azHint mb matches 0 run scoreboard players set #azCue mb -1
execute if score #azHint mb matches 1.. if score #azHintT mb <= #azClk mb run scoreboard players set #azHudQ mb 1
execute if score #azHint mb matches 1.. if score #azHintT mb <= #azClk mb run scoreboard players set #azHint mb 0
scoreboard players remove @e[type=minecraft:text_display,tag=rlk_mb_az_pop] azT 1
kill @e[type=minecraft:text_display,tag=rlk_mb_az_pop,scores={azT=..0}]
execute if score #azHudQ mb matches 1 run return run function rlk:mboss/azhdaha/hud/refresh
execute if score #azM mb matches 0 run function rlk:mboss/azhdaha/hud/refresh
