import pymysql
import datetime
import os

conn = pymysql.connect(host='210.110.34.148', user='pinwoo', passwd='1234', db='hyein', charset='utf8')


def write_daily(name):
    print("<연구일지 작성, 수정, 삭제는 모두 본인것만 가능합니다.>")
    print("1. 연구일지 작성")
    print("2. 연구일지 수정")
    print("3. 연구일지 삭제")
    print("4. 종료")
    choice = int(input())
    if choice == 1:
        writeDaily = input("내용 입력 -> ")
        try:
            with conn.cursor() as curs:
                sql = ("insert into research (name, date, research, comment, ck) values ('%s', '%s', '%s', '%s', '%s')"%(name, datetime.date.today(), writeDaily, 'standby', 'x'))
                curs.execute(sql)
                conn.commit()
                print("연구일지 작성 완료\n")                       
        except Exception as e:
            print (type(e))
    elif choice == 2:
        try:
            with conn.cursor() as curs:
                sql = ("select * from research where name = '%s'" %name)
                curs.execute(sql)
                result = curs.fetchall()
                print("-----------------------------------------------------------------------------------------------------")
                for row_data in result:
                    print("no. %s  name : %s  date : %s  research : %s" %(row_data[0], row_data[1], row_data[2], row_data[3]))
                print("-----------------------------------------------------------------------------------------------------")
                conn.commit()
                changenum = int(input("수정 할 연구일지 선택  -> "))
                changeDaily = input("수정할 일지 내용 입력 -> ")
                try:
                    with conn.cursor() as curs:
                        sql = ("update research set research = '%s' where number = %d "%(changeDaily, changenum))
                        curs.execute(sql)
                        conn.commit()
                        print("연구일지 수정 완료")
                except Exception as e:
                    print (type(e))
        except Exception as e:
            print (type(e))
    elif choice == 3:
        try:
            with conn.cursor() as curs:
                sql = ("select * from research where name = '%s'" %name)
                curs.execute(sql)
                result = curs.fetchall()
                print("-----------------------------------------------------------------------------------------------------")
                for row_data in result:
                    print("no. %s  name : %s  date : %s  research : %s" %(row_data[0], row_data[1], row_data[2], row_data[3]))
                print("-----------------------------------------------------------------------------------------------------")
                conn.commit()
                deletenum = int(input("삭제 할 연구일지 선택 -> "))
                try:
                    with conn.cursor() as curs:
                        sql = ("insert into deletedresearch select * from research where number = %d" %deletenum)
                        curs.execute(sql)
                        conn.commit()
                        try:
                            with conn.cursor() as curs:
                                sql = ("delete from research where number = %d" %deletenum)
                                curs.execute(sql)
                                conn.commit()
                                print("연구일지 삭제 완료")
                                try:
                                    with conn.cursor() as curs:
                                        curs.execute("alter table research auto_increment = 1")
                                        curs.execute("set @cnt = 0")
                                        curs.execute("update research set research.number = @cnt:=@cnt+1")
                                        conn.commit()
                                except Exception as e:
                                    print(type(e))
                        except Exception as e:
                            print(type(e))
                except Exception as e:
                    print(type(e))
        except Exception as e:
            print(type(e))
    else:
        print("exit")


def research_daily():
    print("1. 날짜별")
    print("2. 연구원별")
    print("3. 전체")
    print("4. 종료")
    choice = int(input())
    if choice == 1:
        dateresearch = input("원하는 날짜 입력(YYYY/MM/DD) -> ")
        try:
            with conn.cursor() as curs:
                sql = ("select * from research where date = %s" %dateresearch)
                curs.execute(sql)
                result = curs.fetchall()
                print("-------------------------------------------------------------------------------------------------------------------------------")
                for row_data in result:
                    if dateresearch == row_data[2]:
                        print("no. %s  name : %s  date : %s  research : %s  comment : %s" %(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4]))
                print("-------------------------------------------------------------------------------------------------------------------------------")
                conn.commit()
        except Exception as e:
             print(type(e))
    elif choice == 2:
        rresearch = input("연구원 이름 입력 -> ")
        try:
            with conn.cursor() as curs:
                sql = ("select * from research where name = %s" %rresearch)
                curs.execute(sql)
                result = curs.fetchall()
                print("-------------------------------------------------------------------------------------------------------------------------------")
                for row_data in result:
                    if rresearch == row_data[1]:
                        print("no. %s  name : %s  date : %s  research : %s  comment : %s" %(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4]))
                print("-------------------------------------------------------------------------------------------------------------------------------")
                conn.commit()
        except Exception as e:
            print(type(e))
    elif choice == 3:
        try:
            with conn.cursor() as curs:
                sql = "select * from research"
                curs.execute(sql)
                result = curs.fetchall()
                print("-------------------------------------------------------------------------------------------------------------------------------")
                for row_data in result:
                    print("no. %-2s  name : %-4s  date : %s  research : %s  comment : %s" %(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4]))
                print("-------------------------------------------------------------------------------------------------------------------------------")
                conn.commit()
        except Exception as e:
            print(type(e))
    elif choice == 4:
        print("종료합니다")
    else:
        print("잘못된 입력입니다.")


