Sub SaveToCSVs()
    Dim fDir
    Dim Workbooks
    Dim wS
    Dim fPath
    Dim sPath
    fPath = "C:\Users\jonei\PythonTest\data"
    sPath = "C:\Users\jonei\PythonTest\data"
    fDir = Dir(fPath)
    Do While (fDir <> "")
        If Right(fDir, 4) = ".xls" Or Right(fDir, 5) = ".xlsx" Then
            On Error Resume Next
            Set wB = Workbooks.Open(fPath & fDir)
            For Each wS In wB.Sheets
                wS.SaveAs sPath & wS.Name, xlCSV
            Next wS
            wB.Close False
            Set wB = Nothing
        End If
        fDir = Dir
        On Error GoTo 0
    Loop
End Sub