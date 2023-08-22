def solution(encrypted):
    decrypted = ""
    aCode = ord("a")
    zCode = ord("z")
    for c in encrypted:
        if(c.islower()) :
            offset = ord(c) - aCode
            reversed_code = zCode - offset
            decrypted += unichr(reversed_code)
        else: 
            decrypted += c
    
    return decrypted


print(solution("wrw blf hvv ozhg mrtsg'h vkrhlwv?"))
print(solution("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!"))

