# E is over (or skipped: /reload, tests): targetable, phase 1 (pool 53 %, floor 1 %), the AI after a short cooldown.
execute store result score #apTot mb run scoreboard players get #mbTot mb
function rlk:mboss/intro_end
function rlk:boss/apep/seq/entrance/done
function rlk:boss/apep/svc/phase_1
function rlk:boss/apep/rig/stance/crouch
function rlk:boss/apep/svc/look_p1
function rlk:boss/apep/play/idle_p1
function rlk:boss/apep/px/p1
scoreboard players set #apPT mb 0
scoreboard players set #apCool mb 20
scoreboard players set #apHudQ mb 1
execute unless score #mbMusPh mb matches 1.. run function rlk:boss/apep/svc/music_1
