def unnest(string, ldelim='(', rdelim=')'):
    lindex = string.find(ldelim)
    rindex, count = 0, 1

    # Count matching pairs of delimiters until balanced
    while count > 0:
        try:
            char = string[lindex+1:][rindex]
        except:
            pass
        if char == ldelim:
            count += 1
        elif char == rdelim:
            count -= 1
        else:
            pass
        rindex += 1
    rindex += lindex
    command = string[lindex+1:rindex]
    return command, lindex+1, rindex


def mapinds(string):
    count = 0
    inds = []
    for char in string:
        if char == '(':
            inds.append(count)
        elif char == ')':
            inds.append(count-1)
        else:
            inds.append(count)
            count += 1
    return inds