def show_researcher():
    print("-------------------------------------------PINLAB-----------------------------------------------------")
    print("가입하지 않은 연구원 정보는 등록되있지 않을 수 있습니다")
    try:
        with conn.cursor() as curs:
            sql = "select * from personal"
            curs.execute(sql)
            result = curs.fetchall()
            for row_data in result:
                print("name : %s  birth : %s  phone : %s  ID : %s  grade : %s" %(row_data[0], row_data[1], row_data[2], row_data[3], row_data[5]))
            print("-------------------------------------------------------------------------------------------------------")
            conn.commit()
    except Exception as e:
        print(type(e))


def check_comment(name):
    count = 0
    try:
        with conn.cursor() as curs:
            sql = ("select * from research where name = '%s' and ck = 'x' and comment not in ('standby')" %name)
            curs.execute(sql)
            result = curs.fetchall()
            print("-------------------------------------------------------------------------------------------------------------------------------")
            for row_data in result:
                if comment!='standby':
                    count += 1
                    print("no. %s  name : %s  date : %s  research : %s  comment : %s" %(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4]))
                    try:
                        with conn.cursor() as curs:
                            sql = ("update research set ck = 'o' where name = '%s' and comment not in ('standby')" %name)
                            curs.execute(sql)
                            conn.commit()
                    except Exception as e:
                        print(type(e))
            print("-------------------------------------------------------------------------------------------------------------------------------")
            conn.commit()
            if count == 0:
                print("코멘트 달린 연구일지가 없습니다.")
    except Exception as e:
        print(type(e))


def write_info():
    print("1. 연구원 등록")
    print("2. 연구원 정보 수정")
    print("3. 연구원 정보 삭제")
    print("4. 프로그램 종료")
    choice = int(input("입력 -> "))
    if choice == 1:
        print("등록할 연구원 정보를 입력해 주세요")
        name = input("이름 -> ")
        birth = input("생년월일 -> ")
        phone = int(input("전화번호 -> "))
        grade = input("등급 -> ")
        try:
            with conn.cursor() as curs:
                sql = ("insert into personal (name, birth, phone, ID, PW, grade, ch) values ('%s', '%s', %s, '%s', '%s', '%s', 'unconfirmed')" %(name, birth, phone, name, birth, grade))
                curs.execute(sql)
                conn.commit()
            print("연구원 등록 완료")
        except Exception as e:
            print(type(e))
    elif choice == 2:
        try:
            with conn.cursor() as curs:
                sql = "select * from personal"
                curs.execute(sql)
                result = curs.fetchall()
                print("-------------------------------------------PINLAB-----------------------------------------------------")
                for row_data in result:
                    print("name : %s  birth : %s  phone : %s  ID : %s  grade : %s" %(row_data[0], row_data[1], row_data[2], row_data[3], row_data[5]))
                print("------------------------------------------------------------------------------------------------------")
                conn.commit()
        except Exception as e:
            print(type(e))
        changePersonal= input("변경할 연구원을 입력해 주세요 -> ")
        print("무엇을 변경할까요?")
        changeObject = input("name, birth, phone, grade -> ")
        changeContents = input("변경할 내용을 입력하세요 -> ")
        try:
            with conn.cursor() as curs:
                sql = ("update personal set " + changeObject + " = '" + changeContents + "' where name = '" + changePersonal + "'")
                curs.execute(sql)
                conn.commit()
            print("연구원 수정 완료")
        except Exception as e:
            print(type(e))
    elif choice == 3:
        try:
            with conn.cursor() as curs:
                sql = "select * from personal"
                curs.execute(sql)
                result = curs.fetchall()
                print("-------------------------------------------PINLAB-----------------------------------------------------")
                for row_data in result:
                    print("name : %s  birth : %s  phone : %s  ID : %s  grade : %s" %(row_data[0], row_data[1], row_data[2], row_data[3], row_data[5]))
                print("------------------------------------------------------------------------------------------------------")
                conn.commit()
                deletedPersonal = input("삭제할 연구원을 입력해 주세요 -> ")
                try:
                    with conn.cursor() as curs:
                        sql = ("insert into deletedpersonal select * from personal where name = '%s'" %deletedPersonal)
                        curs.execute(sql)
                        conn.commit()
                        try:
                            with conn.cursor() as curs:
                                sql = ("delete from personal where name = '%s'" %deletedPersonal)
                                curs.execute(sql)
                                conn.commit()
                                print("연구원 삭제 완료")
                        except Exception as e:
                            print(type(e))
                except Exception as e:
                    print(type(e))
        except Exception as e:
            print(type(e))


