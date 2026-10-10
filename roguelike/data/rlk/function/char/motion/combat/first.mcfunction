# Execute the original damage pipeline at the impact frame.
scoreboard players set @s pmAtkPending 0
execute unless score @s pmAtkKind = #charN tmp run return 0
scoreboard players operation @s comboStep = @s pmAtkStep
scoreboard players set @s swungAt -1
scoreboard players set #pmResolving tmp 1
function rlk:combat/find_immediate
scoreboard players set #pmResolving tmp 0
# The motion timeline owns double-hit timing, so stop the old fixed 3-tick queues.
scoreboard players set @s skQ 0
scoreboard players set @s naQ 0
execute if score @s pmSecond matches 1.. run scoreboard players set @s pmAtkPending 2
