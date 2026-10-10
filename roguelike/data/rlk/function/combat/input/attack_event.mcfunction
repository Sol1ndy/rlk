# @s = 발전 과제를 발생시킨 플레이어. interaction 직타도 이 경로로 즉시 전달된다.
advancement revoke @s only rlk:attack
execute unless entity @s[tag=player] run return 0
execute store result score #lcStamp tmp run time query gametime
function rlk:combat/input/attack
