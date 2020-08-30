Option Explicit
' Get the slot corresponding to the Margin time not after,
'     if the margin is too early, return the slot compatible with the earliest time (schedule)
' the slot could be the last one because large Margin

Function AU_NPMF_GetEarlierAvailableSlots(ByRef lSlotUsed() As Integer, lSlot_nb As Integer, _
                lCurrentSlot) As Integer
    
    Dim lTargetSlot As Integer
    Dim li As Integer
    
    ' find a slot corresponding to the Margin value to put the flight
    lTargetSlot = -1
    
    ' the slot could be the last one because large Margin
    ' but no problem
    
    ' the flight could have a target time = to the schedule and if no anticipation then bad return value !!!!
    For li = lCurrentSlot To 0 Step -1
    
        ' first store the latest time compatible with the flight schedule
        If lSlotUsed(li) = -1 Then
            lTargetSlot = li
            li = 0
        End If
    Next li
    
    AU_NPMF_GetEarlierAvailableSlots = lTargetSlot
    
End Function




' Get the slot corresponding to the Margin time not after,
'     if the margin is too early, return the slot compatible with the earliest time (schedule)
' the slot could be the last one because large Margin

Function AU_NPMF_GetTargetSlots(ByRef lSlotTime() As Date, lSlot_nb As Integer, _
                lMarginTime, lEarliestTime) As Integer
    
    Dim lTargetSlot As Integer
    Dim lTimeSlot As Integer
    Dim li As Integer
    
    ' find a slot corresponding to the Margin value to put the flight
    lTargetSlot = -1
    lTimeSlot = -1
    
    ' the slot could be the last one because large Margin
    ' but no problem
    
    ' the flight could have a target time = to the schedule and if no anticipation then bad return value !!!!
    For li = lSlot_nb - 1 To 0 Step -1
    
        ' first store the latest time compatible with the flight schedule
        If lSlotTime(li) >= lEarliestTime Then
            lTimeSlot = li
        End If
        
        If lSlotTime(li) <= lMarginTime Then
            ' if found a slot test also if compatible with shedule, otherwise take the last compatible
            If lSlotTime(li) >= lEarliestTime Then
                lTargetSlot = li
                li = 0
            End If
        End If
    Next li
    
    If lTargetSlot > -1 Then
        AU_NPMF_GetTargetSlots = lTargetSlot
    ElseIf lTimeSlot > -1 Then
        AU_NPMF_GetTargetSlots = lTimeSlot
    Else
        AU_NPMF_GetTargetSlots = -1
    End If
    
End Function


' Get the slot corresponding to the Margin time not after,
'     if the margin is too early, return the slot compatible with the earliest time (schedule)
' the slot could be the last one because large Margin

Function AU_NPMF_GetLaterAvailableSlots(ByRef lSlotTime() As Date, ByRef lSlotUsed() As Integer, lSlot_nb As Integer, _
                lCurrentSlot, lEarliestTime) As Integer
    
    Dim lTargetSlot As Integer
    Dim li As Integer
    
    ' find a slot corresponding to the Margin value to put the flight
    lTargetSlot = -1
    
    ' the flight could have a target time = to the schedule and if no anticipation then bad return value !!!!
    ' test also thecurrent one just to be sure
    For li = lCurrentSlot To lSlot_nb - 1
        If lSlotUsed(li) = -1 Then
            ' take the first with a compatible time with schedule
            If lSlotTime(li) >= lEarliestTime Then
                lTargetSlot = li
                li = lSlot_nb
            End If
        End If
    Next li
    
    AU_NPMF_GetLaterAvailableSlots = lTargetSlot
    
End Function



' Get the slot corresponding to the Margin time not after,
'     if the margin is too early, return the slot compatible with the earliest time (schedule)
' the slot could be the last one because large Margin

