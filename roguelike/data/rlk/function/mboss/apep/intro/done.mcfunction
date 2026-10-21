# E is over (or skipped: /reload, tests): targetable, phase 1 (pool 53 %, floor 1 %), the AI after a short cooldown.
execute store result score #apTot mb run scoreboard players get #mbTot mb
function rlk:mboss/intro_end
function rlk:mboss/apep/seq/entrance/done
function rlk:mboss/apep/svc/phase_1
function rlk:mboss/apep/rig_stub/stance/crouch
function rlk:mboss/apep/svc/look_p1
function rlk:mboss/apep/play/idle_p1
function rlk:mboss/apep/px/p1
scoreboard players set #apPT mb 0
scoreboard players set #apCool mb 20
scoreboard players set #apHudQ mb 1
execute unless score #mbMusPh mb matches 1.. run function rlk:mboss/apep/svc/music_1