def trash_budget():
    print("--------휴지통--------")
    print("1. 삭제된 연구일지")
    print("2. 삭제된 연구원 목록")
    print("3. 종료")
    choice = int(input("입력 -> "))
    if choice == 1:
        try:
            with conn.cursor() as curs:
                sql = "select * from deletedresearch"
                curs.execute(sql)
                result = curs.fetchall()
                print("-------------------------------------------------------------------------------------------------------------------------------")
                for row_data in result:
                    print("name : %s  date : %s  research : %s  " %(row_data[1], row_data[2], row_data[3]))
                print("-------------------------------------------------------------------------------------------------------------------------------")
                conn.commit()
                print("휴지통 내역을 복원하시겠습니까?(Y/N)")
                choice2 = input("->")
                if (choice2 == 'y') or (choice2 == 'Y'):
                    print("복원할 일지의 이름, 날짜, 연구내용을 작성해 주세요")
                    name = input("이름 -> ")
                    date = input("날짜(YYYY-MM-DD) -> ")
                    content = input("일지 내용 -> ")
                    try:
                        with conn.cursor() as curs:
                            sql = ("insert into research (name, date, research, comment, ck) values ('%s', '%s', '%s', 'standby', 'x')" %(name, date, content))
                            curs.execute(sql)
                            conn.commit()
                            try:
                                with conn.cursor() as curs:
                                    sql = ("delete from deletedresearch where name = '%s' and date = '%s' and research = '%s'" %(name, date, content))
                                    curs.execute(sql)
                                    conn.commit()
                            except Exception as e:
                                print(type(e))
                            print("연구일지 복원 완료.")
                    except Exception as e:
                        print(type(e))
                elif (choice2 == 'n') or (choice2 == 'N'):
                    print("복원취소")
                else:
                    print("잘못된 입력입니다.")
        except Exception as e:
            print(type(e))
    elif choice == 2:
        try:
            with conn.cursor() as curs:
                sql = "select * from deletedpersonal"
                curs.execute(sql)
                result = curs.fetchall()
                print("-------------------------------------------PINLAB-----------------------------------------------------")
                for row_data in result:
                    print("name : %s  birth : %s  phone : %s  ID : %s  grade : %s" %(row_data[0], row_data[1], row_data[2], row_data[3], row_data[5]))
                print("------------------------------------------------------------------------------------------------------")
                conn.commit()
                print("휴지통 내역을 복원하시겠습니까?(Y/N)")
                choice3 = input("->")
                if (choice3 == 'y') or (choice3 == 'Y'):
                    print("복원할 연구원의 이름을 입력해 주세요.")
                    replaceName = input(" -> ")
                    try:
                        with conn.cursor() as curs:
                            sql = ("insert into personal select * from deletedpersonal where name = '%s'" %replaceName)
                            curs.execute(sql)
                            conn.commit()
                            try:
                                with conn.cursor() as curs:
                                    sql = ("delete from deletedpersonal where name = '%s'" %replaceName)
                                    curs.execute(sql)
                                    conn.commit()
                            except Exception as e:
                                print(type(e))
                            print("연구원 정보 복원 완료.")
                    except Exception as e:
                        print(type(e))
                elif (choice3 == 'n') or (choice3 == 'N'):
                    print("복원취소")
                else:
                    print("잘못된 입력입니다.")
        except Exception as e:
            print(type(e))
    elif choice == 3:
        print("휴지통을 종료합니다")
    else:
        print("잘못된 입력입니다.")


