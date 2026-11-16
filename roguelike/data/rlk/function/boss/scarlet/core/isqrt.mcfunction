# #bx_r hr = isqrt(#bx_n hr) within 1, 121 <= #bx_n <= 2e7 (Newton from 2000, 8 steps; round X core/sep).
scoreboard players set #bx_r hr 2000
scoreboard players operation #bx_k hr = #bx_n hr
scoreboard players operation #bx_k hr /= #bx_r hr
scoreboard players operation #bx_r hr += #bx_k hr
scoreboard players operation #bx_r hr /= #c2 hr
execute if score #bx_r hr matches ..0 run scoreboard players set #bx_r hr 1
scoreboard players operation #bx_k hr = #bx_n hr
scoreboard players operation #bx_k hr /= #bx_r hr
scoreboard players operation #bx_r hr += #bx_k hr
scoreboard players operation #bx_r hr /= #c2 hr
execute if score #bx_r hr matches ..0 run scoreboard players set #bx_r hr 1
scoreboard players operation #bx_k hr = #bx_n hr
scoreboard players operation #bx_k hr /= #bx_r hr
scoreboard players operation #bx_r hr += #bx_k hr
scoreboard players operation #bx_r hr /= #c2 hr
execute if score #bx_r hr matches ..0 run scoreboard players set #bx_r hr 1
scoreboard players operation #bx_k hr = #bx_n hr
scoreboard players operation #bx_k hr /= #bx_r hr
scoreboard players operation #bx_r hr += #bx_k hr
scoreboard players operation #bx_r hr /= #c2 hr
execute if score #bx_r hr matches ..0 run scoreboard players set #bx_r hr 1
scoreboard players operation #bx_k hr = #bx_n hr
scoreboard players operation #bx_k hr /= #bx_r hr
scoreboard players operation #bx_r hr += #bx_k hr
scoreboard players operation #bx_r hr /= #c2 hr
execute if score #bx_r hr matches ..0 run scoreboard players set #bx_r hr 1
scoreboard players operation #bx_k hr = #bx_n hr
scoreboard players operation #bx_k hr /= #bx_r hr
scoreboard players operation #bx_r hr += #bx_k hr
scoreboard players operation #bx_r hr /= #c2 hr
execute if score #bx_r hr matches ..0 run scoreboard players set #bx_r hr 1
scoreboard players operation #bx_k hr = #bx_n hr
scoreboard players operation #bx_k hr /= #bx_r hr
scoreboard players operation #bx_r hr += #bx_k hr
scoreboard players operation #bx_r hr /= #c2 hr
execute if score #bx_r hr matches ..0 run scoreboard players set #bx_r hr 1
scoreboard players operation #bx_k hr = #bx_n hr
scoreboard players operation #bx_k hr /= #bx_r hr
scoreboard players operation #bx_r hr += #bx_k hr
scoreboard players operation #bx_r hr /= #c2 hr
execute if score #bx_r hr matches ..0 run scoreboard players set #bx_r hr 1
