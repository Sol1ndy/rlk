# exit back: the unit direction x1000 of the anchor frame in the world.
scoreboard players set #pDir mb 4
scoreboard players operation #pux mb = #fx mb
scoreboard players operation #puz mb = #fz mb
scoreboard players operation #pux mb *= #cm1 mb
scoreboard players operation #puz mb *= #cm1 mb
