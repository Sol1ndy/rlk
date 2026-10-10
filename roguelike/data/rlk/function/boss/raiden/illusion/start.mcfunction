# rdTime 1, as the boss where the previous move left it. Leftovers go silently.
execute as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/vanish
kill @e[type=minecraft:item_display,tag=rlk_rd_ilvis]
function rlk:boss/raiden/object/clear
scoreboard players set @s rdWalk 0
scoreboard players set @s rdBlink 0
kill @e[tag=rlk_rd_blink_dest]
scoreboard players set #rdIlStep rd 1
scoreboard players set #rdIlClock rd 0
scoreboard players set #rdIlTurn rd 1
scoreboard players set #rdIlSlash rd 0
scoreboard players set #rdIlShots rd 0
# She scatters where she stands; the hidden body crosses to the centre this frame.
function rlk:boss/raiden/movement/depart
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~1 ~ 0.9 0.75 0.2
execute at @e[tag=rlk_raiden_arena,limit=1] run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
title @a[tag=player] times 3 36 10
title @a[tag=player] subtitle {text:"검격을 두 번 날리는 분신이 진짜 · 찾아서 공격하세요",color:"light_purple"}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 49
scoreboard players set #rdCap rd 1
scoreboard players set #rdCapPat rd 1
