# Same tick as its hazard strike: follow-through pose, swing arc and flying wave.
function rlk:boss/raiden/illusion/pose {model:"illusion_slash"}
function rlk:boss/raiden/object_vfx/slash
scoreboard players add #rdIlSlash rd 1
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 1 0.8 0.2
