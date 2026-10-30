# Hook death_start (@s = body; hazards cleared, bars hidden, proxies in "dead", the music stopped).
scoreboard players set #cpPat mb 0
scoreboard players set #cpPush mb 0
function rlk:mboss/cproto/rig/unglow
function rlk:mboss/cproto/rig/play {c:3}
function rlk:mboss/line/say {t:"...틀은 멀쩡하군.",c:"#9FC6E8",gap:2,hold:30,snd:2}
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
