# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from models import AiQuestion, AiAnswer, Count
# from datetime import datetime, timedelta
# from django.core.exceptions import ObjectDoesNotExist

# # 유저 로그인시 ai 질문 생성 횟수 복구 판단 로직
# @receiver(user_logged_in)
# # @receiver 데코레이터는 시그널을 처리하기 위해 함수를 등록할 때 사용됨.
# # @receiver은 지정한 시그널(user_logged_in)과 내가 실행하려는 아래 함수를 연결시키는 역할이다.
# def question_check(sender, user, request, **kwargs):
    
#     # 로그인한 유저의 최근 질문 데이터를 가져온다.
#     question_data = AiQuestion.objects.filter(user=user).order_by('-created').first()
#     # 로그인한 유저의 최근 질문 데이터가 있을 경우, 해당 데이터의 created를 가져온다.
#     if question_data:
#         auto_question_created = question_data.created
#     else:
#         auto_question_created = None
    
#     try:
#         # 로그인한 유저의 count 데이터 조회(save 기능을 쓰기 위해 분리해서 작성)
#         question_count_data = Count.objects.get(user=user)
#         # 로그인한 유저의 count 데이터에서 question_count 데이터 가져오기
#         auto_question_count = question_count_data.question_count
#     except ObjectDoesNotExist:
#         # Count 객체가 존재하지 않는 경우, 새로운 Count 객체를 생성하여 초기화
#         question_count_data = Count.objects.create(user=user, question_count=2, answer_count=1)
#         question_count_data.save()
#         auto_question_count = question_count_data.question_count
    
#     # 현재 시간 변수
#     today = datetime.now()
    
#     # 로그인한 유저의 질문 생성 횟수 확인 및 재설정
#     # 1차 확인: 해당 유저의 질문 생성 횟수 확인
#     if auto_question_count < 2 or auto_question_count == None:
#         # 2차 확인: 해당 유저가 최근 작성한 질문 데이터가 하루를 지났는지 확인
#         if auto_question_created < today - timedelta(days=1):
#             auto_question_count = 2
#             question_count_data.save()
#         else:
#             pass
#     else:
#         pass
    
# # 유저 로그인시 ai 답변 생성 횟수 복구 판단 로직
# @receiver(user_logged_in)
# def answer_check(sender, user, request, **kwargs):
    
#     # 로그인한 유저의 최근 질문 데이터를 가져온다.
#     answer_data = AiAnswer.objects.filter(user=user).order_by('-created').first()
#     # 로그인한 유저의 최근 질문 데이터가 있을 경우, 해당 데이터의 created를 가져온다.
#     if answer_data:
#         auto_answer_created = answer_data.created
#     else:
#         auto_answer_created = None
    
#     try:
#         # 로그인한 유저의 count 데이터 조회(save 기능을 쓰기 위해 분리해서 작성)
#         answer_count_data = Count.objects.get(user=user)
#         # 로그인한 유저의 count 데이터에서 question_count 데이터 가져오기
#         auto_answer_count = answer_count_data.answer_count
#     except ObjectDoesNotExist:
#         # Count 객체가 존재하지 않는 경우, 새로운 Count 객체를 생성하여 초기화
#         answer_count_data = Count.objects.create(user=user, question_count=2, answer_count=1)
#         answer_count_data.save()
#         auto_answer_count = answer_count_data.answer_count
    
#     # 현재 시간 변수
#     today = datetime.now()
    
#     # 로그인한 유저의 질문 생성 횟수 확인 및 재설정
#     # 1차 확인: 해당 유저의 질문 생성 횟수 확인
#     if auto_answer_count < 1 or auto_answer_count == None:
#         # 2차 확인: 해당 유저가 최근 작성한 질문 데이터가 하루를 지났는지 확인
#         if auto_answer_created < today - timedelta(days=1):
#             auto_answer_count = 1
#             answer_count_data.save()
#         else:
#             pass
#     else:
#         pass