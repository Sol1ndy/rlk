# The player stayed behind her (20 of 30 t): A1 (no immediate repeat); its cooldown is
# ignored once per 200 t. Fails when it may not run; F1 (HR-26): only inside the near band
# (4.5 b): farther, the far rule / the band pick decide.
execute unless score #ai_d2 hr matches ..202500 run return fail
execute if score #last hr matches 1 run return fail
execute if score #cd_a1 hr <= #clk hr run return run function rlk:boss/scarlet/ai/rear_go
scoreboard players operation #t hr = #clk hr
scoreboard players operation #t hr -= #ai_rcd hr
execute if score #t hr matches ..199 run return fail
scoreboard players operation #ai_rcd hr = #clk hr
return run function rlk:boss/scarlet/ai/rear_go
