# #brd view = isqrt(#brn view), 400 <= #brn <= 3.1e6 (Newton from 1500, 7 steps; view/body_rule)
scoreboard players set #brd view 1500
scoreboard players operation #brk view = #brn view
scoreboard players operation #brk view /= #brd view
scoreboard players operation #brd view += #brk view
scoreboard players operation #brd view /= #2 tmp
execute if score #brd view matches ..0 run scoreboard players set #brd view 1
scoreboard players operation #brk view = #brn view
scoreboard players operation #brk view /= #brd view
scoreboard players operation #brd view += #brk view
scoreboard players operation #brd view /= #2 tmp
execute if score #brd view matches ..0 run scoreboard players set #brd view 1
scoreboard players operation #brk view = #brn view
scoreboard players operation #brk view /= #brd view
scoreboard players operation #brd view += #brk view
scoreboard players operation #brd view /= #2 tmp
execute if score #brd view matches ..0 run scoreboard players set #brd view 1
scoreboard players operation #brk view = #brn view
scoreboard players operation #brk view /= #brd view
scoreboard players operation #brd view += #brk view
scoreboard players operation #brd view /= #2 tmp
execute if score #brd view matches ..0 run scoreboard players set #brd view 1
scoreboard players operation #brk view = #brn view
scoreboard players operation #brk view /= #brd view
scoreboard players operation #brd view += #brk view
scoreboard players operation #brd view /= #2 tmp
execute if score #brd view matches ..0 run scoreboard players set #brd view 1
scoreboard players operation #brk view = #brn view
scoreboard players operation #brk view /= #brd view
scoreboard players operation #brd view += #brk view
scoreboard players operation #brd view /= #2 tmp
execute if score #brd view matches ..0 run scoreboard players set #brd view 1
scoreboard players operation #brk view = #brn view
scoreboard players operation #brk view /= #brd view
scoreboard players operation #brd view += #brk view
scoreboard players operation #brd view /= #2 tmp
execute if score #brd view matches ..0 run scoreboard players set #brd view 1
