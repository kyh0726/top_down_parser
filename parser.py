import re
import sys

# 전역 변수 선언
next_token = None
token_string = ""
symbol_table = {}  # 변수 저장소 (변수 이름: 값)
warning_messages = []  # 여러 경고 메시지를 저장하는 리스트
error_messages = [] # 여러 에러 메시지를 저장하는 리스트

# 토큰 유형 정의
ID = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
CONST = re.compile(r'\d+')
ADD_OP = re.compile(r'\+|-')
MULT_OP = re.compile(r'\*|/')
ASSIGN_OP = re.compile(r':=')
SEMI_COLON = re.compile(r';')
LEFT_PAREN = re.compile(r'\(')
RIGHT_PAREN = re.compile(r'\)')

# 입력 문자열 토큰화
tokens = []
original_sliced_tokens = []
modified_sliced_tokens = []
error_type = []
index = 0
previous_index = 0
# lexical() 함수 - 정의되지 않은 토큰 무시
def lexical():
    global next_token, token_string, index, warning_messages, original_sliced_tokens
    while index < len(tokens):
        token_string = tokens[index]
        # print(f'전체 토큰 리스트 : {tokens}, 전체 토큰 수 : {len(tokens)} 현재 토큰 값 : {tokens[index]}, 인덱스 : {index}')
        original_sliced_tokens.append(token_string)
        if ID.fullmatch(token_string):
            next_token = "ID"
        elif CONST.fullmatch(token_string):
            next_token = "CONST"
        elif ADD_OP.fullmatch(token_string):
            next_token = "ADD_OP"
        elif MULT_OP.fullmatch(token_string):
            next_token = "MULT_OP"
        elif ASSIGN_OP.fullmatch(token_string):
            next_token = "ASSIGN_OP"
        elif SEMI_COLON.fullmatch(token_string):
            next_token = "SEMI_COLON"
        elif LEFT_PAREN.fullmatch(token_string):
            next_token = "LEFT_PAREN"
        elif RIGHT_PAREN.fullmatch(token_string):
            next_token = "RIGHT_PAREN"
        else:
            handle_warning("UNDEFINED_TOKEN")
            continue
        index += 1
        break
    else:
        next_token = None

# 토큰화 함수
def tokenize(input_string):
    global tokens, index, warning_messages
    tokens = input_string.split()
    index = 0
    warning_messages = []
    lexical()  # 첫 번째 토큰 설정
    
# 토큰 개수 세기
def count_tokens(target_tokens):
    id_count = sum(1 for token in target_tokens if ID.fullmatch(token))
    const_count = sum(1 for token in target_tokens if CONST.fullmatch(token))
    op_count = sum(1 for token in target_tokens if ADD_OP.fullmatch(token) or MULT_OP.fullmatch(token))
    return id_count, const_count, op_count



# 파싱 함수 정의
def parse_program():
    if index < len(tokens):
        parse_statements()
        

def parse_statements():
    global tokens
    parse_statement()
    

    def find_semi_colon():        
        global tokens
        if next_token == "SEMI_COLON":
            print_result()
        elif next_token == None:
            pass
        else:
            handle_warning("MISSING_SEMI_COLON")
            find_semi_colon()
    if next_token == None:
        print_result()
        print("result ==> ", format_symbol_table())
    else:
        find_semi_colon()
        parse_statements() # statement semicolon statement semicolon ... 이런 형태로 나올 수 있으니 재귀적으로 수행



def parse_statement():
    global index
    if next_token == "ID":
        variable = token_string
        lexical()
        if next_token == "ASSIGN_OP":
            lexical()
            value = parse_expression()
            symbol_table[variable] = value  # 변수에 값 저장
        else:
            handle_warning("ADD_ASSIGN_OP")
            value = parse_expression()
            symbol_table[variable] = value  # 변수에 값 저장
    elif next_token == "SEMI_COLON":
        pass
    elif next_token == None:
        pass
    else:
        handle_warning("MISSING_OPERAND")
        parse_statement() # 다음 토큰에는 ID값이 먼저 나오는 지 확인!
        

