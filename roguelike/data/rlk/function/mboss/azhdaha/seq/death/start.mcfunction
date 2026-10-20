# The death (WORKING STUB, S1-MOD), clip tick 0: the first line, the music stops with a sting.
function rlk:mboss/line/say {t:"난… 사라지지 않아!",c:"#F2B53A",gap:2,hold:50,snd:2}
function rlk:mboss/music/stop
playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
function rlk:mboss/azhdaha/fx/snd/death_sting
