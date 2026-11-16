# 보유 칸 구역: 아이템 보유 칸 +#slotGain (최대 18). 잠긴 칸(방벽)이 풀린다
execute as @a[tag=player,limit=1] run function rlk:room/obj/do_slot_p
execute unless score #k17 snd matches 1 run function rlk:snd/f17
execute unless score #k18 snd matches 1 run function rlk:snd/f18
particle minecraft:happy_villager ~ ~ ~ 0.5 0.5 0.5 0 25
function rlk:room/obj/kill_group
