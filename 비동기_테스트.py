# 추천 기능 구현 시, 동기적 메서드 반복 호출로 인한 스택 오버플로우 및 리소스 낭비를 방지하기 위해 비동기로 구현 테스트

import asyncio


class AsyncioTest:
    def __init__(self):
        self.test_data = [23, 45, 101, 52, 43, 1, 5, 16, 97, 7, 185, 36, 66, 78, 95, 111, 3, 22, 77, 16, 19, 46, 57, 68,
                          99, 113,
                          124, 135]
        self.a_number = 100
        self.b_count = 0
        self.start_index = 0
        self.for_routin = 5
        self.list_number = 5
        self.summit_list = []
        self.completion = False

    async def main(self):

        await self.a_routine()

        while not self.completion:
            await asyncio.sleep(1)

        summit_list = self.summit_list

        return summit_list

    async def a_routine(self):
        for i in range(self.start_index, self.for_routin):
            if self.test_data[i] > self.a_number:
                self.summit_list.append(self.test_data[i])

            if len(self.summit_list) == self.list_number:
                self.completion = True
                break

        if len(self.summit_list) == self.list_number:
            self.completion = True
        else:
            await self.b_routine()

    async def b_routine(self):
        if len(self.test_data) > self.for_routin:
            self.start_index = self.for_routin
            self.for_routin += 5
            await self.a_routine()

        elif len(self.test_data) == self.for_routin:
            self.completion = True

        else:
            self.start_index = self.for_routin
            self.for_routin = len(self.test_data)
            await self.a_routine()


async def run_test():
    test = AsyncioTest()
    result = await test.main()
    print(result)


asyncio.run(run_test())
