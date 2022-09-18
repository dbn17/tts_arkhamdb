FACTION_DECK_GUID=Global.getVar('FACTION_DECK_GUID')
function onSetupCards()
  local factionDeck = getObjectFromGUID(FACTION_DECK_GUID)
  factionDeck.randomize()
end
