# 1 when a kept tail moved her on this or the last tick (#ai_tmc) with the move ai/move_pick would choose now
# (farther than 6 b a walk / glide in, nearer a strafe): the recovery goes on with it (no new pick, the clip plays
# on); else fail (the recovery picks anew).
scoreboard players operation #t hr = #clk hr
scoreboard players operation #t hr -= #ai_tmc hr
execute unless score #t hr matches 0..1 run return fail
execute unless score #ai_mv hr matches 1..3 unless score #ai_mv hr matches 5 run return fail
execute if score #ai_d2 hr matches 360001.. if score #ai_mv hr matches 2..3 run return fail
execute if score #ai_d2 hr matches ..360000 unless score #ai_mv hr matches 2..3 run return fail
return 1