# 생성자 expression
def parse_expression():
    global index
    # 피생성자 term 부분
    value = parse_term()

    # 피생성자 term_tail 부분
    while next_token == "ADD_OP":
        op = token_string
        lexical()
        term_value = parse_term()
        if value == "Unknown" or term_value == "Unknown":
            value = "Unknown"
        else:
            value = value + term_value if op == '+' else value - term_value
    
    return value

def parse_term():
    value = parse_factor()
    # factor_tail 생성자 부분
    while next_token == "MULT_OP":
        op = token_string
        lexical()
        factor_value = parse_factor()
        if value == "Unknown" or factor_value == "Unknown":
            value = "Unknown"
        else:
            if op == "*":
                value = value * factor_value
            else:
                if factor_value == 0: # 0으로 나눈 경우
                    value = "Unknown"
                    handle_error("DIVISION_BY_ZERO_ERROR")
                else:
                    value = value // factor_value

    return value

def parse_factor():
    global error_type
    if next_token == "LEFT_PAREN":
        lexical()
        value = parse_expression()
        if next_token == "RIGHT_PAREN":
            lexical()
        else:
            handle_warning("ADD_RIGHT_PAREN")
    elif next_token == "ID":
        value = symbol_table.get(token_string, "Undefined")
        if value == "Undefined":
            handle_error("UNDEFINED_ID_ERROR")
            value = "Unknown"
        lexical()
    elif next_token == "CONST":
        value = int(token_string)
        lexical()
    elif next_token == "SEMI_COLON" or next_token == None:
        handle_error("INSOLUBLE_ERROR")# '(' 'ID' 'CONST' 세 값 중에 하나도 안나왔는데 문장이 끝났다거나, 그 뒤에 토큰이 없는 경우는 치명적인 오류로 간주한다.
        value = "Unknown"
        return value
    else:
        handle_warning("MISSING_OPERAND")
        return parse_factor() # 만약 '(' 'ID' 'CONST' 세 값 중에 안나올 경우 handle_warning 과정을 거친 후에 재귀적으로 parse_factor 수행
    return value


def handle_warning(warning_type):
    global next_token, original_sliced_tokens, index, warning_messages
    match warning_type:
        case "ADD_RIGHT_PAREN": # ')' 괄호 넣어주는 방식으로 처리
            warning_messages.append(f"(Warning) ')' 괄호가 생략되었습니다. 토큰 '{tokens[index - 1]}' 의 오른쪽 옆에 ')'을 추가합니다.")
            tokens.insert(index, ')')
            index += 1
            lexical()

        case "MISSING_OPERAND": # '다음 토큰 값들을 계속 빼주면서 ID나 CONST 값을 찾아주는 방식으로 처리'
            warning_messages.append(f"(Warning) 적절하지 못한 토큰 '{tokens[index-1]}'을(를) 삭제했습니다.")
            tokens.pop(index - 1)
            index -= 1
            lexical() 
        case "ADD_ASSIGN_OP": # ':='을 넣어주는 방식으로 처리
            warning_messages.append(f"(Warning) ':=' 할당 연산자가 생략되었습니다. 토큰 '{tokens[index - 2]}' 의 오른쪽 옆에 ':='을 추가합니다.")
            tokens.insert(index - 1, ':=')
            original_sliced_tokens.pop()
            lexical()
        case "MISSING_SEMI_COLON": # '다음 토큰 값들을 계속 빼주면서 ID나 CONST 값을 찾아주는 방식으로 처리'
            warning_messages.append(f"(Warning) 적절하지 못한 토큰 '{tokens[index-1]}'을(를) 삭제했습니다.")
            tokens.pop(index - 1)
            index -= 1
            lexical() 
        case "UNDEFINED_TOKEN":
            warning_messages.append(f"(Warning) 정의되지 않은 토큰 '{token_string}'을(를) 삭제합니다.")
            tokens.pop(index)

