import asyncio
import json
import re
import sys
import time
from typing import Any

from app import models
from app.database import Session
from app.getgema_gather import GetgemaGather


def re_all_cursor(value: str) -> list[str]:
    # 定义正则表达式模式
    pattern = r'"(T,\d{1,12},\d{8,24})"'
    pattern = r'"cursor":\s"(.{1,32},.{1,32},.{1,32})",'
    
    # 查找所有匹配项
    return re.findall(pattern, value)


def re_all_numbers(value: str) -> list[str]:
    # 定义正则表达式模式
    pattern = r'"(\+888\s\d{1,6}\s\d{1,6})"'
    
    # 查找所有匹配项
    return re.findall(pattern, value)


async def main():
    getgema_gather = GetgemaGather()
    
    cursor = None
    for i in range(4878):
        for _ in range(3):
            try:
                time.sleep(1)
                result = await getgema_gather.nft_search(
                    "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N",
                    "af904314608b2384958183c1c667de0028660f25c628a6a0ae9512e8c70a840e",
                    cursor
                )
                
                json_str = json.dumps(result)
                
                # 获取下一页游标
                cursors = re_all_cursor(json_str)
                if len(cursors) > 0:
                    cursor = cursors[-1]
                    print(f"next cursor - {cursor}")
                else:
                    sys.exit()
                
                # 获取所有手机号
                _numbers = [n.replace(" ", "") for n in re_all_numbers(json_str)]
                print(f"第 {i + 1} 页 - {_numbers}")
                
                # 添加到数据库
                with Session() as session:
                    for _number in _numbers:
                        try:
                            is_exist = session.query(models.ThreeEightsNumbers).filter(
                                models.ThreeEightsNumbers.number == _number
                            ).count()
                            if is_exist > 0:
                                continue
                            number_data = models.ThreeEightsNumbers(number=_number)
                            session.add(number_data)
                            session.commit()
                        except Exception as e:
                            print(f"第 {i + 1} 页 - 发生错误 - 添加到数据库 - {_number} - {e}")
                
                break
            except Exception as e:
                print(f"第 {i + 1} 页 - 发生错误 - {e}")
                continue
    
    pass


if __name__ == '__main__':
    asyncio.run(main())
    pass
