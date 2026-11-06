# (FIX perf) the new field one tick after the branding hit (that tick carries the hit, the brand and the
# pattern's own work), here at the same floor point; the next one no sooner than rule_cd ticks later.
scoreboard players operation #aq33C mb = #azClk mb
scoreboard players add #aq33C mb 100
scoreboard players set #azAftF mb 42
scoreboard players set #azAftD mb 1
function rlk:boss/azhdaha/aft/new