def initialization():
    print("초기화 할 목록을 선택해 주세요")
    print("1. 연구원 목록")
    print("2. 연구일지")
    print("3. 연구원 목록 (in 휴지통)")
    print("4. 연구일지 (in 휴지통)")
    print("5. 종료")
    choice = int(input(" -> "))

    if choice == 1:
        print("정말로 초기화 하시겠습니까?(Y/N)")
        choice2 = int(input(" -> "))
        if (choice2 == 'y') or (choice2 == 'Y'):
            try:
                with conn.cursor() as curs:
                    sql = "truncate table personal"
                    curs.execute(sql)
                    conn.commit()
                    print("초기화 완료")
            except Exception as e:
                print(type(e))
        elif (choice2 == 'n') or (choice2 == 'N'):
            print("초기화 종료")
        else:
            print("잘못된 입력입니다.")
    elif choice == 2:
        print("정말로 초기화 하시겠습니까?(Y/N)")
        choice2 = int(input(" -> "))
        if (choice2 == 'y') or (choice2 == 'Y'):
            try:
                with conn.cursor() as curs:
                    sql = "truncate table research"
                    curs.execute(sql)
                    conn.commit()
                    print("초기화 완료")
            except Exception as e:
                print(type(e))
        elif (choice2 == 'n') or (choice2 == 'N'):
            print("초기화 종료")
        else:
            print("잘못된 입력입니다.")
    elif choice == 3:
        print("정말로 초기화 하시겠습니까?(Y/N)")
        choice2 = int(input(" -> "))
        if (choice2 == 'y') or (choice2 == 'Y'):
            try:
                with conn.cursor() as curs:
                    sql = "truncate table deletedpersonal"
                    curs.execute(sql)
                    conn.commit()
                    print("초기화 완료")
            except Exception as e:
                print(type(e))
        elif (choice2 == 'n') or (choice2 == 'N'):
            print("초기화 종료")
        else:
            print("잘못된 입력입니다.")
    elif choice == 4:
        print("정말로 초기화 하시겠습니까?(Y/N)")
        choice2 = int(input(" -> "))
        if (choice2 == 'y') or (choice2 == 'Y'):
            try:
                with conn.cursor() as curs:
                    sql = "truncate table deletedresearch"
                    curs.execute(sql)
                    conn.commit()
                    print("초기화 완료")
            except Exception as e:
                print(type(e))
        elif (choice2 == 'n') or (choice2 == 'N'):
            print("초기화 종료")
        else:
            print("잘못된 입력입니다.")
    elif choice == 5:
        print("초기화를 종료합니다.")
    else:
        print("잘못된 입력입니다.")
    

def write_comment():
    try:
        with conn.cursor() as curs:
            sql = "select * from research"
            curs.execute(sql)
            result = curs.fetchall()
            print("-------------------------------------------------------------------------------------------------------------------------------")
            for row_data in result:
                print("no. %s  name : %s  date : %s  research : %s  comment : %s" %(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4]))
            print("-------------------------------------------------------------------------------------------------------------------------------")
            commentNum = int(input("코멘트를 작성할 번호를 입력해 주세요 -> "))
            writeComment = input("코멘트 작성 -> ")
            try:
                with conn.cursor() as curs:
                    sql = ("update research set comment = '%s' where number = %d" %(writeComment, commentNum))
                    curs.execute(sql)
                    print("코멘트 작성 완료")
                    conn.commit()
            except Exception as e:
                print(type(e))
    except Exception as e:
        print(type(e))