Function AU_NPMF_GetIxOfEarlierFlightCanMove(lAll_AUFlights As CL_AllFlights, _
                ByRef lSlotTime() As Date, ByRef lSlotUsed() As Integer, lSlot_nb As Integer, _
                lCurrentSlot As Integer, lCurrentFlight As Integer) As Integer
    
    Dim lEarlierAvailableSlot As Integer
    Dim llEarlierAvailableSlotTime As Date
    Dim lTargetSlot As Integer
    
    Dim lEarliestFlightSlot As Integer
    Dim li As Integer
    Dim ltime As Date
    
    ' find a slot corresponding to the Margin value to put the flight
    
    If lSlotUsed(lCurrentSlot) = -1 Then
        If AU_NPM_ManageMarginPrioFlights_IsFlightScheduleCompatible(lAll_AUFlights, lSlotTime(lCurrentSlot), lCurrentFlight) = True Then
            ' this fligh is compatible
            lTargetSlot = lCurrentSlot
        Else
            ' no solution because current and earlier slot not compatible with schedule
            lTargetSlot = -1
        End If
    Else
        ' find an empty flot
        lEarlierAvailableSlot = AU_NPMF_GetEarlierAvailableSlots(lSlotUsed(), lSlot_nb, lCurrentSlot)
        If lEarlierAvailableSlot < 0 Then
            ' no earlier slot available
            lTargetSlot = -1
        Else
            lTargetSlot = lEarlierAvailableSlot
        End If
    End If
    AU_NPMF_GetIxOfEarlierFlightCanMove = lTargetSlot
    
End Function





'------------------------------------------------------------------------------ AU_NPMF_GetFirstCompatibleSlot
' Get the first slot corresponding to the schedule time ,
Function AU_NPMF_GetFirstCompatibleSlot(lAll_AUFlights As CL_AllFlights, _
                ByRef lSlotTime() As Date, ByRef lSlotUsed() As Integer, lSlot_nb As Integer, _
                lCurrentFlight As Integer) As Integer
    
    Dim lEarliestTime As Date
    Dim lTargetSlot As Integer
    Dim li As Integer
    
    ' find a slot corresponding to the Margin value to put the flight
    
        ' find an empty flot
    lEarliestTime = lAll_AUFlights.GetRefBlockTime(lCurrentFlight) _
                                                    - GHspt_FlightEarlyDeparture_forDate
                                                    

    lTargetSlot = -1
    For li = 0 To lSlot_nb - 1
        
        If lSlotTime(li) >= lEarliestTime Then
            ' this slot is compatible
            lTargetSlot = li
            li = lSlot_nb
        End If
    Next li
    
    AU_NPMF_GetFirstCompatibleSlot = lTargetSlot
    
End Function

'------------------------------------------------------------ AU_NPM_ManageMarginPrioFlights_AssignPrioOnlyFlight
' Assign priority only flights in the remaining slot

Function AU_NPM_ManageMarginPrioFlights_IsFlightScheduleCompatible(lAll_AUFlights As CL_AllFlights, _
            lSlotTime As Date, lFlightIx As Integer) As Boolean

    Dim lEarliestTime As Date
    Dim lReturn As Boolean
    
    ' the slot is available : end of the recurcive function
    lEarliestTime = lAll_AUFlights.GetRefBlockTime(lFlightIx) _
                                                    - GHspt_FlightEarlyDeparture_forDate
    ' test if flight can be move
    If lSlotTime >= lEarliestTime Then
        lReturn = True
    Else
        lReturn = False
    End If
    
    AU_NPM_ManageMarginPrioFlights_IsFlightScheduleCompatible = lReturn
End Function





'---------------------------------------- AU_NPM_ManageMarginPrioFlights_UpdateFDATimeFromSlots
Sub AU_NPM_ManageMarginPrioFlights_UpdateFDATimeFromSlots(lAll_AUFlights As CL_AllFlights, _
            ByRef lSlotTime() As Date, ByRef lSlotList() As Integer, lSlot_nb As Integer)
            
    Dim lFl As Integer
    Dim lFlIx As Integer
    Dim ltime As Date
    
    ' ---------- manage the baseline flights on schedule
    ' loop on baseline flights
    For lFl = 0 To lSlot_nb - 1
        lFlIx = lSlotList(lFl)
        If lFlIx > -1 Then
            ltime = lSlotTime(lFl)
            Call lAll_AUFlights.SetFDATime(lFlIx, ltime)
        End If
    Next lFl

End Sub




