# Every gauntlet tick after p/<g>/tick (the core): a cut's hit judged a perfect parry (#mbDodgeOk mb 1 from
# mboss/hurt_dodge with #parT tmp 3) takes one segment; a perfect dodge (#parT 0) takes none. The event is cleared.
execute unless score #mbDodgeOk mb matches 1 run return 0
scoreboard players set #mbDodgeOk mb 0
execute unless score #parT tmp matches 3 run return 0
execute if score #pipoff hr matches 1 run return 0
function rlk:boss/scarlet/shield/take
