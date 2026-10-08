$execute if score #n tmp matches $(n).. run data modify storage rlk:eng lq set from storage rlk:eng tq[0].on
$execute unless score #n tmp matches $(n).. run data modify storage rlk:eng lq set from storage rlk:eng tq[0].off
