# Weighted pick, P1, near (api.WEIGHTS; zeroed while cooling down / repeating / beyond MID_MAX).
scoreboard players set #ai_sum hr 0
scoreboard players set #ai_wa1 hr 8
execute if score #cd_a1 hr > #clk hr run scoreboard players set #ai_wa1 hr 0
execute if score #last hr matches 1 run scoreboard players set #ai_wa1 hr 0
scoreboard players operation #ai_sum hr += #ai_wa1 hr
scoreboard players set #ai_wa2 hr 8
execute if score #cd_a2 hr > #clk hr run scoreboard players set #ai_wa2 hr 0
execute if score #last hr matches 2 run scoreboard players set #ai_wa2 hr 0
scoreboard players operation #ai_sum hr += #ai_wa2 hr
scoreboard players set #ai_wa3 hr 30
execute if score #cd_a3 hr > #clk hr run scoreboard players set #ai_wa3 hr 0
execute if score #last hr matches 3 run scoreboard players set #ai_wa3 hr 0
scoreboard players operation #ai_sum hr += #ai_wa3 hr
scoreboard players set #ai_wa3s hr 30
execute if score #cd_a3s hr > #clk hr run scoreboard players set #ai_wa3s hr 0
execute if score #last hr matches 8 run scoreboard players set #ai_wa3s hr 0
scoreboard players operation #ai_sum hr += #ai_wa3s hr
scoreboard players set #ai_wd4 hr 25
execute if score #cd_d4 hr > #clk hr run scoreboard players set #ai_wd4 hr 0
execute if score #last hr matches 9 run scoreboard players set #ai_wd4 hr 0
scoreboard players operation #ai_sum hr += #ai_wd4 hr
scoreboard players set #ai_wrings hr 5
execute if score #cd_rings hr > #clk hr run scoreboard players set #ai_wrings hr 0
execute if score #last hr matches 11 run scoreboard players set #ai_wrings hr 0
scoreboard players operation #ai_sum hr += #ai_wrings hr
scoreboard players set #ai_wa9 hr 20
execute if score #cd_a9 hr > #clk hr run scoreboard players set #ai_wa9 hr 0
execute if score #last hr matches 6 run scoreboard players set #ai_wa9 hr 0
scoreboard players operation #ai_sum hr += #ai_wa9 hr
scoreboard players set #ai_wa10 hr 16
execute if score #cd_a10 hr > #clk hr run scoreboard players set #ai_wa10 hr 0
execute if score #last hr matches 7 run scoreboard players set #ai_wa10 hr 0
scoreboard players operation #ai_sum hr += #ai_wa10 hr
scoreboard players set #ai_wblue hr 15
execute if score #cd_blue hr > #clk hr run scoreboard players set #ai_wblue hr 0
execute if score #last hr matches 14 run scoreboard players set #ai_wblue hr 0
scoreboard players operation #ai_sum hr += #ai_wblue hr
scoreboard players set #ai_wkcut hr 16
execute if score #cd_kcut hr > #clk hr run scoreboard players set #ai_wkcut hr 0
execute if score #last hr matches 15 run scoreboard players set #ai_wkcut hr 0
scoreboard players operation #ai_sum hr += #ai_wkcut hr
execute if score #ai_sum hr matches ..0 run return run function rlk:boss/scarlet/ai/none
execute store result score #ai_r hr run random value 0..999
scoreboard players operation #ai_r hr *= #ai_sum hr
scoreboard players operation #ai_r hr /= #c1000 hr
execute if score #ai_r hr < #ai_wa1 hr run return run function rlk:boss/scarlet/core/start/a1
scoreboard players operation #ai_r hr -= #ai_wa1 hr
execute if score #ai_r hr < #ai_wa2 hr run return run function rlk:boss/scarlet/core/start/a2
scoreboard players operation #ai_r hr -= #ai_wa2 hr
execute if score #ai_r hr < #ai_wa3 hr run return run function rlk:boss/scarlet/core/start/a3
scoreboard players operation #ai_r hr -= #ai_wa3 hr
execute if score #ai_r hr < #ai_wa3s hr run return run function rlk:boss/scarlet/core/start/a3s
scoreboard players operation #ai_r hr -= #ai_wa3s hr
execute if score #ai_r hr < #ai_wd4 hr run return run function rlk:boss/scarlet/core/start/d4
scoreboard players operation #ai_r hr -= #ai_wd4 hr
execute if score #ai_r hr < #ai_wrings hr run return run function rlk:boss/scarlet/core/start/rings
scoreboard players operation #ai_r hr -= #ai_wrings hr
execute if score #ai_r hr < #ai_wa9 hr run return run function rlk:boss/scarlet/core/start/a9
scoreboard players operation #ai_r hr -= #ai_wa9 hr
execute if score #ai_r hr < #ai_wa10 hr run return run function rlk:boss/scarlet/core/start/a10
scoreboard players operation #ai_r hr -= #ai_wa10 hr
execute if score #ai_r hr < #ai_wblue hr run return run function rlk:boss/scarlet/core/start/blue
scoreboard players operation #ai_r hr -= #ai_wblue hr
execute if score #ai_r hr < #ai_wkcut hr run return run function rlk:boss/scarlet/core/start/kcut
scoreboard players operation #ai_r hr -= #ai_wkcut hr
function rlk:boss/scarlet/ai/none
