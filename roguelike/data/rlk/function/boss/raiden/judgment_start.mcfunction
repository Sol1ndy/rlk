function rlk:boss/raiden/object/clear
scoreboard players set @s rdUltUsed 1
scoreboard players set @s rdWalk 0
function rlk:boss/raiden/movement/depart
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/judgment_rig/start
# The body is hidden from this frame (tick hides rdPat 15), so this move is never seen.
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~ ~ ~-8 run tp @s ~ ~ ~ 0 0
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/vfx/judgment_warning
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~ ~ ~3 run function rlk:boss/raiden/object/create {kind:3,model:"remembrance_flower",hp:4,id:1,y:0.05}
title @a[tag=player] times 4 85 16
title @a[tag=player] subtitle {text:"꽃을 공격 → 보호막 안으로! 번개 1타 / 다른 공격 4타",color:"aqua",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 105
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
playsound minecraft:entity.wither.ambient hostile @a[tag=player] ~ ~ ~ 0.7 0.5 0.3
