FACTION_DECK_GUID=Global.getVar('FACTION_DECK_GUID')
function onSetupCards()
  publicDeckUrl="https://de.arkhamdb.com/api/public/decklist/"

  num = 39137
  print("Requesting deck ID " .. num)
  WebRequest.get(publicDeckUrl .. "39137", self, 'deckReadCallback')
end

function deckReadCallback(req)
  -- Result check..
  if req.is_done and not req.is_error
  then
    if string.find(req.text, "<!DOCTYPE html>")
    then
      broadcastToAll("Cannot find "..deckID.." on ArkhamDB", {0.5,0.5,0.5})
      return
    end
    JsonDeckRes = JSON.decode(req.text)
  else
    print (req.error)
    return
  end
  if (JsonDeckRes == nil)
  then
    broadcastToAll("Problems parsing the JSON", {0.5,0.5,0.5})
    return
  else
    print("Found cards for: "..JsonDeckRes.name)
  end

    -- Count number of cards in decklist
  cards = {}
  numSlots=0
  for cardid,number in pairs(JsonDeckRes.slots)
  do
    for a=1,number,1 do
      cards[#cards+1] = cardid
    end
  end
  print("There are " .. #cards .. " in this deck")
  searchCards(cards)
end

function searchCards(cards)
  local factionDeck = getObjectFromGUID(FACTION_DECK_GUID)

  for unused,card in pairs(cards) do
      cloneParams={}
      cloneParams.position = {0,0,50}
      tmpDeck = factionDeck.clone(cloneParams)
      allCards = tmpDeck.getObjects()
      found=false
      for k,v in pairs(allCards) do
        if (not found) then
            if (v.description == card)
            then
                local takeParams = {position={10,0,20}, callback='cardTaken', callback_owner=self, index=v.index, smooth = false, params={card,1,false,v.guid}}
                tmpDeck.takeObject(takeParams)
                --print('Took card with ID '.. card .. " from supply")
                found = true
            end
        end
      end

      tmpDeck.destruct()
  end
  print("Deck loaded sucessfully")
  --factionDeck.randomize()

end

function cardTaken(card, params)
  -- Check destination deck (permanent?)
  local destPos ={0,2,0}

  card.setPosition(destPos)
end