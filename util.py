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

def push(obj, l, depth):
    while depth:
        l = l[-1]
        depth -= 1
    if obj != "" and obj != ")":
        l.append(obj)
    elif obj == ")":
        l[-1] += ")"

def parse(s):
    groups = []
    depth = 0
    try:
        current_chars = ""
        head = True
        for char in s:
            if char == '.':
                push(current_chars, groups, depth)
                current_chars = ""
                push([], groups, depth)
                depth += 1
                head = False
            elif char == 'L':
                head = True
                current_chars += char
            elif char == '[':
                push(current_chars, groups, depth)
                current_chars = ""
                push([], groups, depth)
                depth += 1
            elif char == ']':
                push(current_chars, groups, depth)
                current_chars = ""
                depth -= 2
            elif char == '(':
                current_chars += char
            elif char == ')':
                push(")", groups, depth)
            elif not head:
                current_chars += char
                push(current_chars, groups, depth)
                current_chars = ""
            else:
                current_chars += char
        push(current_chars, groups, depth)
    except IndexError:
        raise ValueError('Parentheses mismatch')
    else:
        return groups

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
