# As the boss on the real clone's spot: she reforms, 「간파했군.」, stun 100 t (then 7).
tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute rotated as @s run tp @s ~ ~ ~ ~ 0
function rlk:boss/raiden/rig/play/blink_in
function rlk:boss/raiden/movement/arrive
function rlk:boss/raiden/line/ganpa
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~1 ~ 0.8 0.9 0.2
scoreboard players remove @s rdRage 120
execute if score @s rdRage matches ..-1 run scoreboard players set @s rdRage 0
function rlk:boss/raiden/illusion/reset
scoreboard players set @s rdSgStun 1
function rlk:boss/raiden/sg/stun_begin
