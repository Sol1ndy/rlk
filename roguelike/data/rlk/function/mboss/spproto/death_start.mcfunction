# Hook death_start (@s = body; hazards cleared, bars hidden, music stopped).
scoreboard players set #spPat mb 0
function rlk:mboss/spproto/rig/unglow
function rlk:mboss/spproto/rig/sink
function rlk:mboss/line/say {t:"균열이... 닫힌다.",c:"#8FD8FF",gap:2,hold:30,snd:2}
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
