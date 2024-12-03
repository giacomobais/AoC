
DIGITS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
CHAR_DIGITS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
CHAR_TO_DIGIT = dict(zip(CHAR_DIGITS, DIGITS))

def extract_digits(line):
    for char in line:
        if char in DIGITS:
            a = char
            break
    for char in reversed(line):
        if char in DIGITS:
            b = char
            break
    return int(a+b)

def extract_real_digits(line):
    first_digit = None
    second_digit = None
    hypothesis = ''
    for char in line:
        if char in DIGITS:
            if first_digit is None:
                first_digit = char
            second_digit = char
        hypothesis += char
        hypothesis_len = len(hypothesis)
        match = False
        for char_digit in CHAR_DIGITS:
            test = char_digit[:hypothesis_len]
            if hypothesis == test and hypothesis in CHAR_TO_DIGIT:
                if first_digit is None:
                    first_digit = CHAR_TO_DIGIT[hypothesis]
                second_digit = CHAR_TO_DIGIT[hypothesis]
                break
            if hypothesis == test:
                match = True
                break
        if match is False:
            if first_digit is None:
                hypothesis = hypothesis[1:]
            else:
                hypothesis = hypothesis[-1]
    return int(first_digit + second_digit)

if __name__ == '__main__':
    file_path = 'input.txt'
    with open(file_path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip('\n') for line in lines]
    sum = 0
    for line in lines:
        calibration = extract_digits(line)
        sum += calibration
    print(sum)
    
    real_sum = 0
    for i, line in enumerate(lines):
        calibration = extract_real_digits(line)
        real_sum += calibration
    print(real_sum)