# (macro px) a capsule bound to a proxy is active only while that proxy's current column top <= top (tenths).
$execute store result score #t mb run data get storage rlk:mboss px.top.$(px) 10
execute if score #t mb > #pTop mb run scoreboard players set #pAct mb 0
