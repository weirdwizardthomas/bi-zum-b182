(define (problem life)
    (:domain sailor)
    (:requirements :strips)
    (:objects
              ; inventory
              alcohol       -    item
              bear_hide     -    item
              coconut       -    item
              pearl         -    item
              treasure_map  -    item
              wood          -    item
              flowers       -    item
              ; vessels
              boat          -    item
              frigate       -    item
              caravel       -    item
              ; gold
              gold_nugget   -    item
              gold_coin     -    item
              gold_bar      -    item
              ; goal items
              coke          -    item
              ring          -    item
              ; locations
              woods         -    location
              river         -    location
              port          -    location
              inn           -    location
              town          -    location
              academy       -    location
              sea           -    location
              lighthouse    -    location
              island        -    location 
              ; intoxication
              sober         -    intoxication_level
              tipsy         -    intoxication_level
              drunk         -    intoxication_level
              alcoholic     -    intoxication_level
              ; status
              tough         -    status
              captain       -    status
              convicted     -    status
              pirates       -    status    
              pirate_slayer -    status
              bear_wrestler -    status
              ; goals
              married       -    goal
              admiral       -    goal
              coke_addict   -    goal
              achieved      -    goal
              g             -    goal ; debugging goal
              ; acquaintance
              dubious       -    acquaintance
              good          -    acquaintance
              smugglers     -    acquaintance
    )
    (:init
              ; connect locations
              (adjacent woods river)
              (adjacent river port)
              (adjacent port inn)
              (adjacent port town)
              (adjacent town academy)
              (adjacent port lighthouse)
              (adjacent port sea)
              (adjacent sea lighthouse)
              (adjacent sea island)
    
              ; ship required
              (requires_ship sea island)
              (requires_ship lighthouse sea)
              (requires_ship port sea)
              (requires_ship lighthouse port)
    
              (intoxication sober)
              (at port)
        )

    (:goal    (and
                  (goal married)
                  (goal coke_addict)
                  (goal admiral)
              )
    )
)
