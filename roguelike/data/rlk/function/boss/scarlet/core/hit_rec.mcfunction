# A player hit on her while she recovers / idles (on_hit; scores only): the last 4 hit times (#h1..#h4); 4
# in 40 t -> the counter trigger (#ctr, resolved by the next fight tick); every 4th -> the flinch.
scoreboard players operation #h4 hr = #h3 hr
scoreboard players operation #h3 hr = #h2 hr
scoreboard players operation #h2 hr = #h1 hr
scoreboard players operation #h1 hr = #clk hr
scoreboard players add #hits hr 1
scoreboard players operation #t5 hr = #hits hr
scoreboard players set #t4 hr 4
scoreboard players operation #t5 hr %= #t4 hr
execute if score #t5 hr matches 0 run scoreboard players set #flq hr 1
execute if score #hits hr matches ..3 run return 0
scoreboard players operation #t5 hr = #clk hr
scoreboard players operation #t5 hr -= #h4 hr
execute if score #t5 hr matches ..40 run scoreboard players set #ctr hr 1