while True:
    conn = pymysql.connect(host='210.110.34.148', user='pinwoo', passwd='1234', db='hyein', charset='utf8')
    print("1. login")
    print("2. signup")
    print("3. exit")
    account = int(input())

    if account == 1:
        check = 0
        print("로그인을 진행합니다.")
        print("아이디와 비밀번호를 입력해주세요")
        inputID = input("ID : ")
        inputPW = input("PASSWORD : ")
        try:
            with conn.cursor() as curs:
                sql = "select * from personal"
                curs.execute(sql)
                result = curs.fetchall()
                for row_data in result:
                    if (inputID == row_data[3])&(inputPW == row_data[4]):
                        check += 1
                        print("%s님 반갑습니다." % row_data[0])
                        if row_data[5] == 'undergraduate':
                            while True:
                                try:
                                    with conn.cursor() as curs:
                                        sql = ("select * from research where name = '%s' and ck = 'x' and comment not in ('standby')" %row_data[0])
                                        curs.execute(sql)
                                        result = curs.fetchall()
                                        for row_data in result:
                                            print("[comment update]")
                                except Exception as e:
                                    print(type(e))
                                print("*****학부생 %s님*****" % row_data[0])
                                print("1. 연구일지 작성/수정/삭제")
                                print("2. 연구일지 확인")
                                print("3. 연구원 정보 열람")
                                print("4. 코멘트 작성된 연구일지 확인")
                                print("5. 로그아웃")
                                a = int(input())
                                if a == 1:
                                    realname = row_data[0]
                                    write_daily(realname)
                                elif a == 2:
                                    research_daily()
                                elif a == 3:
                                    show_researcher()
                                elif a == 4:
                                    realname2 = row_data[0]
                                    check_comment(realname2)
                                elif a == 5:
                                    print("<logout>")
                                    break
                                else:
                                    print("잘못된 입력입니다.")
                            
                        elif row_data[5] == 'master':
                            while True:
                                try:
                                    with conn.cursor() as curs:
                                        sql = ("select * from research where name = '%s' and ck = 'x' and comment not in ('standby')" %row_data[0])
                                        curs.execute(sql)
                                        result = curs.fetchall()
                                        for row_data in result:
                                            print("[comment update]")
                                except Exception as e:
                                    print(type(e))
                                print("*****석사생 %s님*****" % row_data[0])
                                print("1. 연구일지 작성/수정/삭제")
                                print("2. 연구일지 확인")
                                print("3. 연구원 정보 열람")
                                print("4. 연구원 등록/수정/삭제")
                                print("5. 코멘트 작성된 연구일지 확인")
                                print("6. 휴지통")
                                print("7. 로그아웃")
                                b = int(input())
                                if b == 1:
                                    realname = row_data[0]
                                    write_daily(realname)
                                elif b == 2:
                                    research_daily()
                                elif b == 3:
                                    show_researcher()
                                elif b == 4:
                                    write_info()
                                elif b == 5:
                                    realname2 = row_data[0]
                                    check_comment(realname2)
                                elif b == 6:
                                    trash_budget()
                                elif b == 7:
                                    print("<logout>")
                                    break
                                else:
                                    print("잘못된 입력입니다.")
                        else:
                            while True:
                                print("*****교수 %s님*****" % row_data[0])
                                print("1. 연구일지 작성/수정/삭제")
                                print("2. 연구일지 확인")
                                print("3. 연구일지 코멘트 작성")
                                print("4. 연구원 정보 열람")
                                print("5. 휴지통")
                                print("6. 초기화")
                                print("7. 로그아웃")
                                c = int(input())
                                if c == 1:
                                    realname = row_data[0]
                                    write_daily(realname)
                                elif c == 2:
                                    research_daily()
                                elif c == 3:
                                    write_comment()
                                elif c == 4:
                                    show_researcher()
                                elif c == 5:
                                    trash_budget()
                                elif c == 6:
                                    initialization()
                                elif c == 7:
                                    print("<logout>")
                                    break
                                else:
                                    print("잘못된 입력입니다/")
                if check == 0:
                    print("ID나 PW가 일치하지 않습니다.")
                conn.commit()
        except Exception as e:
            print(type(e))
        finally:
            conn.close()

    elif account == 2:
        check1 = 0
        print("회원가입을 진행합니다")
        print("***********************************본인 확인***********************************")
        print("//아직 회원님의 정보가 등록 되있지 않을 시 회원가입에 제한이 있을 수 있습니다//")
        inputname = input("이름 : ")
        inputbirth = input("생년월일 : ")
        inputphone = input("전화번호 : ")
        try:
            with conn.cursor() as curs:
                sql = "select * from personal where ch = 'unconfirmed'"
                curs.execute(sql)
                result = curs.fetchall()
                for row_data in result:
                    if (inputname == row_data[0])&(inputbirth == row_data[1])&(inputphone == row_data[2]):
                        check1 += 1
                        print("%s님 반갑습니다." % row_data[0])
                        print("회원가입을 진행합니다.")
                        overlap = 0
                        makeID = input("아이디 -> ")
                        try:
                            with conn.cursor() as curs:
                                sql = "select * from personal"
                                curs.execute(sql)
                                result = curs.fetchall()
                                for row_data in result:
                                    if makeID == row_data[3]:
                                        overlap += 1
                                        print("중복된 아이디 입니다.")
                                if overlap == 0:
                                    print("사용가능한 아이디 입니다.")
                                    makePW = input("비밀번호 -> ")
                                    try:
                                        with conn.cursor() as curs:
                                            sql = ("update personal set ID = '%s', PW = '%s', ch = 'confirmed' where name = '%s'" %(makeID, makePW, inputname))
                                            curs.execute(sql)
                                            conn.commit()
                                            print("회원가입이 완료되었습니다.")
                                    except Exception as e:
                                        print(type(e))
                                conn.commit()
                        except Exception as e:
                            print(type(e))         
                if check1 == 0:
                    print("아직 회원정보가 등록되지 않으셨습니다. 등록되었는지 확인 후 다시 시도해 주세요.")
                conn.commit()
        except Exception as e:
            print(type(e))
        finally:
            conn.close()
    else:
        print("프로그램을 종료합니다.")
        break
        
       
    
    

