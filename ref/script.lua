--[[ Lua code. See documentation: http://berserk-games.com/knowledgebase/scripting/ --]]

--[[ The onLoad event is called after the game save finishes loading. --]]
function onLoad()
  --[[ print('onLoad!') --]]
  init()
  -- Setup...
  publicDeckURL="https://arkhamdb.com/api/public/decklist/"
  privateDeckURL="https://arkhamdb.com/api/public/deck/"
  cardURL="https://arkhamdb.com/api/public/card/"
  subnameCards={{name="The Necronomicon",xp=0},{name="Archaic Glyphs",xp=3},{name="Strange Solution",xp=4},{name="Relic of Ages",xp=0}, {name="Ancient Stone",xp=4}}
  extraPermanents={["Duke"]=true,["Sophie"]=true}
  multiClassCards={{name=".45 Thompson",xp=3},{name="Scroll of Secrets",xp=3},{name="Tennessee Sour Mash",xp=3},{name="Enchanted Blade",xp=3},{name="Grisly Totem",xp=3}}
  bondedCards={{name="Hallowed Mirror",bondedName="Soothing Melody",bondedCode=05314,copies=3},{name="Occult Lexicon",bondedName="Blood-Rite",bondedCode=05317,copies=3}}
  privateDeck = true
  permanents = true

  local tileGUID = '928c8e'
  tile = getObjectFromGUID(tileGUID)
  makeText()
  makeButton()
  makeCheckboxPP()
  makeCheckboxPerms()
end

function spawnZone()
  -- Clean up scripting zone
  if pcZone
  then
    pcZone.destruct()
  end
  deckPos = LocalPos(self,{-1.85,1.5,1.8})
  permPos = LocalPos(self,{-4.63,1.5,1.8})
  local pcZonePos = LocalPos(self,{4.75, 2.6 , 1.8})
  zoneSpawn = {position = pcZonePos
       , scale = { 2.57, 5.1, 3.47 }
       , type = 'ScriptingTrigger'
--       , callback = 'zoneCallback'
       , callback_owner = self
       , rotation = self.getRotation() }
  pcZone = spawnObject(zoneSpawn)
  for i=1,1 do
       coroutine.yield(0)
   end

   local objectsInZone = pcZone.getObjects()
   for i,v in pairs(objectsInZone) do
     if v.tag == 'Deck' then
       playerCardDeck = v
     end
   end

   -- Get deck from ArkhamDB..
   local deckURL
   if privateDeck then deckURL = privateDeckURL
   else deckURL = publicDeckURL
   end

   WebRequest.get(deckURL .. deckID, self, 'deckReadCallback')

   return 1
end

function init()
  cardList = {}
  doneSlots = 0
  playerCardDeck = {}
  totalCards = 0
end

function buttonClicked()
  -- Reset
  init()
  -- Spawn scripting zone
  startLuaCoroutine(self, "spawnZone")
end

function checkboxPPClicked()
  buttons = tile.getButtons()
  for k,v in pairs(buttons) do
    if (v.label == "Private deck") then
      local button_parameters = {}
      button_parameters.label = "Public deck"
      button_parameters.index = v.index
      tile.editButton(button_parameters)
      privateDeck = false
    else
      if (v.label == "Public deck") then
        local button_parameters = {}
        button_parameters.label = "Private deck"
        button_parameters.index = v.index
        tile.editButton(button_parameters)
        privateDeck = true
      end
    end
  end
end

function checkboxPermsClicked()
  buttons = tile.getButtons()
  for k,v in pairs(buttons) do
    if (v.label == "Permanents") then
      local button_parameters = {}
      button_parameters.label = "No permanents"
      button_parameters.index = v.index
      tile.editButton(button_parameters)
      permanents = false
    else
      if (v.label == "No permanents") then
        local button_parameters = {}
        button_parameters.label = "Permanents"
        button_parameters.index = v.index
        tile.editButton(button_parameters)
        permanents = true
      end
    end
  end
end

function deckReadCallback(req)
  -- Result check..
  if req.is_done and not req.is_error
  then
    if string.find(req.text, "<!DOCTYPE html>")
    then
      broadcastToAll("Private deck "..deckID.." is not shared", {0.5,0.5,0.5})
      return
    end
    JsonDeckRes = JSON.decode(req.text)
  else
    print (req.error)
    return
  end
  if (JsonDeckRes == nil)
  then
    broadcastToAll("Deck not found!", {0.5,0.5,0.5})
    return
  else
    print("Found decklist: "..JsonDeckRes.name)
  end
  -- Count number of cards in decklist
  numSlots=0
  for cardid,number in
  pairs(JsonDeckRes.slots)
  do
    numSlots = numSlots + 1
  end

  -- Save card id, number in table and request card info from ArkhamDB
  for cardID,number in pairs(JsonDeckRes.slots)
  do
    local row = {}
    row.cardName = ""
    row.cardCount = number
    cardList[cardID] = row
    WebRequest.get(cardURL .. cardID, self, 'cardReadCallback')
    totalCards = totalCards + number
  end
end

function cardReadCallback(req)
  -- Result check..
  if req.is_done and not req.is_error
  then
    -- Find unicode before using JSON.decode since it doesnt handle hex UTF-16
    local tmpText = string.gsub(req.text,"\\u(%w%w%w%w)", convertHexToDec)
    JsonCardRes = JSON.decode(tmpText)
  else
    print(req.error)
    return
  end

  -- Update card name in table
  if(JsonCardRes.xp == nil or JsonCardRes.xp == 0)
  then
    cardList[JsonCardRes.code].cardName = JsonCardRes.real_name
  else
    cardList[JsonCardRes.code].cardName = JsonCardRes.real_name .. " (" .. JsonCardRes.xp .. ")"
  end

  -- Check for subname
  for k,v in pairs(subnameCards) do
    if (v.name == JsonCardRes.real_name and (v.xp == JsonCardRes.xp or JsonCardRes.xp == nil))
    then
      cardList[JsonCardRes.code].subName = JsonCardRes.subname
    end
  end

  -- Check for multiclass
  for k,v in pairs(multiClassCards) do
    if (v.name == JsonCardRes.real_name and (v.xp == JsonCardRes.xp or JsonCardRes.xp == nil))
    then
      cardList[JsonCardRes.code].subName = JsonCardRes.faction_name
    end
  end

  -- Check if card is permanent (if separation is selected)
  if permanents then
    if (JsonCardRes.permanent == true or extraPermanents[JsonCardRes.real_name]) then
      cardList[JsonCardRes.code].permanent = true
    else
      cardList[JsonCardRes.code].permanent = false
    end
  else
    cardList[JsonCardRes.code].permanent = false
  end

  -- Check for bonded
  for k,v in pairs(bondedCards) do
    if (v.name == JsonCardRes.real_name)
    then
      local row = {}
      row.cardName = v.bondedName
      row.cardCount = v.copies
      row.permanent = true
      cardList[v.bondedCode] = row
    end
  end

  -- Update number of processed slots, if complete, start building the deck
  doneSlots = doneSlots + 1
  if (doneSlots == numSlots)
  then
    createDeck()
  end
end

function createDeck()
  -- Create clone of playerCardDeck to use for drawing cards
  local cloneParams = {}
  cloneParams.position = {0,0,50}
  tmpDeck = playerCardDeck.clone(cloneParams)

  for k,v in pairs(cardList) do
    searchForCard(v.cardName, v.subName, v.cardCount, v.permanent)
  end

  tmpDeck.destruct()
end

function searchForCard(cardName, subName, cardCount, permanent)
  allCards = tmpDeck.getObjects()
  for k,v in pairs(allCards) do
    if (v.nickname == cardName)
    then
      if(subName == nil or v.description == subName)
      then
        local takeParams = {position={10,0,20}, callback='cardTaken', callback_owner=self, index=v.index, smooth = false, params={cardName,cardCount,permanent,v.guid}}
        tmpDeck.takeObject(takeParams)
        print('Added '.. cardCount .. ' of ' .. cardName)
        return
      end
    end
  end
  broadcastToAll("Card not found: "..cardName, {0.5,0.5,0.5})
end

function cardTaken(card, params)
  -- Check destination deck (permanent?)
  local destPos
  if (params[3] == true) then -- permanent card
    destPos = permPos
  else
    destPos = deckPos
  end

  if (card.getName() == params[1]) then
    for i=1,params[2]-1,1 do
      local cloneParams = {}
      cloneParams.position=destPos
      card.clone(cloneParams)
    end
    card.setPosition(destPos)
  else
    print('Wrong card: ' .. card.getName())
    tmpDeck.putObject(card)
  end
end

function makeText()
  -- Create textbox
  local input_parameters = {}
  input_parameters.input_function = "inputTyped"
  input_parameters.function_owner = self
  input_parameters.position = {-0.02,0.2,-0.56}
  input_parameters.width = 1620
  input_parameters.scale = {0.1,0.1,0.1}
  input_parameters.height = 600
  input_parameters.font_size = 500
  input_parameters.tooltip = "*** PLEASE USE PRIVATE DECKS IF YOUR DECK IS ONLY FOR TTS *** \n\nInput deck ID from ArkhamDB URL of your deck\n\nExample: For the URL 'https://arkhamdb.com/decklist/view/101/knowledge-overwhelming-solo-deck-1.0', you should input '101'"
  input_parameters.alignment = 3 -- (1 = Automatic, 2 = Left, 3 = Center, 4 = Right, 5 = Justified) –Optional
  input_parameters.value=""
  tile.createInput(input_parameters)
end

function makeButton()
  -- Create Button
  local button_parameters = {}
  button_parameters.click_function = "buttonClicked"
  button_parameters.function_owner = self
  button_parameters.position = {-0.26,0.1,0.37}
  button_parameters.width = 300
  button_parameters.height = 4
  button_parameters.tooltip = "Click to start building deck"
  tile.createButton(button_parameters)
end

function makeCheckboxPP()
  local checkbox_parameters = {}
  checkbox_parameters.click_function = "checkboxPPClicked"
  checkbox_parameters.function_owner = self
  checkbox_parameters.position = {-0.4,0.2,-0.6}
  checkbox_parameters.width = 1350
  checkbox_parameters.height = 300
  checkbox_parameters.tooltip = "Click to toggle Private/Public deck ID"
  checkbox_parameters.label = "Private deck"
  checkbox_parameters.font_size = 200
  checkbox_parameters.scale = {0.1,0.1,0.1}
  tile.createButton(checkbox_parameters)
end

function makeCheckboxPerms()
  local checkbox_parameters = {}
  checkbox_parameters.click_function = "checkboxPermsClicked"
  checkbox_parameters.function_owner = self
  checkbox_parameters.position = {-0.4,0.2,-0.5}
  checkbox_parameters.width = 1350
  checkbox_parameters.height = 300
  checkbox_parameters.tooltip = "Click to toggle separate permanents"
  checkbox_parameters.label = "Permanents"
  checkbox_parameters.font_size = 200
  checkbox_parameters.scale = {0.1,0.1,0.1}
  tile.createButton(checkbox_parameters)
end

-- Function to convert utf-16 hex to actual character since JSON.decode doesn't seem to handle utf-16 hex very well..
function convertHexToDec(a)
  return string.char(tonumber(a,16))
end
--------------
--------------
-- Start of Dzikakulka's positioning script


-- Return position "position" in "object"'s frame of reference
-- (most likely the only function you want to directly access)
function LocalPos(object, position)
    local rot = object.getRotation()
    local lPos = {position[1], position[2], position[3]}

    -- Z-X-Y extrinsic
    local zRot = RotMatrix('z', rot['z'])
    lPos = RotateVector(zRot, lPos)
    local xRot = RotMatrix('x', rot['x'])
    lPos = RotateVector(xRot, lPos)
    local yRot = RotMatrix('y', rot['y'])
    lPos = RotateVector(yRot, lPos)

    return Vect_Sum(lPos, object.getPosition())
end

-- Build rotation matrix
-- 1st table = 1st row, 2nd table = 2nd row etc
function RotMatrix(axis, angDeg)
    local ang = math.rad(angDeg)
    local cs = math.cos
    local sn = math.sin

    if axis == 'x' then
        return {
                    { 1,        0,             0 },
                    { 0,   cs(ang),   -1*sn(ang) },
                    { 0,   sn(ang),      cs(ang) }
               }
    elseif axis == 'y' then
        return {
                    {    cs(ang),   0,   sn(ang) },
                    {          0,   1,         0 },
                    { -1*sn(ang),   0,   cs(ang) }
               }
    elseif axis == 'z' then
        return {
                    { cs(ang),   -1*sn(ang),   0 },
                    { sn(ang),      cs(ang),   0 },
                    { 0,                  0,   1 }
               }
    end
end

-- Apply given rotation matrix on given vector
-- (multiply matrix and column vector)
function RotateVector(rotMat, vect)
    local out = {0, 0, 0}
    for i=1,3,1 do
        for j=1,3,1 do
            out[i] = out[i] + rotMat[i][j]*vect[j]
        end
    end
    return out
end

-- Sum of two vectors (of any size)
function Vect_Sum(vec1, vec2)
    local out = {}
    local k = 1
    while vec1[k] ~= nil and vec2[k] ~= nil do
        out[k] = vec1[k] + vec2[k]
        k = k+1
    end
    return out
end

-- End Dzikakulka's positioning script


function inputTyped(objectInputTyped, playerColorTyped, input_value, selected)
    deckID = input_value
end

--[[ The onUpdate event is called once per frame. --]]
function onUpdate ()
    --[[ print('onUpdate loop!') --]]
end
