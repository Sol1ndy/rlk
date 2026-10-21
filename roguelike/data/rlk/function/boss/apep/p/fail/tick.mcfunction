# AP-REV (plan 7.5-7.7, 3.4): the revival stage.
function rlk:boss/apep/heart/tick
execute if score #apPT mb matches 20 run execute unless score #apq40L mb matches 1 run function rlk:boss/apep/p/fail/strike
execute if score #apPT mb matches 60.. run function rlk:boss/apep/p/fail/restart
