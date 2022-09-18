FACTION_DECK_GUID=Global.getVar('FACTION_DECK_GUID')
CREATE_DECK_BOARD_GUID=Global.getVar('CREATE_DECK_BOARD_GUID')

function onLoad()
  board = getObjectFromGUID(CREATE_DECK_BOARD_GUID)
  makeText()
end

function makeText()
  -- Create textbox
  local input_parameters = {}
  input_parameters.input_function = "inputTyped"
  input_parameters.function_owner = self
  input_parameters.position = {4.0,1.0, -3.5}
  input_parameters.width = 1620
  input_parameters.scale = {1,1,1}
  input_parameters.height = 600
  input_parameters.font_size = 500
  input_parameters.tooltip = "Put in the ID of your public deck on ArkhamDB"
  input_parameters.alignment = 3 -- (1 = Automatic, 2 = Left, 3 = Center, 4 = Right, 5 = Justified) –Optional
  input_parameters.value=""
  board.createInput(input_parameters)
end

function inputTyped(objectInputTyped, playerColorTyped, input_value, selected)
    deckID = input_value
end

function onSetupCards()
  -- Bound to the onClick
  publicDeckUrl="https://de.arkhamdb.com/api/public/decklist/"
  if (deckID==nil) then
    print("Error! You need to enter the ID of your public deck in the input field first!")
    return
  end

  print("Requesting deck ID " .. deckID)
  WebRequest.get(publicDeckUrl .. deckID, self, 'deckReadCallback')
end

function deckReadCallback(req)
  -- Result check..
  if req.is_done and not req.is_error
  then
    if string.find(req.text, "<html>")
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
    broadcastToAll("Cannot find "..deckID.." on ArkhamDB", {0.5,0.5,0.5})
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