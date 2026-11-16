# MX ended (@s = body): at <= 30 % of her HP it repeats once at once, 60 % (the video's second X; the
# no-repeat rule does not apply). Returns 1 when it started again.
scoreboard players operation #t4 hr = #mx_rep hr
scoreboard players set #mx_rep hr 0
execute if score #t4 hr matches 1 run return fail
execute if score #fl hr matches 1.. run return fail
execute if score #lock hr matches 1 run return fail
scoreboard players operation #t hr = @s mhpC
scoreboard players operation #t hr *= #c100 hr
scoreboard players operation #t2 hr = @s mhpM
scoreboard players set #t3 hr 30
scoreboard players operation #t2 hr *= #t3 hr
execute if score #t hr > #t2 hr run return fail
execute store result score #t hr run random value 1..100
execute if score #t hr matches 61.. run return fail
function rlk:boss/scarlet/core/start/mx
scoreboard players set #mx_rep hr 1
return 1
