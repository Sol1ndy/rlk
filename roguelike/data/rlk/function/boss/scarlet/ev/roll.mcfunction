# The event roll (PLAN §7.3.1; death_start, or the reward hook when the ending never reached it): #hrEv 1 item / 2 buff.
scoreboard players set #hrEv hr 0
scoreboard players set #hrEvDone hr 0
scoreboard players set #hrEvDrop hr 0
execute if data storage rlk:hr {ev:{force:"item"}} run return run scoreboard players set #hrEv hr 1
execute if data storage rlk:hr {ev:{force:"buff"}} run return run scoreboard players set #hrEv hr 2
execute as @a[tag=player,limit=1] if score @s it_sword_hwamu matches 1.. run return run scoreboard players set #hrEv hr 2
execute as @a[tag=player,limit=1] if score @s hrMoon matches 1.. run return run scoreboard players set #hrEv hr 1
execute store result score #t hr run random value 1..1000
execute if score #t hr matches ..500 run return run scoreboard players set #hrEv hr 1
scoreboard players set #hrEv hr 2
