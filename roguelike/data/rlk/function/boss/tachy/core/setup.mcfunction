# @s = the new body: module state, the rig, Pyro blade (G1 start), the intro waits for intro_tick.
function rlk:boss/tachy/init
function rlk:boss/tachy/core/vars
scoreboard players set @s aFire 0
scoreboard players set @s aThunder 0
scoreboard players set @s dFire 0
scoreboard players set @s dThunder 0
function rlk:boss/tachy/rig_stub/init
function rlk:boss/tachy/rig_stub/spawn
function rlk:boss/tachy/rig_stub/look/form/cape
function rlk:boss/tachy/rig_stub/look/visor/up_off
function rlk:boss/tachy/rig_stub/look/edge/off
function rlk:boss/tachy/rig_stub/look/hands/open
function rlk:boss/tachy/el/set1
function rlk:boss/tachy/rig_stub/look/visor/up_off
function rlk:boss/tachy/rig_stub/look/edge/off
data modify storage rlk:mboss sub set value []
