def validar_rut(rut:str) -> bool:
    s = rut.replace(".", "").upper().strip()
    if len(s)< 2:
        return False
    body, dv= s[:-1], s[-1]
    try:
        total=0
        mul= 2
        for digit in reversed (body):
            total+=int(digit)*mul
            mul+=1
            if mul== 8:
                mul= 2
    except ValueError:
        return False
    rest= 11 -  (total % 11)
    if rest == 11:
        expected = "0"
    elif rest ==10:
        expected ="K"
    else:
        expected=str(rest)
    return dv== expected