FACTION_DECK_GUID=Global.getVar('FACTION_DECK_GUID')
function onSetupCards()
  local factionDeck = getObjectFromGUID(FACTION_DECK_GUID)
  local cloneParams = {}
  cloneParams.position = {0,0,50}
  tmpDeck = factionDeck.clone(cloneParams)

  allCards = tmpDeck.getObjects()
  for k,v in pairs(allCards) do
    if (v.description == "01026")
    then
        local takeParams = {position={10,0,20}, callback='cardTaken', callback_owner=self, index=v.index, smooth = false, params={"01026",1,false,v.guid}}
        tmpDeck.takeObject(takeParams)
        print('Took 01026')
    end
  end
  --factionDeck.randomize()
  tmpDeck.destruct()
end

function cardTaken(card, params)
  -- Check destination deck (permanent?)
  local destPos ={0,2,0}

  card.setPosition(destPos)
end