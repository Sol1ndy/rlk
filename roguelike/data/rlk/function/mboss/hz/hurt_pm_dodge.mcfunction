# @s = a per-mille hazard whose hit was avoided (#dodged 1): the dodge event (hurt_dodge), and a perfect dodge consumes
# its volley group as on any hazard (grp_hit: one volley = one answer).
function rlk:mboss/hurt_dodge
scoreboard players operation #g mb = @s mbHzG
execute if score #g mb matches 1.. run function rlk:mboss/grp_hit
