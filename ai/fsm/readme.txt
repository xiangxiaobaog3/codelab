Miner:

dig for gold
  thirsty + 1
  fatigue + 1
engouch gold
  deposit gold
  if thirsty
     quenchThirst
  if fatigue
     sendMsg(HiHoneyImHome)
     goHomeAndTilRest
     if receiveMsg(cookStew):
         EatStew()
         sendMsg('eatDone')
         goToSleep()

wife:
  vistBathroom
  doHouseWork

  if receive(HiHoneyImHome):
      cookStew
        when cookStew done
            sendMsg(StewReady)
  if receive('eatDone')
      doHouseWork()


dispatch(E1, E2, msg, extra) -> E1 sendMsg to E2
E2 as receiver pass msg to E2's stateMachine
stateMachine -> globalState.on_message
             -> currentState.on_message
