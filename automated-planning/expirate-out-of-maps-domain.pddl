
(define (domain sailor)

    (:requirements
                  :negative-preconditions
                  :typing
                  :strips
    )

    (:types 
        player
        location
        item
        status
        goal
        acquaintance
        intoxication_level
    )

    (:predicates
        (adjacent ?a - location ?b - location)          ; tile 'a' borders tile 'b', transitive
        (at ?l - location)                              ; player 'p' is at location 'location'
        (requires_ship ?from - location ?to - location) ; moving 'from' to 'to' requires a ship to traverse, transitive
        (status ?s - status)                            ; captain, conviction, tough, wooed
        (acquaintance ?a - acquaintance)                ; dubious, serious, smugglers
        (has ?i - item)                                 ; item possession
        (intoxication ?level - intoxication_level)      ; level of intoxication - sober, tipsy, drunk, alcoholic
        (seaworthy)                                     ; can travel by sea
        (goal ?g - goal)                                ; goal of the game - married, admiral, coke, g
    )

    ; movement actions -------------------------------------------------------------------------------------------------
    (:action sail
     :parameters   (?from - location ?to - location)
     :precondition (and
                       (at ?from)                          
                       (or
                          (adjacent ?from ?to)
                          (adjacent ?to ?from)
                       )
                       (or
                          (requires_ship ?from ?to)
                          (requires_ship ?to ?from)
                       )
                       (seaworthy)
                   )
    :effect        (and
                       (not (at ?from))
                       (at ?to)
                   )
    )

    (:action walk
     :parameters (?from - location ?to - location)
     :precondition (and 
                       (at ?from)
                       (or
                          (adjacent ?from ?to)
                          (adjacent ?to ?from)
                       )
                       (not (requires_ship ?from ?to))
                       (not (requires_ship ?to ?from))
                   )
     :effect       (and
                       (not (at ?from))
                       (at ?to)
                   )
    )

    ; vessel actions ---------------------------------------------------------------------------------------------------
    (:action build_boat
     :parameters   ()
     :precondition (and (has wood))
     :effect       (and
                       ; spend resources
                       (not (has wood))
                       ; gain a vessel
                       (has boat)
                       (seaworthy)
                   )
    )

    (:action build_frigate
     :parameters   ()
     :precondition (and
                       (has boat)
                       (has gold_nugget)
                       (has wood)
                   )
     :effect       (and
                       ; spend resources
                       (not (has wood))
                       (not (has golden_nugget))
                       (not (has boat))
                       ; gain a vessel
                       (has frigate)
                   )
    )

    (:action build_caravel
     :parameters   ()
     :precondition (and
                       (has boat)
                       (has gold_coin)
                       (has wood)
                   )
     :effect       (and
                       ; spend resources
                       (not (has boat))
                       (not (has gold_coin))
                       (not (has wood))
                       ; gain a vessel
                       (has caravel)
                   )
    )

    ; drinking actions -------------------------------------------------------------------------------------------------
    (:action drink_sober ; sober -> tipsy
     :parameters   ()
     :precondition (and
                       (has alcohol)
                       (intoxication sober)
                   )
     :effect       (and
                       (not (has alcohol))
                       (not (intoxication sober))
                       (intoxication tipsy)
                   )
    )

    (:action drink_tipsy ; tipsy -> drunk
     :parameters   ()
     :precondition (and
                       (has alcohol)
                       (intoxication tipsy)
                   )
     :effect       (and
                       (not (has alcohol))
                       (not (intoxication tipsy))
                       (intoxication drunk)
                   )
    )

    (:action drink_drunk ; drunk -> alcoholic
     :parameters   ()
     :precondition (and
                       (has alcohol)
                       (intoxication drunk)
                   )
     :effect       (and
                       (not (has alcohol))
                       (intoxication drunk)
                       (intoxication alcoholic)
                   )
    )

    ; woods actions -----------------------------------------------------------------------------------------------------
    (:action chop_wood
     :parameters   ()
     :precondition (or
                      (at woods)
                      (at island)
                   )
     :effect       (and (has wood))
    )

     (:action pick_flowers
      :parameters   ()
      :precondition (and (at woods))
      :effect       (and (has flowers))
    )

    (:action meet_retired_pirate
     :parameters   ()
     :precondition (and
                       (at woods)
                       (has alcohol)
                   )
     :effect       (and
                       (not (has alcohol))
                       (acquaintance dubious)
                   )
    )

    (:action wrestle_bear
     :parameters   ()
     :precondition (and (at woods))
     :effect       (and
                       (has bear_hide)
                       (status bear_wrestler)
                       (status tough)
                   )
    )

    ; river actions ----------------------------------------------------------------------------------------------------
    (:action steal_boat
     :parameters   ()
     :precondition (and (at river))
     :effect       (and
                       (status convicted)
                       (has boat)
                       (seaworthy)
                   )
    )

    (:action pan
     :parameters    ()
     :precondition  (and (at river))
     :effect        (and (has gold_nugget))
    )

    (:action bathe
     :parameters   ()
     :precondition (or
                       (at river)
                       (at sea)
                   )
     :effect       (and
                       (intoxication sober)
                       (not (intoxication tipsy))
                       (not (intoxication drunk))
                   )
    )

    ; port actions -----------------------------------------------------------------------------------------------------
    (:action work
     :parameters   ()
     :precondition (and
                       (at port)
                       (intoxication sober)
                   )
     :effect       (and (has gold_nugget))
    )

    (:action trade
     :parameters   (?i - item)
     :precondition (and
                       (at port)
                       (has ?i)
                       (or
                          (= ?i bear_hide)
                          (= ?i coconut)
                       )
                   )
     :effect       (and
                       (not (has ?i))
                       (has gold_coin))
    )

    (:action meet_smugglers
     :parameters   ()
     :precondition (and
                       (at port)
                       (acquaintance dubious)
                       (has gold_bar)
                   )
     :effect       (and (acquaintance smugglers))
    )

    ; inn actions ------------------------------------------------------------------------------------------------------
    (:action buy_alcohol
     :parameters   ()
     :precondition (and (has gold_nugget))
     :effect       (and
                       (at inn)
                       (not (has gold_nugget))
                       (has alcohol)
                   )
    )

    (:action buy_drinks
     :parameters   ()
     :precondition (and (has gold_coin))
     :effect       (and
                       (at inn)
                       (acquaintance good)
                       (not (has gold_coin))
                   )
    )

    (:action brawl
     :parameters   ()
     :precondition (and
                       (at inn)
                       (intoxication tipsy)
                   )
     :effect       (and (status tough))
    )
    
    ; town actions -----------------------------------------------------------------------------------------------------
    (:action save
     :parameters   ()
     :precondition (and
                       (at town)
                       (has gold_nugget)
                   )
     :effect       (and
                       (not (has gold_nugget))
                       (has gold_coin)
                       (acquaintance good)
                   )
    )

    (:action invest
     :parameters   ()
     :precondition (and
                       (at town)
                       (has gold_coin)
                   )
     :effect       (and
                       (not (has gold_coin))
                       (has gold_bar)
                       (acquaintance good)
                   )
    )

    (:action thieve
     :parameters   ()
     :precondition (and (at town))
     :effect       (and
                       (status convicted)
                       (has gold_coin)
                   )
    )

    (:action buy_indulgence
     :parameters   ()
     :precondition (and
                       (at town)
                       (status convicted)
                       (has gold_nugget)
                   )
     :effect       (and
                       (not (has gold_nugget))
                       (not (status convicted))
                   )
    )

    (:action serve_public
     :parameters   ()
     :precondition (and
                       (at town)
                       (status convicted)
                   )
     :effect       (and
                       (not (status convicted))
                       ; become tipsy --> not sober or drunk
                       (not (intoxication sober))
                       (not (intoxication drunk))
                       (intoxication tipsy)
                   )
    )

    ; academy actions --------------------------------------------------------------------------------------------------
    (:action study
     :parameters   ()
     :precondition (and
                       (at academy)
                       (not (status convicted))
                       (has gold_coin)
                   )
     :effect       (and
                       (not (has gold_coin))
                       (status captain)
                  )
    )

    (:action promoted_to_admiral
     :parameters   ()
     :precondition (and
                       (at academy)
                       (status pirate_slayer)
                       (status captain)
                       (intoxication sober)
                       (not (intoxication tipsy))
                       (not (intoxication drunk))
                   )
     :effect       (and (goal admiral))
    )

    ; sea actions ------------------------------------------------------------------------------------------------------
    (:action ambushed
     :parameters   ()
     :precondition (and
                       (at sea)
                       (not (status tough))
                   )
     :effect       (and
                       ; lose all gold & vessels
                       (not (has gold_nugget))
                       (not (has gold_coin))
                       (not (has gold_bar))
                       (not (has frigate))
                       (not (has caravel))
                       ; life boat
                       (has boat)
                       (status tough)
                   )
    )

    (:action join_pirates
     :parameters   ()
     :precondition (and
                       (at sea)
                       (acquaintance dubious)
                   )
     :effect       (and
                       ; become tipsy --> not sober or drunk
                       (not (intoxication sober))
                       (not (intoxication drunk))
                       (intoxication tipsy)
                       ; become a pirate
                       (status pirate)
                   )
    )

    (:action defeat_pirates
     :parameters   ()
     :precondition (and
                       (at sea)
                       (status tough)
                       (has caravel)
                   )
     :effect       (and
                       ; gain booty
                       (has gold_nugget)
                       (has gold_coin)
                       (has gold_bar)
                       (has boat)
                       (has frigate)
                       (has caravel)
                       ; become a pirate slayer
                       (status pirate_slayer)
                   )
    )

    (:action hunt_for_pearls
     :parameters   ()
     :precondition (and (at sea))
     :effect       (and (has pearl))
    )

    ; lighthouse actions -----------------------------------------------------------------------------------------------
    (:action woo
     :parameters   ()
     :precondition (and
                       (at lighthouse)
                       (or
                          (status pirate_slayer)
                          (status bear_wrestler)
                          (status captain)
                       )
                   )
      :effect      (and (status wooed))
    )


    ; island actions ---------------------------------------------------------------------------------------------------
    (:action collect_coconuts
     :parameters   ()
     :precondition (and (at island))
     :effect       (and (has coconut))
    )

    (:action find_treasure
     :parameters   ()
     :precondition (and
                       (at island)
                       (has treasure_map)
                   )
     :effect       (and (has coke))
    )

    (:action marry
     :parameters   ()
     :precondition (and
                       (at island)
                       (not (intoxication drunk))
                       (not (intoxication alcoholic))
                       (has ring)
                       (has flowers)

                       (acquaintance good)
                       (not (status convicted))
                       (status wooed)
                   )
        :effect    (and (goal married))
    )
    ; universal actions ------------------------------------------------------------------------------------------------
    (:action craft_ring
     :parameters   ()
     :precondition (and
                       (has gold_bar)
                       (has pearl)
                   )
     :effect       (and
                       (not (has gold_bar))
                       (not (has pearl))
                       (has ring)
                   )
    )

    (:action become_addicted_to_coke
     :parameters   ()
     :precondition (and
                       (has coke)
                       (has frigate)
                       (has gold_bar)
                       (intoxication alcoholic)
                       (acquaintance smugglers)
                   )
     :effect       (and (goal coke_addict))
    )

    (:action goal_achieved
     :parameters   ()
     :precondition (or
                      (goal married)
                      (goal coke)
                      (goal admiral)
                   )
     :effect       (and (goal achieved))
    )
)