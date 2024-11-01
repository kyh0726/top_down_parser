<warning의 경우>
    # handle_warning 함수에서 정의됨 
    -> ')'가 나오지 않을 때 ( 추가하면서 해결 )
    -> ':='가 나오지 않을 때 ( 추가하면서 해결 )
    -> 피연산자 나오지 않을 때 ( 다음 토큰 삭제하면서 해결이 되는 경우에는 )
    -> 세미콜론 관련해서는 warning으로 처리함 그냥 뒤에 세미콜론 나와야 하는데 나오지 않을 경우 뒤에 있는거 모두 다 삭제함

    # lexical 함수 보면 됨
    -> 만약 아예 정의되지 않은 토큰이 나올 경우 => 정의되지 않은 토큰 삭제합니다 

<error의 경우>
    # parse_factor 함수 쪽에서 next_token이 ;, None 인 경우 보면 됨
    -> 피연산자 나와야 하는데 ;이나 다음 토큰이 None 일 때, 즉 최대한 다음 토큰을 삭제하면서 피연산자 삭제해보려 하는데도 피연산자가 제대로 나오지 않으면

    # parse_factor() 의 함수에서 "undefined" 쪽 보면 됨
    -> 선언되지 않은 ID가 참조되었을 때 

<전체적인 flow>
    우선 과제 pdf에 있는 CFG를 유심히 보셈
    그러면 Non-Terminal 부분 Terminal 부분이 나뉘어서 보일거임
    논 터미널 (어떤 값을 생성할 수 있는 거, 예를 들면 pdf에서 statements, statement 등등)
    터미널 (어떤 값을 생성할 수 없는 거, 즉 마지막으로 생성되는 것인데 예를 들면 pdf에서 :=, ;, + 등등)
    논 터미널들을 함수로 구현되어 있는데 함수 이름을 보면 알 수 있음.
    함수들 그렇게 어렵지 않은데 유심히 보면 흐름이 보인다 그냥 읽어보셈.

    => 프로그램 실행하게 되면 파일에 있는 값들 전부 읽음, tokenize함수를 통해 whitespace를 기준으로 파일에 있는 값들을 다 분리시켜서 tokens에 저장함. 
    그리고 lexical()함수를 통해 tokens 배열에 가장 첫번째에 있는 값을 읽고 next_token에는 그 값에 해당하는 token을, token_string은 가장 첫번째에 있는 값 자체를 저장하고, index를 1 증가시킴.
    그리고 parse_statements함수를 거치고, parse_statement, parse_expressions 함수.. 순차적으로 거쳐가면서 값을 확인하는데 이건 직접 봐야 하고..
    
    가장 중요한 건 lexical 함수인데 기존 토큰 확인하고 다음 토큰으로 넘어갈 때 하는거임 이게 계속 쓰이는데 역할을 분명히 알고가야 함..





<CFG 관련>
    statements, statement, expression 생성자들은 함수 이름을 보면 쉽게 알 수 있음

    term_factor, term, factor, factor_tail 생성자들도 마찬가지로 함수로 구현되어 있는데

    term_factor, term 생성자는 parse_term() 함수에 같이 구현되어 있음 
    -> 이건 나도 따로 따로 분리하고 싶었는데 값을 리턴하는 부분에서 꼬여서 이게 최선인 것 같음

    factor, factor_tail 생성자도 마찬가지로 parse_factor 함수에 같이 구현되어 있음
    -> 이건 나도 따로 따로 분리하고 싶었는데 값을 리턴하는 부분에서 꼬여서 이게 최선인 것 같음

    assignment_op, semi_colon, add_operator 등등 terminal하나에 일대일 대응되는 non_terminal 생성자들이 있는데 이것들은 전 부 lexical()함수에 구현되어 있다.


<출력 부분>
    오류, 경고가 동시에 발생하면 오류 우선
    
    if 수정해서 기존의 input값이 바뀌는 경우
        if 바뀌어도 올바른 CFG 안됨
            기존의 input값 출력

        elif 바뀌어서 올바른 CFG됨
            수정된 input값 출력

        elif 바뀌어서 올바른 CFG가 되는데, 선언되지 않은 변수 오류 뜨면?
            바뀐 input값 출력 
            (그런데 Error Message만 뜨게 해뒀는데, 여기서 Warning Message도 출력을 해줘야 할 것 같은데 왜냐하면 추가한 input값을 보여줘야 하기 때문에 
            => 이 부분은 교수님께 여쭤봐야 할 것 같아서 바뀔 수도 있음, 근데 출력 부분만 살짝 바뀌는거라 큰 상관은 없음 )

    elif input값 안바뀌면
        기존의 input값 출력

    


                <<설명이 난잡한데 모르는 거 있으면 물어보센>>
