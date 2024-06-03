import asyncio

user_keywords = ['비행기', '자동자', '배', '사과', '옥수수', '미국', '해외', '러시아', '한국', '백엔드', '개발자', '태양력', '풍력', '발전기']
total_keywords = ['비행기', '옥수수', '배', '개구리', '사자', '러시아', '개발자', '백엔드', '태양력', '발전기', '과자', '전화']
post_keywords = {'자전거': ['바이트', '산악'],
                 '구급차': ['병원차', '엠뷸런스'],
                 '사과': ['풋사과', '방울사과'],
                 '미국': ['아메리카', '자유주의'],
                 '개발자': ['싸피', '공부'],
                 '프론트엔드': ['디자인', 'HTML'],
                 '풍력': ['자연적', '바람'],
                 '발전기': ['전기생산', '자연친화'],
                 '빼빼로': ['11월11일', '커플'],
                 '초코송이': ['버섯모양', '작은과자'],
                 '갤럭시': ['삼성', '한국기업'],
                 '아이폰': ['미국', '외국기업'],
                 '전화': ['스마트폰', '집전화'], }
user = True


class GetPostMatchKeyword():

    # 기본값으로 초기화
    def __init__(self):
        self.키워드리스트 = []
        self.키워드캐싱리스트 = []  # db내 키워드 인덱스가 변함에 따라 중복 키워드 확인을 방지하기 위해 50개의 키워드만 캐싱
        self.키워드리스트출처 = ''  # 지정 단어 : Total, User, Mix
        self.키워드반복횟수 = 10
        self.키워드사용갯수 = 10
        self.키워드호출갯수 = 50
        self.키워드10개이상있음 = True

        self.재사용키워드리스트 = []

        self.반환포스트리스트 = []
        self.반환포스트갯수 = 5
        self.포스트호출id = 0  # 해당 키워드를 가진 포스트 중 [1]번째 포스트 가져오기
        self.실행완료여부 = False
        self.반환텍스트 = ''

    # 전체키워드 호출 코드의 재사용성을 위해 메서드로 제작
    def 전체키워드호출및저장_메서드(self):
        db_레코드_갯수 = len(total_keywords)  # 메모리 절약을 위해 count로 레코드 갯수만 확인
        if db_레코드_갯수 > self.키워드호출갯수:
            self.키워드캐싱리스트 = total_keywords[:self.키워드호출갯수]
        else:
            self.키워드캐싱리스트 = total_keywords

    def 키워드리스트_선행_작업_메서드(self):
        # 키워드 반복 횟수 지정
        if len(self.키워드캐싱리스트) < self.키워드반복횟수:  # 원본키워드 갯수가 키워드 초기 갯수(10개)보다 적을 경우
            self.키워드리스트 = self.키워드캐싱리스트
            self.키워드반복횟수 = len(self.키워드캐싱리스트)  # 키워드 초기 갯수를 원본 키워드 초기 갯수(9이하)로 설정
            # self.키워드호출갯수 = len(self.키워드리스트) # 키워드 초기 호출 갯수를 원본 키워드 초기 갯수(9이하)로 설정
            self.키워드10개이상있음 = False
            self.키워드캐싱리스트.clear()  # 요소를 삭제함으로써 메모리 확보하기 위해 캐싱 리스트 초기화
        else:  # 키워드 갯수가 10개 이상인 경우
            self.키워드리스트 = self.키워드캐싱리스트[:self.키워드반복횟수]  # 키워드 반복 횟수만큼만 호출

    # 키워드 맞춤 포스트 탐색 함수
    async def 키워드_맞춤_포스트_탐색_함수(self):
        # 키워드 맞춤 포스트 조사 실행
        for 키워드선택번호 in range(self.키워드반복횟수):  # 키워드 리스트의 초기 갯수대로 반복
            키워드 = self.키워드리스트[키워드선택번호]

            if 키워드 in post_keywords:
                self.반환포스트리스트.append(post_keywords[키워드][self.포스트호출id])
                if not self.포스트호출id:
                    self.재사용키워드리스트.append(키워드)

            # 목표 포스트 수량 확인 후, 달성하면 위 while문 정지를 위해 True로 변환 뒤 반복 중단
            if len(self.반환포스트리스트) == self.반환포스트갯수:
                self.반환텍스트 = '맞춤형 포스트 추천'
                self.실행완료여부 = True
                break

        if len(self.반환포스트리스트) < self.반환포스트갯수:
            await self.세부_검증_메서드()

    # 실행 결과 검증 메서드
    async def 세부_검증_메서드(self):

        # 재사용 키워드 리스트에 키워드 존재 시, 설정 변경하여 재실행
        if self.재사용키워드리스트:
            self.포스트호출id += 1  # 해당 키워드의 다음번째 포스트 호출
            self.키워드리스트 = self.재사용키워드리스트  # 재사용키워드로 대체
            self.키워드반복횟수 = len(self.재사용키워드리스트)
            self.재사용키워드리스트 = []  # 재사용키워드리스트 초기화
            await self.키워드_맞춤_포스트_탐색_함수()

        elif self.키워드10개이상있음:
            self.포스트호출id = 0
            del self.키워드캐싱리스트[:self.키워드사용갯수]
            self.키워드리스트_선행_작업_메서드()
            await self.키워드_맞춤_포스트_탐색_함수()

        else:  # 재사용 가능한 키워드도 없고, 추가 호출 가능한 키워드도 없을 경우
            if self.키워드리스트출처 == 'User':
                if self.반환포스트리스트:
                    self.키워드리스트출처 = 'Mix'
                else:
                    self.키워드리스트출처 = 'Total'

                self.포스트호출id = 0
                self.전체키워드호출및저장_메서드()
                self.키워드리스트_선행_작업_메서드()
                await self.키워드_맞춤_포스트_탐색_함수()

            else:
                if self.반환포스트리스트:
                    self.반환텍스트 = '일부 포스트만 추천'
                else:
                    self.반환텍스트 = '추천 키워드 및 포스트 없음'

                self.실행완료여부 = True

    def 반환데이터정리(self):
        최종반환데이터 = {
            '포스트출처': self.키워드리스트출처,
            '반환텍스트': self.반환텍스트,
            '반환포스트': self.반환포스트리스트,
        }
        return 최종반환데이터

    # 키워드 리스트 설정
    async def test_main(self, user):

        # 유저 로그린 여부 따른 메서드 실행
        if user and user_keywords:  # 사용자가 로그인 상태이고, 해당 유저 키워드가 있으면 실행
            self.키워드리스트출처 = 'User'
            db_레코드_갯수 = len(user_keywords)  # 메모리 절약을 위해 count로 레코드 갯수만 확인
            if db_레코드_갯수 > self.키워드호출갯수:
                self.키워드캐싱리스트 = user_keywords[:self.키워드호출갯수]
            else:
                self.키워드캐싱리스트 = user_keywords

        elif total_keywords:  # 사용자가 비로그인 상태이면, 전체 키워드가 있으면 실행
            self.키워드리스트출처 = 'Total'
            self.전체키워드호출및저장_메서드()

        else:  # 로그인 유저도 아니고, 전체 키워드에도 키워드가 없으면 실행
            self.반환텍스트 = '추천 키워드 없음.'
            최종반환데이터 = self.반환데이터정리()  # 추후 출력 함수에 해당 데이터 첨부하여 실행
            return 최종반환데이터

        self.키워드리스트_선행_작업_메서드()
        await self.키워드_맞춤_포스트_탐색_함수()

        while self.실행완료여부 == False:
            await asyncio.sleep(2)  # 반복 메서드들의 작업 완료 여부를 2초마다 확인

        최종반환데이터 = self.반환데이터정리()

        return 최종반환데이터


async def run_test():
    test = GetPostMatchKeyword()
    result = await test.test_main(user)
    print(result)


asyncio.run(run_test())