def handle_error(param_error_type):
    match param_error_type:
        case "UNDEFINED_ID_ERROR":
            error_messages.append(f"(Error) 정의되지 않은 변수({token_string})가 참조됨")
            error_type.append("UNDEFINED_ID_ERROR")
            symbol_table[token_string] = "Unknown"
        case "INSOLUBLE_ERROR":
            error_messages.append(f"(Error) 추가나 삭제를 통해 오류를 수정할 수 없음")
            error_type.append("INSOLUBLE_ERROR")
        case "DIVISION_BY_ZERO_ERROR":
            error_messages.append(f"(Error) 0으로 나누는 에러가 발생했습니다. 해당 값은 Unknown으로 할당됩니다.")
            error_type.append("DIVISION_BY_ZERO_ERROR")
# 사용 예시
def print_result():
    # 세미콜론을 만날 때마다 토큰 개수를 출력


    global tokens, modified_sliced_tokens, original_sliced_tokens, previous_index, index, error_type
    
    modified_sliced_tokens = tokens[previous_index: index]
    previous_index = index
    modified_input = " ".join(modified_sliced_tokens)
    original_input = " ".join(original_sliced_tokens)

    def print_error_and_warning():
        for message in warning_messages:
            print(message)
        for message in error_messages:
            print(message)
        
    def print_error():
        for message in error_messages:
            print(message)

    def print_warning():
        for message in warning_messages:
            print(message)

    def print_no_error_and_warning():
        print("(OK)")



    if error_messages:

        if ("INSOLUBLE_ERROR" in error_type): # 문법을 수정을 통해 해결할 수 없는 경우
            print(f"원래 input 값 : {original_input}")
            id_count, const_count, op_count = count_tokens(original_sliced_tokens)
            print(f"ID: {id_count}; CONST: {const_count}; OPERATOR: {op_count};")
            print_error()

        elif warning_messages: # ZERO_DIVISION이나 UNDEFINED인 에러에는 걸리는데, 문법은 수정을 통해 해결된 경우
            print(f"수정된 input 값 : {modified_input}")
            id_count, const_count, op_count = count_tokens(modified_sliced_tokens)
            print(f"ID: {id_count}; CONST: {const_count}; OPERATOR: {op_count};")
            print_error_and_warning()
        
        else: # ZERO_DIVISION이나 UNDEFINED인 에러에만 걸리고, 수정은 이뤄지지 않은 경우
            print(f"원래 input 값 : {original_input}")
            id_count, const_count, op_count = count_tokens(modified_sliced_tokens)
            print(f"ID: {id_count}; CONST: {const_count}; OPERATOR: {op_count};")
            print_error_and_warning()
                    

    elif warning_messages: # 문법을 수정을 통해 해결할 수 있고 오류는 발생하지 않는 경우
        print(f"수정된 input 값 : {modified_input}")
        id_count, const_count, op_count = count_tokens(modified_sliced_tokens)
        print(f"ID: {id_count}; CONST: {const_count}; OPERATOR: {op_count};")
        print_warning()

    else: # 아무 문제 없음
        print(f"원래 input 값 : {original_input}")
        id_count, const_count, op_count = count_tokens(original_sliced_tokens)
        print(f"ID: {id_count}; CONST: {const_count}; OPERATOR: {op_count};")
        print_no_error_and_warning()

    print()
    original_sliced_tokens.clear()
    warning_messages.clear()
    error_messages.clear()
    error_type.clear()
    lexical()

# 심볼 테이블 형식화 함수
def format_symbol_table():
    return "; ".join(f"{var}: {val}" for var, val in symbol_table.items())

# main 함수
def main():
    if len(sys.argv) < 2:
        print("다음과 같은 방식으로 프로그램을 실행해주세요 : python parser.py input.txt")
        return

    file_name = sys.argv[1]
    try:
        with open(file_name, "r") as input_file:
            input_string = input_file.read()
            tokenize(input_string.strip())
            parse_program()

    except FileNotFoundError:
        print(f"파일 '{file_name}'을(를) 찾을 수 없습니다.")

# 프로그램 실행
if __name__ == "__main__":
    main()